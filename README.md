# UniConnect v2 — Everyone can learn these skills

Full-stack MVP: Django REST backend + React (Vite) frontend.
- Required University selection on signup (API + DB)
- Auto-mentor assignment for students
- Courses & Enrollments; teacher can update progress (0–100)
- Groups & Projects with Repo URL
- PWA (installable), responsive UI
- Dockerized backend & frontend, docker-compose, Render blueprint

## Dev quickstart
### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
echo 'VITE_API_BASE=http://localhost:8000/api' > .env
npm run dev
```

## Deploy
- Render: use `render.yaml`
- VPS: `docker compose up -d --build`
- Frontend static (Netlify/Vercel): set `VITE_API_BASE` to your backend URL

© UniConnect — Made in Kenya
