from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class ProjectCreate(BaseModel):
    brand_name: str
    activity_description: str


class Step2Territory(BaseModel):
    territory: str


class Step3Classes(BaseModel):
    nice_classes: list[int]


class SearchQuery(BaseModel):
    project_id: int


class AssistantPrompt(BaseModel):
    prompt: str
    brand_name: Optional[str] = None


class PaymentRequest(BaseModel):
    project_id: int
    amount_eur: int
