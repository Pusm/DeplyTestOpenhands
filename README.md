# FastAPI + Jinja2 Fullstack App

A minimal fullstack web application using FastAPI and Jinja2 templates.

## Features
- API endpoint at `/api/hello`
- Frontend with HTML/JS at `/`
- Static file serving at `/static/`

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn app.main:app --reload
```

3. Open http://localhost:8000 in your browser

## Deployment

### Heroku
1. Create a new Heroku app
2. Set buildpack to `heroku/python`
3. Deploy using Git:
```bash
git push heroku main
```

### Railway
1. Create a new Railway project
2. Connect your Git repository
3. Railway will automatically detect and deploy the app

## Project Structure
```
.
├── app/
│   ├── main.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
├── requirements.txt
├── runtime.txt
├── Procfile
├── .gitignore
└── README.md
```