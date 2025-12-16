# Job Application Manager

![Docker](https://img.shields.io/badge/Docker-dev%20env-2496ED)
![React](https://img.shields.io/badge/React-frontend-green)
![JavaScript](https://img.shields.io/badge/JavaScript-frontend-green)
![Django](https://img.shields.io/badge/Django-backend-blue)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![black](https://img.shields.io/badge/code%20style-black-000000)

*A Smart Application Tracking & Skill Recommendation Platform*

## Introduction  
Our **Job Application Manager** is a full-stack web platform that helps users organize their job search and application process. Job seekers often lose track of deadlines, stages, and required skill requirements across many platforms. Our application allows users to:

- Track various applications on a centralized dashboard
- Get suggestions by AI on skills to practice
- Get recommended LeetCode problems from job position applied to
- Upload profile & resume
- Chat with AI to get further suggestions

There are some existing application similar to our application such as LeetCode and Simplify. But they rather focus on one part of the application process (tracker, practice questions, etc.) while our application integrate them together. Moreover, compared with existing spreadsheets or job-tracking tools, our system is **smarter** and **more personalized**: the AI analyzes job descriptions and the user's background to recommend specific skills and practice problems—reducing stress and improving preparation efficiency.

Motivation: Searching for jobs is overwhelming. We wanted to build a tool that *we ourselves would use*—a platform combining tracking, organization, and personalized learning guidance.

---

## Technical Architecture

### System Overview

<p align="center">
  <img src="assets/architecture.png" width="60%">
</p>

### Frontend
**Functionalities**: Displays UI, Manages application list and forms, Handles login and profile pages

**Interaction**: Sends requests to backend via HTTP (REST API) such as create, update, read. Get the JSON response from backend

**Language/Library**: React, Vite, Javascript, CSS

### Backend
**Functionalities**: Authentication, CRUD for applications, Resume upload handling

**Interaction**: Get HTTP request from frontend and send response in JSON; Use Django ORM to communicate with SQLite Database; Send prompt to AI via OpenAI API to get response

**Language/Library**: Django, Python

### AI
**Functionalities**: Extracts keywords from job description, Calls OpenAI API for skill suggestions, Returns recommended skills and LeetCode topics

**Interaction**: Get Job Description and Prompt from backend via OpenAI API

**Language/Library**: OpenAI, Python

### Database
**Functionalities**: Stores user accounts, Stores job application info, Stores LeetCode problem info

**Interaction**: The backend performs CRUD operations using Django ORM

**Language/Library**: SQLite, Django ORM

## Installation Instruction

### 1. Clone the repository
```bash
git clone https://github.com/CS222-UIUC/Job-Application-Manager.git
cd Job-Application-Manager
```

### 2. Setup environment variable
```bash
cp .env.example .env
# Edit .env and fill in your own values (e.g. OPENAI_API_KEY)
```

### 3. Setup using docker
```bash
docker-compose up --build
```

Now you should be able to use the app (see step 4).

If it doesn't work, you may need to setup the database for the first time
```bash
# In another terminal:
# setup database
# - migrate
docker compose exec backend python manage.py migrate
# - upload the first 3758 leetcode problems
docker compose exec backend python manage.py get_leetcode_problem
```

You can check if both backend and frontend are running using the command
```bash
docker-compose ps
```

Also, if you want to manage the backend database, you may need to create superuser.
```bash
# create superuser by this command, following the instruction
docker compose exec backend createsuperuser
```

### 4. Using the website
Now you should be able to use the frontend website at http://localhost:5173/

And the backend database at http://localhost:8000/admin/ (using your own account)

## Members

| Name             | Github | Role                     | Responsibilities                                                |
| ---------------- | -------------- | ------------------------ | --------------------------------------------------------------- |
| **Zhijian Yang** | [<img src="https://github.com/yangzhijiany.png" width="40"/>](https://github.com/yangzhijiany) | Full-stack + Integration | Connect React & Django, assist backend, deployment, using API   |
| **William Lu**   | [<img src="https://github.com/William-f-12.png" width="40"/>](https://github.com/William-f-12) | Backend                  | Models, authentication, AI recommendation, leetcode             |
| **Liyuan Lu**    | [<img src="https://github.com/LiyuanLu0529.png" width="40"/>](https://github.com/LiyuanLu0529) | Backend                  | Resume upload, REST API endpoints, database schema              |
| **Yantao Lin**   | [<img src="https://github.com/ytLin27.png" width="40"/>](https://github.com/ytLin27) | Frontend                 | UI components, dashboard, forms, login page                     |
