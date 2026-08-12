# BugHunt v2

A bug tracking REST API built with FastAPI and PostgreSQL. Users can create project-specific tickets to track bugs, issues, and feature requests.

> **Status:** In active development

## Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy  
**Database:** PostgreSQL  
**Infrastructure:** Docker, AWS (planned)  

## Project Structure

bug-tracker-v2/
├── alembic/
│ └── versions/
├── app/
│ ├── auth.py
│ ├── database.py
│ ├── main.py
│ ├── models.py
│ ├── schemas.py
│ └── routes/
│ ├── auth.py
│ ├── bugs.py
│ ├── projects.py
│ └── users.py
├── tests/
│ ├── conftest.py
│ └── test_bugs.py
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
└── requirements.txt


## Prerequisites

- Docker
- Docker Compose

## Getting Started

```bash
# Clone the repo
git clone https://github.com/JqJohnny/bug-tracker-v2

# Copy environment variables and fill in your values
cp .env.example .env

# Build and start the containers
docker-compose up --build

# Run database migrations (in a separate terminal)
$env:DB_HOST="localhost"; alembic upgrade head
```

The API will be available at `http://localhost:8000`.  
Interactive docs at `http://localhost:8000/docs`.

## Running Tests

```bash
# Make sure Docker is running first
docker-compose up -d

# Run the test suite
pytest tests/ -v
```

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register with email and password |
| POST | `/api/auth/login` | Login and receive a JWT token |
| GET | `/api/auth/google/login` | Begin Google OAuth flow |
| GET | `/api/auth/google/callback` | Google OAuth callback |

### Bugs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bugs` | Get all bugs (filterable by status, priority, assignee) |
| POST | `/api/bugs` | Create a bug |
| GET | `/api/bugs/{id}` | Get a bug |
| PATCH | `/api/bugs/{id}` | Update a bug (author or assignee only) |
| DELETE | `/api/bugs/{id}` | Delete a bug (author only) |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Get all users |
| GET | `/api/users/{id}` | Get a user |
| DELETE | `/api/users/{id}` | Delete your own account |

### Projects
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects` | Get all projects |
| POST | `/api/projects` | Create a project |
| GET | `/api/projects/{id}` | Get a project |
| PATCH | `/api/projects/{id}` | Update a project (owner only) |
| DELETE | `/api/projects/{id}` | Delete a project (owner only) |
| POST | `/api/projects/{id}/contributors/{user_id}` | Add contributor (owner only) |
| DELETE | `/api/projects/{id}/contributors/{user_id}` | Remove contributor (owner only) |

## Environment Variables
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=
DB_NAME=bughunt
DB_PORT=5433
SECRET_KEY=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
TEST_DATABASE_URL=postgresql://postgres:@localhost:5434/bughunt_test


## Roadmap

- [x] Database models and schema
- [x] CRUD API endpoints
- [x] Bug filtering (status, priority, assignee)
- [x] Project contributor management
- [x] JWT authentication (email/password)
- [x] Google OAuth
- [x] Docker containerization
- [x] Automated test suite (pytest)
- [ ] CI/CD (GitHub Actions)
- [ ] AWS deployment

## Changelog

**v2.0** *(In progress)*  
Rebuilt as a REST API with FastAPI, PostgreSQL, and SQLAlchemy. Expanded scope includes relational database architecture, RESTful endpoints, JWT authentication, Google OAuth, Docker containerization, and an automated test suite.

**v1.0**  
Original capstone project built with Firebase and JavaScript.  
[View v1.0](https://github.com/JqJohnny/BugTracker) | [Archived capstone document](https://docs.google.com/document/d/1QBhnF3IqqH9kL8IIt968BQnGg4jEVfZGOBpG-NalNZs/edit?usp=sharing)

## License

MIT License. See [LICENSE](LICENSE) for details.