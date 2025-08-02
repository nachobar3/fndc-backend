from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class CubeStatus(str, Enum):
    PROPUESTO = "propuesto"
    HABILITADO = "habilitado"


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    preferred_cube: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    preferred_cube: Optional[str] = None


class User(UserBase):
    id: str
    role: UserRole = UserRole.USER
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime


class UserInDB(User):
    hashed_password: str


class TournamentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    date: datetime
    location: str = Field(..., min_length=1, max_length=200)
    start_time: str = Field(..., description="Time in HH:MM format")
    duration_days: int = Field(..., ge=1, le=30)
    rounds: int = Field(..., ge=1, le=20)


class TournamentCreate(TournamentBase):
    pass


class Tournament(TournamentBase):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime


class CubeProposalBase(BaseModel):
    tournament_id: str
    cube_url: str = Field(..., description="URL from cubecobra.com")
    description: str = Field(..., min_length=1, max_length=500)


class CubeProposalCreate(CubeProposalBase):
    pass


class CubeProposal(CubeProposalBase):
    id: str
    user_id: str
    status: CubeStatus = CubeStatus.PROPUESTO
    created_at: datetime
    updated_at: datetime


class TournamentRegistration(BaseModel):
    id: str
    tournament_id: str
    user_id: str
    registered_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class PasswordReset(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)


class EmailVerification(BaseModel):
    token: str 