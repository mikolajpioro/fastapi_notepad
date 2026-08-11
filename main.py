from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload


# model imports-------
import models
from database import Base, engine, get_db
# model imports-------

# schema imports-------
from schemas import NoteBase, NoteCreate, NoteResponse, NoteUpdate
# schema imports-------

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.get("/", include_in_schema=False, name="Home")
@app.get("notes", include_in_schema=False, name="Notes")
def home_page(request: Request, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Note))
    notes = result.scalars().all()

    return templates.TemplateResponse(request, "home.html", {"notes": notes, "title": "Notepad"})

# add single note page
# add single note page
# add single note page