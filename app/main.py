from fastapi import FastAPI
from .database import engine, Base
from .routes import bugs, users, projects

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BugHunt API", description="A bug tracking REST API", version="1.0.0"
)

app.include_router(bugs.router)
app.include_router(users.router)
app.include_router(projects.router)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
