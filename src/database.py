"""
Database module for persisting tournament sessions
"""

import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Session(Base):
    """Database model for monitoring sessions"""

    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    url = Column(String, nullable=False)
    config = Column(Text, nullable=False)  # JSON string
    status = Column(String, default="starting")
    created_at = Column(DateTime, default=datetime.now)
    last_update = Column(DateTime, nullable=True)
    data = Column(Text, nullable=True)  # JSON string
    error = Column(String, nullable=True)


class Database:
    """Database connection handler"""

    def __init__(self, database_url=None):
        """Initialize database connection"""
        if database_url is None:
            # Try to get from environment, fallback to SQLite for local dev
            database_url = os.environ.get("DATABASE_URL", "sqlite:///sessions.db")

        # Fix postgres:// to postgresql:// for SQLAlchemy
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)

        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Get a database session"""
        return self.SessionLocal()

    def create_session(self, session_id, url, config):
        """Create a new monitoring session"""
        db = self.get_session()
        try:
            session = Session(
                id=session_id,
                url=url,
                config=json.dumps(config),
                status="starting",
                created_at=datetime.now(),
            )
            db.add(session)
            db.commit()
            return session
        finally:
            db.close()

    def get_all_sessions(self):
        """Get all active sessions"""
        db = self.get_session()
        try:
            sessions = db.query(Session).all()
            return [
                {
                    "id": s.id,
                    "url": s.url,
                    "config": json.loads(s.config),
                    "status": s.status,
                    "created_at": s.created_at,
                    "last_update": s.last_update,
                    "data": json.loads(s.data) if s.data else None,
                    "error": s.error,
                }
                for s in sessions
            ]
        finally:
            db.close()

    def get_session_by_id(self, session_id):
        """Get a specific session"""
        db = self.get_session()
        try:
            session = db.query(Session).filter(Session.id == session_id).first()
            if not session:
                return None
            return {
                "id": session.id,
                "url": session.url,
                "config": json.loads(session.config),
                "status": session.status,
                "created_at": session.created_at,
                "last_update": session.last_update,
                "data": json.loads(session.data) if session.data else None,
                "error": session.error,
            }
        finally:
            db.close()

    def update_session(self, session_id, **kwargs):
        """Update a session"""
        db = self.get_session()
        try:
            session = db.query(Session).filter(Session.id == session_id).first()
            if not session:
                return False

            for key, value in kwargs.items():
                if key == "data" and value is not None:
                    value = json.dumps(value)
                elif key == "config" and value is not None:
                    value = json.dumps(value)
                setattr(session, key, value)

            db.commit()
            return True
        finally:
            db.close()

    def delete_session(self, session_id):
        """Delete a session"""
        db = self.get_session()
        try:
            session = db.query(Session).filter(Session.id == session_id).first()
            if session:
                db.delete(session)
                db.commit()
                return True
            return False
        finally:
            db.close()
