from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Project, User
from ..schemas import ProjectCreate, ProjectUpdate, ProjectResponse
