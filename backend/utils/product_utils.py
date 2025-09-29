from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import user_model, event_model

def check_admin_permission_for_event(
    db: Session,
    current_user: user_model.User,
    event_id: int
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted: only admins can perform this action"
        )
        
    event = db.query(event_model.Event).filter(event_model.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event Not Found")
    
    if not any(admin.id == current_user.id for admin in event.administrators):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted: you can only manage products of your own events"
        )