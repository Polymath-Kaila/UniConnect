# UniConnect Backend (Django + DRF + JWT)

## Quickstart
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Highlights
- Custom User (required `university`, role student/teacher, auto mentor for students)
- Courses & Enrollments (teachers create; students enroll), teacher can update `progress` (0-100)
- Groups → Projects (with `repo_url`) → Tasks
- Simple connections
