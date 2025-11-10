# -*- coding: utf-8 -*-
"""
Enhanced extractor.py
1. Try requests first
2. If failed, fall back to Playwright (headless Chromium)
Supports: iCIMS, Workday, Greenhouse, Ashby, Lever, SmartRecruiters, BambooHR, etc.
"""

import json
import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
from playwright.sync_api import sync_playwright

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def _extract_from_html(html: str, url: str) -> str:
    """Extract job description text from HTML for common ATS platforms."""
    soup = BeautifulSoup(html, "lxml")
    domain = url.lower()

    # Remove unwanted elements
    for tag in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'button', 'aside']):
        tag.decompose()

    # Remove elements with common noise classes/ids
    noise_selectors = [
        {'class': 'navigation'},
        {'class': 'nav'},
        {'class': 'menu'},
        {'class': 'footer'},
        {'class': 'header'},
        {'class': 'sidebar'},
        {'id': 'header'},
        {'id': 'footer'},
        {'id': 'navigation'},
    ]
    for selector in noise_selectors:
        for element in soup.find_all(attrs=selector):
            element.decompose()

    # iCIMS
    if "icims.com" in domain:
        job_content = soup.find("div", id="jobcontent")
        if job_content:
            return _clean_text(job_content.get_text(" ", strip=True))

    # Workday
    if "myworkdayjobs.com" in domain:
        selectors = [
            {"data-automation-id": "jobPostingDescription"},
            {"data-automation-id": "richTextArea"},
            {"role": "text"},
        ]
        for c in selectors:
            wd_div = soup.find("div", c)
            if wd_div:
                return _clean_text(wd_div.get_text(" ", strip=True))
        wd_section = soup.find("section")
        if wd_section:
            return _clean_text(wd_section.get_text(" ", strip=True))

    # Greenhouse
    if "greenhouse.io" in domain:
        gh_div = soup.find("div", class_="job")
        if gh_div:
            return _clean_text(gh_div.get_text(" ", strip=True))

    # Ashby
    if "ashbyhq.com" in domain:
        ashby_div = soup.find("div", {"data-testid": "JobDescription"})
        if ashby_div:
            return _clean_text(ashby_div.get_text(" ", strip=True))

    # Lever
    if "lever.co" in domain:
        lever_div = soup.find("div", class_="posting")
        if lever_div:
            return _clean_text(lever_div.get_text(" ", strip=True))

    # SmartRecruiters
    if "smartrecruiters.com" in domain:
        sr_div = soup.find("div", class_="job-sections")
        if sr_div:
            return _clean_text(sr_div.get_text(" ", strip=True))

    # BambooHR
    if "bamboohr.com" in domain:
        bh_div = soup.find("div", id="content")
        if bh_div:
            return _clean_text(bh_div.get_text(" ", strip=True))

    # Fallback: try to find main content areas
    main_content = soup.find("main") or soup.find("article") or soup.find("div", role="main")
    if main_content:
        return _clean_text(main_content.get_text(" ", strip=True))

    body_text = soup.get_text(" ", strip=True)
    if body_text:
        return _clean_text(body_text)

    return ""


def _clean_text(text: str) -> str:
    """Clean extracted text by removing common noise patterns."""
    import re

    # Remove Material Icons text patterns
    text = re.sub(r'\b(expand_more|expand_less|person_outline|location_on|work|attach_money|schedule|keyboard_arrow_down|keyboard_arrow_up)\b', '', text, flags=re.IGNORECASE)

    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove button/link noise
    common_noise = [
        'Skip to main content',
        'Sign in',
        'Sign up',
        'Apply now',
        'Save job',
        'Share job',
        'Cookie policy',
        'Privacy policy',
        'Terms of service',
        'Terms and conditions',
    ]
    for noise in common_noise:
        text = text.replace(noise, '')

    return text.strip()


def extract_jd_text(url: str) -> str:
    try:
        res = requests.get(url, timeout=15, headers=DEFAULT_HEADERS, allow_redirects=True)
        text = _extract_from_html(res.text, url)
        if text and len(text) > 200:
            print("Extracted via requests")
            return text
    except Exception as e:
        print(f"requests failed: {e}")

    # Fallback: Playwright
    print("Falling back to Playwright rendering...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        page.wait_for_timeout(5000)  # wait 5s for dynamic content
        html = page.content()
        browser.close()

    text = _extract_from_html(html, url)
    if not text:
        raise RuntimeError("Failed to extract job description after Playwright rendering: " + url)

    print("Extracted via Playwright")
    return text


def analyze_jd(jd_text: str) -> dict:
    prompt = f"""
    You are a recruiting assistant. Analyze this job description and extract structured information.

    Return VALID JSON with this exact schema:

    {{
      "job_title": "Software Engineer",
      "company": "Company Name",
      "location": "City, State or Remote",
      "responsibilities": [
        "Design and develop scalable backend services",
        "Collaborate with cross-functional teams",
        "Mentor junior engineers"
      ],
      "requirements": [
        "5+ years of experience in software development",
        "Strong proficiency in Python and Java",
        "Experience with cloud platforms (AWS/GCP)"
      ],
      "categories": [
        {{"name": "Languages", "skills": ["Python","Java"]}},
        {{"name": "Cloud", "skills": ["AWS","GCP"]}}
      ],
      "flat": ["Python","Java","AWS","GCP"]
    }}

    Rules:
    - Extract job_title, company, and location from the text. If not found, use "Not specified".
    - Extract 3-5 key responsibilities as bullet points. Each should be concise (one line), specific, and actionable.
    - Extract 3-5 key requirements as bullet points. Each should be concise (one line), specific, and measurable when possible.
    - Extract only explicitly mentioned technical skills (languages, frameworks, tools, platforms, cloud, databases, etc.).
    - Do NOT include vague phrases like "strong communication" in skills.
    - Prefer specific names: "Python", "React", "AWS Lambda", "Docker".
    - Classify skills under categories: Languages, Frameworks, Web, Mobile, Cloud, Databases, DevOps, Data/AI, Testing, Security, Hardware/Embedded, Design/UX, Tools, CRM/ERP, Domain/Compliance.
    - Each category should have at most 9 items.
    - Focus on the most important and role-defining information.
    - Output VALID JSON only.

    Job Description:
    {jd_text[:15000]}
    """

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set OPENAI_API_KEY in .env")

    client = OpenAI(api_key=api_key)

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"},
        )
        raw = resp.choices[0].message.content.strip()
        return json.loads(raw)

    except Exception as e:
        print("JSON parse failed:", e)
        return {"error": "LLM response parsing failed"}


# ----------- Test -----------
if __name__ == "__main__":
    test_url = "https://lifeattiktok.com/search/7533023896800495890"
    jd = extract_jd_text(test_url)
    print("First 500 chars:\n", jd[:500])
    skills = analyze_jd(jd[:10000])
    print("Extracted skills:\n", json.dumps(skills, indent=2))
