from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, LargeBinary, String
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.extensions import bcrypt, db
from project.time_utils import utc_now


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    _password: Mapped[bytes] = mapped_column(LargeBinary(60), nullable=False)
    authenticated: Mapped[bool] = mapped_column(default=False)
    email_confirmation_sent_on: Mapped[datetime | None]
    email_confirmed: Mapped[bool | None] = mapped_column(default=False)
    email_confirmed_on: Mapped[datetime | None]
    registered_on: Mapped[datetime | None]
    last_logged_in: Mapped[datetime | None]
    current_logged_in: Mapped[datetime | None]
    role: Mapped[str] = mapped_column(String, default='user')
    items: Mapped[list[Item]] = relationship(back_populates='user')

    def __init__(
        self,
        email: str,
        password: str,
        email_confirmation_sent_on: datetime | None = None,
        role: str = 'user',
    ) -> None:
        self.email = email
        self.password = password
        self.authenticated = False
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.registered_on = utc_now()
        self.last_logged_in = None
        self.current_logged_in = utc_now()
        self.role = role

    @hybrid_property
    def password(self) -> bytes:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        self._password = bcrypt.generate_password_hash(password)

    @hybrid_method
    def is_correct_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_email_confirmed(self):
        """Return True if the user confirmed their email address."""
        return self.email_confirmed

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self) -> str:
        """Return the user's ID as a string for Flask-Login."""
        return str(self.id)

    def __repr__(self) -> str:
        return '<User {}>'.format(self.email)


class Item(db.Model):
    __tablename__ = 'items'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str | None]
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User | None] = relationship(back_populates='items')

    def __init__(self, name: str, notes: str | None, user_id: int) -> None:
        self.name = name
        self.notes = notes
        self.user_id = user_id

    def __repr__(self) -> str:
        return '<Item {}>'.format(self.id)
