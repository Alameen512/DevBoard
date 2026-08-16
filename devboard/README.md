# DevBoard

A modern, dark-themed **Developer Productivity Dashboard** for tracking projects, tasks, GitHub activity, and daily productivity streaks — built as a full-stack Django portfolio project.

![Status](https://img.shields.io/badge/status-active-brightgreen) ![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![Django](https://img.shields.io/badge/django-4.2-092E20)

---

## Overview

DevBoard is a self-hosted dashboard where a developer can log in and manage everything about their day-to-day work in one place: active projects, a task board, a productivity streak, and a mocked GitHub activity feed (structured so it's a drop-in swap for the real GitHub REST API later).

It's built with a deliberately simple, widely-taught stack — HTML5, CSS3, Bootstrap 5, vanilla JavaScript, Python, Django, and SQLite — so every part of it is easy to read, extend, and explain in an interview.

---

## Features

- **Authentication** — registration, login, logout, password change, all backed by Django's auth system
- **Dashboard** — personalized greeting, current date, productivity summary, current streak, and 4 stat cards (Total Projects, Completed Tasks, Current Streak, GitHub Contributions)
- **Projects** — full CRUD (create, edit, delete) with name, description, technologies, status, progress bar, live task count, GitHub/demo links, and client-side status filtering (All / In Progress / Completed / Planned)
- **Tasks** — full CRUD with priority, status, due date, project linking, instant client-side search + filter, and one-click "mark complete" (which also updates the productivity streak)
- **Activity feed** — auto-logged timeline of what happened (project created, task completed, etc.)
- **GitHub** — profile summary, repo/follower/following counts, recent repos with stars and language — currently mocked, isolated in one function (`get_github_data()`) so it's a one-function swap to the real API
- **Analytics** — weekly productivity bar chart, task status doughnut chart, per-project progress chart, streak stats
- **Profile** — editable avatar, bio, skills, GitHub handle, with public-facing summary card
- **Settings** — dark/light appearance (with live preview), notification preferences, account (username/email) and password change
- **Django Admin** — customized list views, filters, and search for Users, Profiles, Projects, Tasks, and Activities
- **Fully responsive** — collapsible sidebar becomes an off-canvas mobile menu below `992px`, no horizontal scrolling at any breakpoint

---

## Screenshots

> _Add screenshots here once you've run the app locally, e.g.:_
> `screenshots/dashboard.png`, `screenshots/projects.png`, `screenshots/tasks.png`, `screenshots/analytics.png`

---

## Technologies Used

**Frontend**
- HTML5, CSS3 (custom dark theme — no CSS framework overrides beyond Bootstrap's grid/utilities)
- Bootstrap 5.3 (grid, modals, off-canvas sidebar, form controls)
- Bootstrap Icons
- Vanilla JavaScript (no build step, no frameworks) — split into focused files: `script.js`, `charts.js`, `projects.js`, `tasks.js`, `settings.js`
- Chart.js (loaded via CDN) for the weekly productivity, status breakdown, and project progress charts

**Backend**
- Python 3
- Django 4.2 (models, views, forms, URL routing, auth, admin, template inheritance)

**Database**
- SQLite (Django's default — zero setup required)

---

## Project Structure

```
devboard/
│
├── manage.py
├── requirements.txt
├── db.sqlite3                  (created after your first migrate)
│
├── devboard/                   # Project-level config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── dashboard/                  # The one app that powers everything
│   ├── models.py               # Profile, Project, Task, Activity
│   ├── views.py                # All page + CRUD views
│   ├── urls.py                 # App-level routes
│   ├── forms.py                # ModelForms + settings forms
│   ├── admin.py                # Customized Django admin
│   ├── signals.py              # Auto-creates a Profile per new User
│   └── migrations/
│
├── templates/
│   ├── base.html                (shell: sidebar, topbar, auth layout)
│   ├── dashboard.html
│   ├── projects.html
│   ├── tasks.html
│   ├── activity.html
│   ├── github.html
│   ├── analytics.html
│   ├── profile.html
│   ├── settings.html
│   ├── partials/
│   │   ├── _project_fields.html
│   │   └── _task_fields.html
│   └── registration/
│       ├── login.html
│       └── register.html
│
└── static/
    ├── css/
    │   └── style.css            # Dark theme, red/purple gradient accents
    └── js/
        ├── script.js             # Sidebar toggle, shared behaviour
        ├── charts.js              # Chart.js setup (all charts)
        ├── projects.js            # Project status filtering
        ├── tasks.js                # Task search + filtering
        └── settings.js            # Live dark/light preview
```

---

## Installation

### 1. Clone / unzip the project

```bash
cd devboard
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Database Setup

DevBoard uses SQLite, so there's no external database server to install or configure.

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates `db.sqlite3` with all four models: `Profile`, `Project`, `Task`, `Activity` (plus Django's built-in `User`).

### Create an admin account

```bash
python manage.py createsuperuser
```

Follow the prompts, then visit `/admin/` once the server is running to manage all data directly.

---

## Running Locally

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** — you'll land on the login page. Click **Create one** to register a new account (this also auto-creates your `Profile` via a signal), or sign in with the superuser you created above.

Every new account starts empty — add a project or two from the **Projects** page and a few tasks from **Tasks** to see the dashboard stats and charts populate.

---

## Django Admin

Visit `/admin/` and log in with your superuser account to manage:

- **Users** — Django's built-in user admin
- **Profiles** — bio, skills, GitHub handle, streaks, appearance/notification settings
- **Projects** — with inline status/progress filtering and search
- **Tasks** — filterable by status/priority, searchable by title
- **Activities** — read-only audit log of what happened and when

---

## Future Improvements

- Connect the **GitHub** page to the real GitHub REST API (`https://api.github.com/users/<username>`) — `get_github_data()` in `views.py` is already isolated for this swap
- Add drag-and-drop task status changes (Todo → In Progress → Completed) via a small JS + `fetch()` call to a JSON endpoint
- Add project-level task boards (Kanban view) instead of the flat task list
- Email digests using `email_notifications` / `task_reminders` (currently stored but not yet wired to an email backend)
- Pagination for large task/project lists
- REST API layer (Django REST Framework) so DevBoard's data could power a future mobile app
- Automated tests (`pytest-django`) for the CRUD views and streak-calculation logic

---

## Author

Built as a portfolio project demonstrating a full HTML/CSS/Bootstrap/JS frontend wired to a Django + SQLite backend — authentication, CRUD, template inheritance, and a custom-themed admin, all in one deliberately dependency-light stack.

Feel free to fork this, swap in your own branding, and use it as your own productivity dashboard.
