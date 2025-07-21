from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Optional, Any, Union
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    account_id: int

class UserResponse(UserBase):
    id: int
    account_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime

class TokenData(BaseModel):
    username: Optional[str] = None
    account_id: Optional[int] = None

# Login schema
class UserLogin(BaseModel):
    username: str
    password: str

# Base schemas
class MessageBase(BaseModel):
    number: str
    message: Optional[str] = None
    vars: Optional[Dict[str, Any]] = None
    scheduleTo: Optional[datetime] = None

class FallbackBase(BaseModel):
    channel: str
    message: str

# Request schemas
class RcsSendRequest(BaseModel):
    accountId: int
    channel: str
    channelType: str
    templateId: str
    campaignName: Optional[str] = None
    campaignId: Optional[str] = None
    callbackUrl: Optional[str] = None
    fallback: Optional[List[FallbackBase]] = None
    messages: List[MessageBase]

class EventsQueryParams(BaseModel):
    limit: Optional[int] = 100
    page: Optional[int] = 1
    callbackUserId: Optional[List[str]] = None

# Response schemas
class MessageSuccess(BaseModel):
    number: str
    callbackMessageId: str

class MessageError(BaseModel):
    number: str
    errorMessage: str

class RcsSendResponse(BaseModel):
    return_code: int = Field(..., alias="return.code")
    return_message: str = Field(..., alias="return.message")
    return_campaignName: Optional[str] = Field(None, alias="return.campaignName")
    return_campaignId: Optional[str] = Field(None, alias="return.campaignId")
    return_numberSuccesses: int = Field(..., alias="return.numberSucesses")
    return_numberErrors: int = Field(..., alias="return.numberErrors")
    messages: Dict[str, List[Union[MessageSuccess, MessageError]]] = {
        "successes": [],
        "errors": []
    }

    class Config:
        populate_by_name = True

class Event(BaseModel):
    eventId: str
    callbackMessageId: str
    campaignName: Optional[str] = None
    campaignId: Optional[str] = None
    templateId: str
    templateName: str
    accountId: int
    channel: str
    channelType: str
    messageText: Optional[str] = None
    messageStatus: str
    eventType: str
    eventValue: Optional[str] = None
    eventDirection: str
    callbackUrl: Optional[str] = None
    scheduleTo: Optional[datetime] = None
    createdAt: datetime
    updatedAt: Optional[datetime] = None
    timestamp: datetime

class EventsResponse(BaseModel):
    events: List[Event]
    total: int
    page: int
    limit: int
