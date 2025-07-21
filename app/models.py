from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    account = relationship("Account", back_populates="users")

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    api_key = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    users = relationship("User", back_populates="account")
    messages = relationship("Message", back_populates="account")
    events = relationship("Event", back_populates="account")

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    channel = Column(String)
    channel_type = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    messages = relationship("Message", back_populates="template")
    events = relationship("Event", back_populates="template")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    callback_message_id = Column(String, unique=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    template_id = Column(Integer, ForeignKey("templates.id"))
    campaign_name = Column(String, nullable=True)
    campaign_id = Column(String, nullable=True)
    channel = Column(String)
    channel_type = Column(String)
    number = Column(String)
    message_text = Column(Text, nullable=True)
    variables = Column(JSON, nullable=True)
    callback_url = Column(String, nullable=True)
    schedule_to = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="scheduled")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    account = relationship("Account", back_populates="messages")
    template = relationship("Template", back_populates="messages")
    events = relationship("Event", back_populates="message")
    
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True)
    callback_message_id = Column(String, ForeignKey("messages.callback_message_id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))
    template_id = Column(Integer, ForeignKey("templates.id"))
    campaign_name = Column(String, nullable=True)
    campaign_id = Column(String, nullable=True)
    channel = Column(String)
    channel_type = Column(String)
    message_text = Column(Text, nullable=True)
    message_status = Column(String)
    event_type = Column(String)
    event_value = Column(String, nullable=True)
    event_direction = Column(String)
    callback_url = Column(String, nullable=True)
    schedule_to = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    account = relationship("Account", back_populates="events")
    template = relationship("Template", back_populates="events")
    message = relationship("Message", back_populates="events")
