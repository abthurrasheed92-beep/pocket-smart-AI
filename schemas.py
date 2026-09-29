from typing import List, Optional

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class HomeRequest(BaseModel):
    budget: float = Field(gt=0)
    room_type: str
    style: str
    items: List[str] = []
    notes: Optional[str] = None


class PartyRequest(BaseModel):
    budget: float = Field(gt=0)
    guests: int = Field(gt=0)
    event_type: str
    venue: str
    city: str
    preferences: Optional[str] = None


class JewelryRequest(BaseModel):
    budget: float = Field(gt=0)
    occasion: str
    style: str
    outfit_color: str
    notes: Optional[str] = None


class RecommendationItem(BaseModel):
    category: str
    name: str
    reason: str
    estimated_price: float
    search_url: Optional[str] = None
    platform: Optional[str] = None


class RecommendationResponse(BaseModel):
    source: str
    summary: str
    budget: float
    budget_used: float
    recommendations: List[RecommendationItem]