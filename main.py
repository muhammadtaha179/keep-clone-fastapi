from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Note
from app.schemas import NoteCreate, NoteResponse
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List


app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/notes", response_model=NoteResponse)
def create_note(note: NoteCreate, db:Session = Depends(get_db)):
    note_db = Note(title = note.title, content = note.content)
    db.add(note_db)
    db.commit()
    db.refresh(note_db)
    return note_db
@app.get("/notes", response_model=List[NoteResponse])
def get_all_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    return notes

@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note:NoteCreate, db: Session = Depends(get_db) ):
    db_note = db.query(Note).filter(Note.id==note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Not found")
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note
@app.delete("/notes/{note_id}")
def delete_note(note_id:int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}




