# BugHunt v2

A bug tracking REST API built with FastAPI and PostgreSQL. Users can create project-specific tickets to track bugs, issues, and feature requests.

> **Status:** In active development

## Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy  
**Database:** PostgreSQL  
**Infrastructure:** Docker (planned), AWS (planned)  

## Project Structure

```
bug-tracker-v2/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/
│       ├── bugs.py
│       ├── users.py
│       └── projects.py
├── .env
├── .gitignore
└── requirements.txt
```

## Prerequisites

- Python 3.14+
- PostgreSQL

## Getting Started

```bash
# Clone the repo
git clone https://github.com/JqJohnny/bug-tracker-v2

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment variables and fill in your values
cp .env.example .env

# Run the server
uvicorn app.main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/bugs` | Get all bugs |
| POST | `/api/bugs` | Create a bug |
| PATCH | `/api/bugs/{id}` | Update a bug |
| DELETE | `/api/bugs/{id}` | Delete a bug |
| GET | `/api/users` | Get all users |
| POST | `/api/users` | Create a user |
| GET | `/api/users/{id}` | Get a user |
| DELETE | `/api/users/{id}` | Delete a user |
| GET | `/api/projects` | Get all projects |
| POST | `/api/projects` | Create a project |
| PATCH | `/api/projects/{id}` | Update a project |
| DELETE | `/api/projects/{id}` | Delete a project |
| POST | `/api/projects/{id}/contributors/{user_id}` | Add contributor |
| DELETE | `/api/projects/{id}/contributors/{user_id}` | Remove contributor |

## Roadmap

- [x] Database models and schema
- [x] CRUD API endpoints
- [x] Bug filtering
- [x] Project contributor management
- [ ] Authentication (email/password)
- [ ] Google OAuth
- [ ] Docker containerization
- [ ] CI/CD (GitHub Actions)
- [ ] AWS deployment

## Changelog

**v2.0** *(In progress)*  
Rebuilt as a REST API with FastAPI, PostgreSQL, and SQLAlchemy. Expanded scope includes relational database architecture, RESTful endpoints, and planned cloud deployment.

**v1.0**  
Original capstone project built with Firebase and JavaScript.  
[View v1.0](https://github.com/JqJohnny/BugTracker) | [Archived capstone document](https://docs.google.com/document/d/1QBhnF3IqqH9kL8IIt968BQnGg4jEVfZGOBpG-NalNZs/edit?usp=sharing)

## License

MIT License. See [LICENSE](LICENSE) for details.
