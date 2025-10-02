import enum

class EventStatus(str, enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class SaleStatus(str, enum.Enum):
    PAID = "PAGO"
    CANCELED = "CANCELADO"
    
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    COMMISSIONER = "commissioner"