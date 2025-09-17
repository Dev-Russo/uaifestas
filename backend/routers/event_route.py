from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from models import event_model
from schemas import event_schema

NOT_FOUND = "Event Not Found"


router = APIRouter()



@router.post("/", response_model=event_schema.Event)
def create_event(event: event_schema.EventCreate, db: Session = Depends(get_db)):
    
    db_event = event_model.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return db_event

@router.get("/", response_model=list[event_schema.Event])
def get_all_events(db: Session = Depends(get_db)):
    event = db.query(event_model.Event).all()
    return event

@router.get("/{id_event}", response_model=event_schema.Event)
def get_event_by_id(id_event: int, db: Session = Depends(get_db)):
    event = db.query(event_model.Event).filter(event_model.Event.id == id_event).first()
    if not event:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return event

@router.put("/{id_event}", response_model=event_schema.Event)
def update_event(id_event: int, event: event_schema.EventBase, db: Session = Depends(get_db)):
    db_event = db.query(event_model.Event).filter(event_model.Event.id == id_event).first()
    
    if not db_event:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    
    if event.name != None:
        db_event.name = event.name
    if event.description != None:
        db_event.description = event.description
    if event.location != None:
        db_event.location = event.location
    if event.date != None:
        db_event.date = event.date
        
    db.commit()
    db.refresh(db_event)
    
    return db_event
        
@router.delete("/{id_event}")
def delete_event(id_event: int, db: Session = Depends(get_db)):
    db_event = db.query(event_model.Event).filter(event_model.Event.id == id_event).first()
    
    if not db_event:
        HTTPException(status_code=404, detail=NOT_FOUND)
    
    db.delete(db_event)
    db.commit()
    
    return {"message": f"Item with {id_event} deleted sucessfully"}