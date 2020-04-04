from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PhoneNumberType
from typing_extensions import Final

from apps.common.models import (
    Timestampable,
    UUIDable,
)

MAX_LENGTH: Final[int] = 255


class HelpRequest(Timestampable, UUIDable):
    first_name = Column(String(length=MAX_LENGTH), nullable=False)
    last_name = Column(String(length=MAX_LENGTH), nullable=False)
    phone_number = Column(PhoneNumberType(region='PL', max_length=MAX_LENGTH))
    address = Column(String(length=MAX_LENGTH), nullable=False)
    things = Column(String(length=(MAX_LENGTH * 4)), nullable=False)
    finished_at = Column(DateTime, default=None, nullable=True)
    accepted_at = Column(DateTime, default=None, nullable=True)

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
