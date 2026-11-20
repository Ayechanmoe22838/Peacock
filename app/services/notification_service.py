from typing import Optional
from sqlalchemy.orm import Session
import app.models as models

def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    notification_type: str = "info",
    link_url: Optional[str] = None
) -> models.Notification:
    notif = models.Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        link_url=link_url,
        is_read=False
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

def notify_admins(
    db: Session,
    title: str,
    message: str,
    notification_type: str = "info",
    link_url: Optional[str] = None
):
    admins = db.query(models.User).filter(models.User.role == "admin", models.User.is_active == True).all()
    for admin in admins:
        notif = models.Notification(
            user_id=admin.user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            link_url=link_url,
            is_read=False
        )
        db.add(notif)
    db.commit()
