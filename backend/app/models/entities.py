from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_google: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    projects: Mapped[list['Project']] = relationship(back_populates='user', cascade='all, delete-orphan')


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    brand_name: Mapped[str] = mapped_column(String(255))
    logo_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    activity_description: Mapped[str] = mapped_column(Text)
    territory: Mapped[str] = mapped_column(String(64), default='FRANCE')
    nice_classes: Mapped[str] = mapped_column(String(255), default='')
    status: Mapped[str] = mapped_column(String(64), default='draft')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates='projects')
    results: Mapped[list['SearchResult']] = relationship(back_populates='project', cascade='all, delete-orphan')


class SearchResult(Base):
    __tablename__ = 'search_results'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))
    candidate_name: Mapped[str] = mapped_column(String(255))
    source: Mapped[str] = mapped_column(String(64))
    score: Mapped[float] = mapped_column(Float)
    risk_level: Mapped[str] = mapped_column(String(16))

    project: Mapped[Project] = relationship(back_populates='results')


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token: Mapped[str] = mapped_column(String(512), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
