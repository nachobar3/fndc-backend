from datetime import datetime, UTC
from typing import List, Optional
from bson import ObjectId
from .database import get_db
from .models import UserCreate, UserUpdate, TournamentCreate, CubeProposalCreate
from .auth import get_password_hash, verify_password
from .models import UserRole, CubeStatus


# User CRUD operations
async def create_user(user: UserCreate) -> dict:
    db = await get_db()
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise ValueError("Email already registered")
    
    now = datetime.now(UTC)
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user.password)
    user_dict["role"] = UserRole.USER
    user_dict["is_verified"] = False
    user_dict["created_at"] = now
    user_dict["updated_at"] = now
    del user_dict["password"]
    
    result = await db.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return user_dict


async def get_user_by_email(email: str) -> Optional[dict]:
    db = await get_db()
    user = await db.users.find_one({"email": email})
    if user:
        user["id"] = str(user["_id"])
        del user["_id"]
    return user


async def get_user_by_id(user_id: str) -> Optional[dict]:
    db = await get_db()
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user["id"] = str(user["_id"])
        del user["_id"]
    return user


async def update_user(user_id: str, user_update: UserUpdate) -> Optional[dict]:
    db = await get_db()
    
    update_data = user_update.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.now(UTC)
        result = await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        if result.modified_count:
            return await get_user_by_id(user_id)
    return None


async def verify_user_email(email: str) -> bool:
    db = await get_db()
    result = await db.users.update_one(
        {"email": email},
        {"$set": {"is_verified": True, "updated_at": datetime.now(UTC)}}
    )
    return result.modified_count > 0


async def update_user_password(email: str, new_password: str) -> bool:
    db = await get_db()
    hashed_password = get_password_hash(new_password)
    result = await db.users.update_one(
        {"email": email},
        {"$set": {"hashed_password": hashed_password, "updated_at": datetime.now(UTC)}}
    )
    return result.modified_count > 0


async def authenticate_user(email: str, password: str) -> Optional[dict]:
    user = await get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


# Tournament CRUD operations
async def create_tournament(tournament: TournamentCreate, admin_id: str) -> dict:
    db = await get_db()
    now = datetime.now(UTC)
    tournament_dict = tournament.dict()
    tournament_dict["created_by"] = admin_id
    tournament_dict["created_at"] = now
    tournament_dict["updated_at"] = now
    
    result = await db.tournaments.insert_one(tournament_dict)
    tournament_dict["id"] = str(result.inserted_id)
    return tournament_dict


async def get_tournaments() -> List[dict]:
    db = await get_db()
    tournaments = await db.tournaments.find().to_list(length=None)
    for tournament in tournaments:
        tournament["id"] = str(tournament["_id"])
        del tournament["_id"]
    return tournaments


async def get_tournament_by_id(tournament_id: str) -> Optional[dict]:
    db = await get_db()
    tournament = await db.tournaments.find_one({"_id": ObjectId(tournament_id)})
    if tournament:
        tournament["id"] = str(tournament["_id"])
        del tournament["_id"]
    return tournament


# Cube Proposal CRUD operations
async def create_cube_proposal(proposal: CubeProposalCreate, user_id: str) -> dict:
    db = await get_db()
    now = datetime.now(UTC)
    proposal_dict = proposal.dict()
    proposal_dict["user_id"] = user_id
    proposal_dict["status"] = CubeStatus.PROPUESTO
    proposal_dict["created_at"] = now
    proposal_dict["updated_at"] = now
    
    result = await db.cube_proposals.insert_one(proposal_dict)
    proposal_dict["id"] = str(result.inserted_id)
    return proposal_dict


async def get_cube_proposals_by_tournament(tournament_id: str) -> List[dict]:
    db = await get_db()
    proposals = await db.cube_proposals.find({"tournament_id": tournament_id}).to_list(length=None)
    for proposal in proposals:
        proposal["id"] = str(proposal["_id"])
        del proposal["_id"]
    return proposals


async def get_enabled_cubes_by_tournament(tournament_id: str) -> List[dict]:
    db = await get_db()
    proposals = await db.cube_proposals.find({
        "tournament_id": tournament_id,
        "status": CubeStatus.HABILITADO
    }).to_list(length=None)
    for proposal in proposals:
        proposal["id"] = str(proposal["_id"])
        del proposal["_id"]
    return proposals


async def update_cube_status(proposal_id: str, status: CubeStatus) -> bool:
    db = await get_db()
    result = await db.cube_proposals.update_one(
        {"_id": ObjectId(proposal_id)},
        {"$set": {"status": status, "updated_at": datetime.now(UTC)}}
    )
    return result.modified_count > 0


# Tournament Registration CRUD operations
async def register_user_to_tournament(tournament_id: str, user_id: str) -> dict:
    db = await get_db()
    
    # Check if user is already registered
    existing_registration = await db.tournament_registrations.find_one({
        "tournament_id": tournament_id,
        "user_id": user_id
    })
    if existing_registration:
        raise ValueError("User already registered for this tournament")
    
    now = datetime.now(UTC)
    registration = {
        "tournament_id": tournament_id,
        "user_id": user_id,
        "registered_at": now
    }
    
    result = await db.tournament_registrations.insert_one(registration)
    registration["id"] = str(result.inserted_id)
    return registration


async def get_tournament_registrations(tournament_id: str) -> List[dict]:
    db = await get_db()
    registrations = await db.tournament_registrations.find({"tournament_id": tournament_id}).to_list(length=None)
    for registration in registrations:
        registration["id"] = str(registration["_id"])
        del registration["_id"]
    return registrations


async def check_user_registration(tournament_id: str, user_id: str) -> bool:
    db = await get_db()
    registration = await db.tournament_registrations.find_one({
        "tournament_id": tournament_id,
        "user_id": user_id
    })
    return registration is not None


# Google Auth CRUD operations
async def get_user_by_google_id(google_id: str) -> Optional[dict]:
    db = await get_db()
    user = await db.users.find_one({"google_id": google_id})
    if user:
        user["id"] = str(user["_id"])
        del user["_id"]
    return user


async def create_google_user(user_info: dict) -> dict:
    db = await get_db()
    
    # Check if user already exists by email
    existing_user = await db.users.find_one({"email": user_info["email"]})
    if existing_user:
        # Update existing user with Google ID if not already set
        if not existing_user.get("google_id"):
            await db.users.update_one(
                {"email": user_info["email"]},
                {"$set": {
                    "google_id": user_info["google_id"],
                    "is_verified": True,  # Google users are pre-verified
                    "updated_at": datetime.now(UTC)
                }}
            )
            existing_user["google_id"] = user_info["google_id"]
            existing_user["is_verified"] = True
        
        existing_user["id"] = str(existing_user["_id"])
        del existing_user["_id"]
        return existing_user
    
    # Create new Google user
    now = datetime.now(UTC)
    user_dict = {
        "email": user_info["email"],
        "name": user_info["name"],
        "google_id": user_info["google_id"],
        "role": UserRole.USER,
        "is_verified": True,  # Google users are pre-verified
        "created_at": now,
        "updated_at": now
    }
    
    # Add picture if available
    if user_info.get("picture"):
        user_dict["picture"] = user_info["picture"]
    
    result = await db.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return user_dict


async def update_user_role(user_id: str, new_role: UserRole) -> bool:
    """Update user role (admin only)"""
    db = await get_db()
    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": new_role, "updated_at": datetime.now(UTC)}}
    )
    return result.modified_count > 0


async def get_all_users() -> List[dict]:
    """Get all users (admin only)"""
    db = await get_db()
    users = await db.users.find().to_list(length=None)
    for user in users:
        user["id"] = str(user["_id"])
        del user["_id"]
        # Remove sensitive information
        if "hashed_password" in user:
            del user["hashed_password"]
    return users 