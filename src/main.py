from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas

router = APIRouter(prefix="/notes", tags=["Notes"])

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ➕ Create Note
@router.post("/")
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    new_note = models.Note(**note.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

# 📄 Get Notes
@router.get("/")
def get_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()

# ✏️ Update
@router.put("/{id}")
def update_note(id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    n = db.query(models.Note).filter(models.Note.id == id).first()
    n.title = note.title
    n.note = note.note
    db.commit()
    return n

# ❌ Delete
@router.delete("/{id}")
def delete_note(id: int, db: Session = Depends(get_db)):
    n = db.query(models.Note).filter(models.Note.id == id).first()
    db.delete(n)
    db.commit()
    return {"msg": "Deleted"}