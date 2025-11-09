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

    # iCIMS
    if "icims.com" in domain:
        job_content = soup.find("div", id="jobcontent")
        if job_content:
            return job_content.get_text(" ", strip=True)

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
                return wd_div.get_text(" ", strip=True)
        wd_section = soup.find("section")
        if wd_section:
            return wd_section.get_text(" ", strip=True)

    # Greenhouse
    if "greenhouse.io" in domain:
        gh_div = soup.find("div", class_="job")
        if gh_div:
            return gh_div.get_text(" ", strip=True)

    # Ashby
    if "ashbyhq.com" in domain:
        ashby_div = soup.find("div", {"data-testid": "JobDescription"})
        if ashby_div:
            return ashby_div.get_text(" ", strip=True)

    # Lever
    if "lever.co" in domain:
        lever_div = soup.find("div", class_="posting")
        if lever_div:
            return lever_div.get_text(" ", strip=True)

    # SmartRecruiters
    if "smartrecruiters.com" in domain:
        sr_div = soup.find("div", class_="job-sections")
        if sr_div:
            return sr_div.get_text(" ", strip=True)

    # BambooHR
    if "bamboohr.com" in domain:
        bh_div = soup.find("div", id="content")
        if bh_div:
            return bh_div.get_text(" ", strip=True)

    # Fallback
    body_text = soup.get_text(" ", strip=True)
    if body_text:
        return body_text

    return ""


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
    You are a recruiting assistant. Read the job description and extract specific, concrete skills.
    Follow these rules:

    - Extract only explicitly mentioned skills (languages, frameworks, libraries, tools, platforms, cloud services, databases, devops, testing, security, data/AI, analytics, ML ops, hardware, embedded, compliance/standards, finance tools, design tools, CRM/ERP, etc.). Include relevant domain/compliance items when present (e.g., HIPAA, PCI-DSS, SOX, GLP, GMP, ISO 26262).
    - Do NOT include vague phrases or soft statements (“modern backend,” “cloud experience,” “strong communication”).
    - Prefer atomic names (“Python”, “React”, “AWS Lambda”, “ISO 27001”). Avoid duplicates.
    - Classify each skill under one of these categories when possible:
        ["Languages","Frameworks","Web","Mobile","Cloud","Databases","DevOps","Data/AI","Testing","Security","Hardware/Embedded","Design/UX","Product/Analytics","Tools","CRM/ERP","Domain/Compliance","Soft Skills"]
    - If a skill does not fit any category above, create a new category name that is concise and professional.
    - Each category should have at most 9 items. If more are found, keep the most role-defining ones.
    - Output VALID JSON only, schema:

    {
    "categories": [
        {"name": "Languages", "skills": ["Python","C++"]},
        {"name": "Cloud", "skills": ["AWS","AWS Lambda","S3"]},
        ...
    ],
    "flat": ["Python","C++","AWS","AWS Lambda","S3", "..."]
    }

    Job Description:
    {{jd_text}}
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set OPENAI_API_KEY in .env")

    client = OpenAI(api_key=api_key)

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"},  # force JSON
        )
        raw = resp.choices[0].message.content.strip()
        return json.loads(raw)

    except Exception as e:
        print("JSON parse failed:", e)
        return {"error": "LLM response parsing failed"}


# ----------- Test -----------
if __name__ == "__main__":
    test_url = "https://allegion.wd5.myworkdayjobs.com/en-US/careers/job/Golden-CO/Summer-Intern---Software-Engineering---Platform-Software_JR33861"
    jd = extract_jd_text(test_url)
    print("First 500 chars:\n", jd[:500])
