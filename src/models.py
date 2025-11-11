from dataclasses import dataclass
from datetime import datetime, UTC # Import UTC from datetime
from enum import Enum
from typing import Optional

class FeedbackStatus(Enum):
    PENDING = "Pending"
    IGNORED = "Ignored"
    NEW = "New"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

@dataclass
class Feedback:
    email: str
    message: str
    phone: Optional[str] = None
    id: Optional[int] = None
    status: str = FeedbackStatus.PENDING.value
    metadata: Optional[dict] = None
    created_at: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "message": self.message,
            "status": self.status,
            "metadata": self.metadata,
            "created_at": self.created_at or datetime.now(UTC).isoformat() # Use datetime.now(UTC)
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)