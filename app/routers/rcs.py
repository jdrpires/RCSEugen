from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(
    prefix="/v1/rcs",
    tags=["RCS"],
    responses={404: {"description": "Not found"}},
)

@router.post("/send/", response_model=schemas.RcsSendResponse)
async def send_rcs(
    request: schemas.RcsSendRequest,
    account: models.Account = Depends(auth.verify_token),
    db: Session = Depends(get_db)
):
    """
    Send RCS messages using the specified template.
    
    - **accountId**: ID of the account sending the messages
    - **channel**: Channel to use (e.g., "RCS")
    - **channelType**: Type of channel (e.g., "Single", "Basic")
    - **templateId**: ID of the template to use
    - **campaignName**: Optional name for the campaign
    - **campaignId**: Optional ID for the campaign
    - **callbackUrl**: Optional URL for event callbacks
    - **fallback**: Optional fallback configuration if RCS fails
    - **messages**: Array of messages to send with recipient numbers and variables
    """
    
    # Verify account ID matches the authenticated account
    if request.accountId != account.id:
        raise HTTPException(status_code=403, detail="Account ID does not match authenticated account")
    
    # Check if template exists
    template = db.query(models.Template).filter(models.Template.template_id == request.templateId).first()
    if not template:
        raise HTTPException(status_code=404, detail=f"Template with ID {request.templateId} not found")
    
    # Initialize response
    response = schemas.RcsSendResponse(
        **{
            "return.code": 200,
            "return.message": "Messages processed",
            "return.campaignName": request.campaignName,
            "return.campaignId": request.campaignId,
            "return.numberSucesses": 0,
            "return.numberErrors": 0,
            "messages": {
                "successes": [],
                "errors": []
            }
        }
    )
    
    # Process each message
    for msg in request.messages:
        try:
            # Generate a unique callback message ID
            callback_message_id = str(uuid.uuid4())
            
            # Create message record
            db_message = models.Message(
                callback_message_id=callback_message_id,
                account_id=account.id,
                template_id=template.id,
                campaign_name=request.campaignName,
                campaign_id=request.campaignId,
                channel=request.channel,
                channel_type=request.channelType,
                number=msg.number,
                message_text=msg.message,
                variables=msg.vars,
                callback_url=request.callbackUrl,
                schedule_to=msg.scheduleTo,
                status="scheduled" if msg.scheduleTo and msg.scheduleTo > datetime.now() else "pending"
            )
            
            db.add(db_message)
            db.commit()
            db.refresh(db_message)
            
            # Add to success list
            response.messages["successes"].append(
                schemas.MessageSuccess(
                    number=msg.number,
                    callbackMessageId=callback_message_id
                )
            )
            response.return_numberSuccesses += 1
            
        except Exception as e:
            # Add to error list
            response.messages["errors"].append(
                schemas.MessageError(
                    number=msg.number,
                    errorMessage=str(e)
                )
            )
            response.return_numberErrors += 1
    
    # If all messages failed, update return code
    if response.return_numberSuccesses == 0 and response.return_numberErrors > 0:
        response.return_code = 500
        response.return_message = "All messages failed to process"
    # If some messages failed, update return code
    elif response.return_numberErrors > 0:
        response.return_code = 207
        response.return_message = "Some messages failed to process"
    
    return response

@router.get("/events/", response_model=schemas.EventsResponse)
async def get_events(
    limit: int = Query(100, description="Maximum number of events to return"),
    page: int = Query(1, description="Page number"),
    callbackUserId: Optional[List[str]] = Query(None, description="Filter by callback user IDs"),
    account: models.Account = Depends(auth.verify_token),
    db: Session = Depends(get_db)
):
    """
    Get RCS events with optional filtering.
    
    - **limit**: Maximum number of events to return
    - **page**: Page number for pagination
    - **callbackUserId**: Optional list of callback user IDs to filter by
    """
    
    # Calculate offset for pagination
    offset = (page - 1) * limit
    
    # Build query
    query = db.query(models.Event).filter(models.Event.account_id == account.id)
    
    # Apply filters if provided
    if callbackUserId:
        query = query.filter(models.Event.callback_message_id.in_(callbackUserId))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    events = query.offset(offset).limit(limit).all()
    
    # Convert to response schema
    event_list = []
    for event in events:
        template = db.query(models.Template).filter(models.Template.id == event.template_id).first()
        
        event_list.append(schemas.Event(
            eventId=event.event_id,
            callbackMessageId=event.callback_message_id,
            campaignName=event.campaign_name,
            campaignId=event.campaign_id,
            templateId=str(event.template_id),
            templateName=template.name if template else "Unknown",
            accountId=event.account_id,
            channel=event.channel,
            channelType=event.channel_type,
            messageText=event.message_text,
            messageStatus=event.message_status,
            eventType=event.event_type,
            eventValue=event.event_value,
            eventDirection=event.event_direction,
            callbackUrl=event.callback_url,
            scheduleTo=event.schedule_to,
            createdAt=event.created_at,
            updatedAt=event.updated_at,
            timestamp=event.timestamp
        ))
    
    return schemas.EventsResponse(
        events=event_list,
        total=total,
        page=page,
        limit=limit
    )

@router.get("/events/{callback_message_id}", response_model=schemas.EventsResponse)
async def get_event_by_id(
    callback_message_id: str = Path(..., description="Callback message ID to filter by"),
    account: models.Account = Depends(auth.verify_token),
    db: Session = Depends(get_db)
):
    """
    Get RCS events for a specific callback message ID.
    
    - **callback_message_id**: The callback message ID to filter by
    """
    
    # Build query
    query = db.query(models.Event).filter(
        models.Event.account_id == account.id,
        models.Event.callback_message_id == callback_message_id
    )
    
    # Get total count
    total = query.count()
    
    # Get events
    events = query.all()
    
    if not events:
        raise HTTPException(status_code=404, detail=f"No events found for callback message ID: {callback_message_id}")
    
    # Convert to response schema
    event_list = []
    for event in events:
        template = db.query(models.Template).filter(models.Template.id == event.template_id).first()
        
        event_list.append(schemas.Event(
            eventId=event.event_id,
            callbackMessageId=event.callback_message_id,
            campaignName=event.campaign_name,
            campaignId=event.campaign_id,
            templateId=str(event.template_id),
            templateName=template.name if template else "Unknown",
            accountId=event.account_id,
            channel=event.channel,
            channelType=event.channel_type,
            messageText=event.message_text,
            messageStatus=event.message_status,
            eventType=event.event_type,
            eventValue=event.event_value,
            eventDirection=event.event_direction,
            callbackUrl=event.callback_url,
            scheduleTo=event.schedule_to,
            createdAt=event.created_at,
            updatedAt=event.updated_at,
            timestamp=event.timestamp
        ))
    
    return schemas.EventsResponse(
        events=event_list,
        total=total,
        page=1,
        limit=len(events)
    )
