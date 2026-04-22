from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src import models, schemas
from src.dependencies import get_current_user

router = APIRouter(prefix="/notes", tags=["Notes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ➕ CREATE
@router.post("/")
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    new_note = models.Note(
        title=note.title,
        note=note.note,
        owner_id=user_id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

# 📄 READ ALL
@router.get("/")
def get_notes(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return db.query(models.Note).filter(models.Note.owner_id == user_id).all()

# 🔍 READ ONE
@router.get("/{id}")
def get_note(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    note = db.query(models.Note).filter(
        models.Note.id == id,
        models.Note.owner_id == user_id
    ).first()

    if not note:
        raise HTTPException(404, "Note not found")

    return note

# ✏️ UPDATE
@router.put("/{id}")
def update_note(
    id: int,
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    n = db.query(models.Note).filter(
        models.Note.id == id,
        models.Note.owner_id == user_id
    ).first()

    if not n:
        raise HTTPException(404, "Note not found")

    n.title = note.title
    n.note = note.note

    db.commit()
    db.refresh(n)
    return n

# ❌ DELETE
@router.delete("/{id}")
def delete_note(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    n = db.query(models.Note).filter(
        models.Note.id == id,
        models.Note.owner_id == user_id
    ).first()

    if not n:
        raise HTTPException(404, "Note not found")

    db.delete(n)
    db.commit()
    return {"msg": "Deleted successfully"}


@router.get("/")
def get_notes(
    search: str = "",
    isPinned: bool | None = None,
    isArchive: bool | None = None,
    page: int = 1,
    limit: int = 5,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    query = db.query(models.Note).filter(models.Note.owner_id == user_id)

    # 🔍 Search
    if search:
        query = query.filter(models.Note.title.contains(search))

    # 🎯 Filter
    if isPinned is not None:
        query = query.filter(models.Note.isPinned == isPinned)

    if isArchive is not None:
        query = query.filter(models.Note.isArchive == isArchive)

    # 📄 Pagination
    skip = (page - 1) * limit
    notes = query.offset(skip).limit(limit).all()

    return notes



@router.put("/pin/{id}")
def toggle_pin(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == id, models.Note.owner_id == user_id).first()

    if not note:
        raise HTTPException(404, "Not found")

    note.isPinned = not note.isPinned
    db.commit()
    return {"msg": "Pin toggled"}



@router.put("/archive/{id}")
def toggle_archive(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == id, models.Note.owner_id == user_id).first()

    if not note:
        raise HTTPException(404, "Not found")

    note.isArchive = not note.isArchive
    db.commit()
    return {"msg": "Archive toggled"}