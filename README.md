# Bug Hunt v2

A bug tracking REST API built with FastAPI and PostgreSQL. Users can create project-specific tickets to track bugs, issues, and feature requests.

> **Status:** In active development

## Tech Stack

**Backend:** FastAPI, Python, SQLAlchemy  
**Database:** PostgreSQL  
**Caching:** Redis (planned)  
**Infrastructure:** Docker (planned), AWS (planned)  

## Project Structure

```
bug-hunt-v2/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
```

## Prerequisites

- Python 3.12+
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

# Copy environment variables
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
| PUT | `/api/bugs/:id` | Update a bug |
| DELETE | `/api/bugs/:id` | Delete a bug |

## Roadmap

- [x] Database models and schema
- [x] CRUD API endpoints
- [ ] Authentication
- [ ] Authorization
- [ ] Redis caching
- [ ] Docker containerization
- [ ] AWS deployment

## Changelog

**v2.0** *(In progress)*
Rebuilt as a REST API with FastAPI, PostgreSQL, and SQLAlchemy. Expanded scope includes proper database architecture, API endpoints, and cloud deployment.

**v1.0**
Original capstone project built with Firebase and JavaScript.
[View v1.0](https://github.com/JqJohnny/BugTracker) | [Archived capstone document](https://docs.google.com/document/d/1QBhnF3IqqH9kL8IIt968BQnGg4jEVfZGOBpG-NalNZs/edit?usp=sharing)

## License

MIT License. See [LICENSE](LICENSE) for details.
