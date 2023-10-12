
# Creative Todo

Creative Todo is an intuitive task management app designed for individual and team productivity. Seamlessly authenticate with `Single Sign-On (SSO)`, `create projects`, `add tasks`, and efficiently manage your `projects` and `tasks` with ease. Stay organized, prioritize, and track progress effortlessly. Elevate your task management experience with Creative Todo  app.

## Local Build & Deployment

To build and deploy this project, you will need install the latest [python](https://www.python.org/downloads/) and [PostgreSQL](https://www.postgresql.org/download/) version for your OS, start [postgres server](https://www.postgresql.org/docs/current/server-start.html) and then run the following commands

```bash

#! Clone Project
git clone https://github.com/PromasterGuru/todolist-api.git
#! Switch to todolist-api project directory
cd todolist-api/
#! Install/upgrade package installer for Python (PIP)
python -m pip install --user --upgrade pip
#! Install virtualenv, a tool to create isolated Python environments
python -m pip install --user virtualenv
#! Create project virtual environment
python -m venv env
#! Activate virtual environment
source env/bin/activate
#! Install project dependencies
pip install -r requirements.txt
#! Run project migrations
 python manage.py migrate
#! Start django development server
 python manage.py runserver
```



## Badges

![Workflow](https://github.com/github/docs/actions/workflows/django.yml/badge.svg?event=push) [![Test Coverage](https://api.codeclimate.com/v1/badges/b2d1279d85184f3debab/test_coverage)](https://codeclimate.com/github/PromasterGuru/todolist-api/test_coverage) [![Maintainability](https://api.codeclimate.com/v1/badges/b2d1279d85184f3debab/maintainability)](https://codeclimate.com/github/PromasterGuru/todolist-api/maintainability) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
