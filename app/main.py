from fastapi import FastAPI

from .database import Base, engine
from .routes import auth, bugs, projects, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BugHunt API", description="A bug tracking REST API", version="1.0.0"
)

app.include_router(auth.router)
app.include_router(bugs.router)
app.include_router(users.router)
app.include_router(projects.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
