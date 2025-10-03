from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.auth_utils import get_current_user
from models import user_model
from dependencies import get_db
from models import event_model
from schemas import event_schema, product_schema
from enums import UserRole

NOT_FOUND = "Event Not Found"

router = APIRouter()

@router.post("/", response_model=event_schema.Event)
def create_event(
        event: event_schema.EventCreate,
        db: Session = Depends(get_db),
        current_user: user_model.User = Depends(get_current_user)
    ):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    db_event = event_model.Event(**event.dict())

    db_event.administrators.append(current_user)

    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return db_event

@router.get("/", response_model=list[event_schema.Event])
def get_all_events(db: Session = Depends(get_db)):
    event = db.query(event_model.Event).all()
    return event

@router.get("/my-events", response_model=list[event_schema.Event])
def get_my_events(
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
    ):
    events = db.query(event_model.Event).filter(
        event_model.Event.administrators.any(id=current_user.id)
    ).all()
    return events

@router.get("/{id_event}", response_model=event_schema.Event)
def get_event_by_id(id_event: int, db: Session = Depends(get_db)):
    event = db.query(event_model.Event).filter(event_model.Event.id == id_event).first()
    if not event:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return event

@router.get("/{id_event}/products", response_model=list[product_schema.Product])
def get_products_event(id_event: int, db: Session = Depends(get_db)):
    event = db.query(event_model.Event).filter(event_model.Event.id == id_event).first()
    
    if not event:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return event.products

@router.put("/{id_event}", response_model=event_schema.Event)
def update_event(
    id_event: int,
    event: event_schema.EventBase,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
    ):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Operation not permitted: only admins can update events")
    
    db_event = db.query(event_model.Event).filter(event_model.Event.id == id_event).first()
    
    if not db_event:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    elif all(admin.id != current_user.id for admin in db_event.administrators):
        raise HTTPException(status_code=403, detail="Operation not permitted: you can only update your own events")
    
    if event.name != None:
        db_event.name = event.name
    if event.description != None:
        db_event.description = event.description
    if event.street != None:
        db_event.street = event.street
    if event.created != None:
        db_event.created = event.created
    if event.cep != None:
        db_event.cep = event.cep
    if event.neighborhood != None:
        db_event.neighborhood = event.neighborhood
    if event.number != None:
        db_event.number = event.number
    if event.city != None:
        db_event.city = event.city
    if event.event_date != None:
        db_event.event_date = event.event_date
    if event.image_url != None:
        db_event.image_url = event.image_url
    if event.status != None:
        db_event.status = event.status

    
    db.commit()
    db.refresh(db_event)
    
    return db_event
        
@router.delete("/{id_event}")
def delete_event(
    id_event: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
    ):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Operation not permitted: only admins can delete events")
    
    db_event = db.query(event_model.Event).filter(event_model.Event.id == id_event).first()
    
    if not db_event:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    if all(admin.id != current_user.id for admin in db_event.administrators):
        raise HTTPException(status_code=403, detail="Operation not permitted: you can only update your own events")
    
    db.delete(db_event)
    db.commit()

    return {"message": f"Item with {id_event} deleted successfully"}


"""
Preciso fazer um envio para o email com um end-point que ficara esperando a aceitação do convite,
Assim que o usuario aceitar o convite, ele tera seu role alterado para comissioner e sera adicionado a lista de comissioners do evento
por enquanto vai ficar assim.

Em ambos os Metodos Abaixo.
"""

@router.post("/{id_event}/add_admin/{email_user}", response_model=event_schema.Event)
def add_event_admin(
    id_event: int,
    email_user: str,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    db_event = db.query(event_model.Event).filter(event_model.Event.id == id_event).first()
    if not db_event:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    if current_user not in db_event.administrators:
        raise HTTPException(status_code=403, detail="Operation not permitted: only admins can add event administrators")

    
    new_admin = db.query(user_model.User).filter(user_model.User.email == email_user).first()
    if not new_admin:
        raise HTTPException(status_code=404, detail="User Not Found")

    new_admin.role = UserRole.ADMIN
    if new_admin in db_event.administrators:
        raise HTTPException(status_code=400, detail="User is already an administrator of this event")
    
    db_event.administrators.append(new_admin)
    
    db.commit()
    db.refresh(db_event)

    return db_event


@router.post("/{id_event}/comissioners", response_model=event_schema.Event)
def create_commisioner_for_event(
    id_event: int,
    email_user: str,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    event = db.query(event_model.Event).filter(event_model.Event.id == id_event).first()
    if not event:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    
    if current_user not in event.administratosrs:
        raise HTTPException(status_code=403, detail="Operation not permitted: only event administrators can add comissioners")
    
    new_comissioner = db.query(user_model.User).filter(user_model.User.email == email_user).first()
    if not new_comissioner:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    new_comissioner.role = UserRole.COMMISSIONER
    db_event = db.query(event_model.Event).filter(event_model.Event.id == id_event).first()
    if not db_event:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    db_event.comissioners.append(new_comissioner)

    db.commit()
    db.refresh(db_event)

    return db_event