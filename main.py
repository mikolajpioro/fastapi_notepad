from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException


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
@app.get("/notes", include_in_schema=False, name="Notes")
def home_page(request: Request, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Note))
    notes = result.scalars().all()

    return templates.TemplateResponse(request, "home.html", {"notes": notes, "title": "Notepad"})

@app.get("/notes/{note_id}", include_in_schema=False, name="note_page")
def note_page(request: Request, note_id: int, db: Annotated[Session, Depends(get_db)]):
    result = (db.execute(select(models.Note).where(models.Note.id == note_id)))
    note = result.scalars().first()

    if note:
        title = f"{note.title}"
        return templates.TemplateResponse(request, "note.html", {"note": note, "title": title})
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

@app.get("/api/notes", response_model=list[NoteResponse])
def get_notes(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Note))
    notes = result.scalars().all()
    return notes

@app.get("/api/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Note).where(models.Note.id == note_id))
    note = result.scalars().first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note

@app.post("/api/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, db: Annotated[Session, Depends(get_db)]):
    new_note = models.Note(
        title=note.title,
        content=note.content
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.put("/api/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, updated: NoteUpdate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Note).where(models.Note.id == note_id))
    note = result.scalars().first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not not found"
        )

    note.title = updated.title
    note.content = updated.content

    db.commit()
    db.refresh(note)
    return note

@app.patch("/api/notes/{note_id}", response_model=NoteResponse)
def update_note_partial(note_id: int, updated: NoteUpdate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Note).where(models.Note.id == note_id))
    note = result.scalars().first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    updated_data = updated.model_dump(exclude_unset=True)

    if "title" in updated_data:
        note.title = updated_data["title"]

    if "content" in updated_data:
        note.content = updated_data["content"]

    db.commit()
    db.refresh(note)
    return note

@app.delete("/api/notes/{note_id}", response_model=NoteResponse)
def delete_note(note_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Note).where(models.Note.id == note_id))
    note = result.scalars().first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    db.delete(note)
    db.commit()