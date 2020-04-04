from flask import current_app

from sqlalchemy import (
    Boolean,
    Column,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (
    EmailType,
    PasswordType,
)
from typing_extensions import Final

from apps.common.models import (
    Timestampable,
    UUIDable,
)

MAX_LENGTH: Final[int] = 255


class User(Timestampable, UUIDable):
    email = Column(EmailType, nullable=False, unique=True)
    first_name = Column(String(length=MAX_LENGTH), nullable=False)
    last_name = Column(String(length=MAX_LENGTH), nullable=False)
    username = Column(String(length=MAX_LENGTH), nullable=False)
    password = Column(
        PasswordType(
            max_length=MAX_LENGTH,
            onload=(
                lambda **kwargs: {
                    **kwargs,
                    'schemes': current_app.config['PASSWORD_SCHEMES'],
                }
            ),
        ),
        nullable=False,
        unique=False,
    )
    is_active = Column(Boolean, default=True)

    accepted_help_requests = relationship(
        'apps.help_requests.models.HelpRequest',
        back_populates='accepted_by',
    )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} ({self.email})'
