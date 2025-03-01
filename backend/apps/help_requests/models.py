from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing_extensions import Final

from apps.common.models import (
    Timestampable,
    UUIDable,
)

MAX_LENGTH: Final[int] = 255


class HelpRequest(Timestampable, UUIDable):
    full_name = Column(String(length=MAX_LENGTH), nullable=False)
    phone_number = Column(String(length=MAX_LENGTH), nullable=False)
    address = Column(String(length=MAX_LENGTH), nullable=False)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    products = Column(Text, nullable=False)
    pickup_time = Column(String(length=MAX_LENGTH), nullable=False)
    call_time = Column(String(length=MAX_LENGTH), nullable=False)
    finished_at = Column(DateTime, default=None, nullable=True)
    accepted_at = Column(DateTime, default=None, nullable=True)
    recording_url = Column(String(length=MAX_LENGTH), nullable=True)

    accepted_by_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users_user.id'),
        nullable=True,
    )
    accepted_by = relationship(
        'apps.users.models.User',
        back_populates='accepted_help_requests',
        lazy='joined',
    )
