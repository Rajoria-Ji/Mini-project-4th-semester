from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from textblob import TextBlob
from typing import List, Optional
import os

app = FastAPI(title="Email Intelligence API")

# Database Setup
DB_PATH = os.getenv("DB_PATH", "sqlite:///./emails.db")
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class EmailDB(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text, nullable=False)
    category = Column(String(50), nullable=True) # Intent
    sentiment = Column(String(50), nullable=True)
    status = Column(String(50), default="pending") # pending, sent
    draft_response = Column(Text, nullable=True)

Base.metadata.create_all(bind=engine)

# Pydantic Models
class EmailIngest(BaseModel):
    body: str

class EmailResponse(BaseModel):
    id: int
    body: str
    category: Optional[str]
    sentiment: Optional[str]
    status: str
    draft_response: Optional[str]

    class Config:
        from_attributes = True

class SendDraftRequest(BaseModel):
    draft_response: str

# NLP Logic
def analyze_email(body: str) -> dict:
    blob = TextBlob(body)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
        
    body_lower = body.lower()
    
    # Intent categorization rule-based
    if "refund" in body_lower or "money back" in body_lower or "cancel" in body_lower:
        category = "Refund"
        draft = f"Dear Customer,\n\nWe apologize for the inconvenience. We have received your request regarding a refund. Our billing team will process it within 3-5 business days.\n\nBest,\nSupport Team"
    elif "broken" in body_lower or "error" in body_lower or "not working" in body_lower or "issue" in body_lower:
        category = "Technical Support"
        draft = f"Dear Customer,\n\nThank you for reaching out. We're sorry you're experiencing technical difficulties. Our tech team is looking into the issue and will get back to you shortly.\n\nBest,\nTech Support"
    else:
        category = "General Inquiry"
        draft = f"Dear Customer,\n\nThank you for your message. An agent will review your inquiry and get back to you within 24 hours.\n\nBest,\nCustomer Service"
    
    return {
        "sentiment": sentiment,
        "category": category,
        "draft_response": draft
    }

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CORS for frontend
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints
@app.post("/ingest", response_model=EmailResponse)
def ingest_email(email_in: EmailIngest, db: Session = Depends(get_db)):
    analysis = analyze_email(email_in.body)
    new_email = EmailDB(
        body=email_in.body,
        category=analysis["category"],
        sentiment=analysis["sentiment"],
        draft_response=analysis["draft_response"],
        status="pending"
    )
    db.add(new_email)
    db.commit()
    db.refresh(new_email)
    return new_email

@app.get("/emails", response_model=List[EmailResponse])
def get_emails(db: Session = Depends(get_db)):
    return db.query(EmailDB).order_by(EmailDB.id.desc()).all()

@app.put("/emails/{email_id}/send", response_model=EmailResponse)
def send_email(email_id: int, req: SendDraftRequest, db: Session = Depends(get_db)):
    db_email = db.query(EmailDB).filter(EmailDB.id == email_id).first()
    if not db_email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    db_email.draft_response = req.draft_response
    db_email.status = "sent"
    db.commit()
    db.refresh(db_email)
    return db_email

@app.delete("/emails/{email_id}", response_model=dict)
def delete_email(email_id: int, db: Session = Depends(get_db)):
    db_email = db.query(EmailDB).filter(EmailDB.id == email_id).first()
    if not db_email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    db.delete(db_email)
    db.commit()
    return {"status": "success", "message": "Email deleted"}
