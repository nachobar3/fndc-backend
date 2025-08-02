from datetime import datetime, UTC
from typing import List, Optional
from bson import ObjectId
from .database import get_database
from .models import UserCreate, UserUpdate, TournamentCreate, CubeProposalCreate
from .auth import get_password_hash, verify_password
from .models import UserRole, CubeStatus


# User CRUD operations
async def create_user(user: UserCreate) -> dict:
    db = await get_database()
    
    # Check if user already exists
    existing_user = await db.fndc.users.find_one({"email": user.email})
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
    
    result = await db.fndc.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return user_dict


async def get_user_by_email(email: str) -> Optional[dict]:
    db = await get_database()
    user = await db.fndc.users.find_one({"email": email})
    if user:
        user["id"] = str(user["_id"])
        del user["_id"]
    return user


async def get_user_by_id(user_id: str) -> Optional[dict]:
    db = await get_database()
    user = await db.fndc.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user["id"] = str(user["_id"])
        del user["_id"]
    return user


async def update_user(user_id: str, user_update: UserUpdate) -> Optional[dict]:
    db = await get_database()
    
    update_data = user_update.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.now(UTC)
        result = await db.fndc.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        if result.modified_count:
            return await get_user_by_id(user_id)
    return None


async def verify_user_email(email: str) -> bool:
    db = await get_database()
    result = await db.fndc.users.update_one(
        {"email": email},
        {"$set": {"is_verified": True, "updated_at": datetime.now(UTC)}}
    )
    return result.modified_count > 0


async def update_user_password(email: str, new_password: str) -> bool:
    db = await get_database()
    hashed_password = get_password_hash(new_password)
    result = await db.fndc.users.update_one(
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
    db = await get_database()
    now = datetime.now(UTC)
    tournament_dict = tournament.dict()
    tournament_dict["created_by"] = admin_id
    tournament_dict["created_at"] = now
    tournament_dict["updated_at"] = now
    
    result = await db.fndc.tournaments.insert_one(tournament_dict)
    tournament_dict["id"] = str(result.inserted_id)
    return tournament_dict


async def get_tournaments() -> List[dict]:
    db = await get_database()
    tournaments = await db.fndc.tournaments.find().to_list(length=None)
    for tournament in tournaments:
        tournament["id"] = str(tournament["_id"])
        del tournament["_id"]
    return tournaments


async def get_tournament_by_id(tournament_id: str) -> Optional[dict]:
    db = await get_database()
    tournament = await db.fndc.tournaments.find_one({"_id": ObjectId(tournament_id)})
    if tournament:
        tournament["id"] = str(tournament["_id"])
        del tournament["_id"]
    return tournament


# Cube Proposal CRUD operations
async def create_cube_proposal(proposal: CubeProposalCreate, user_id: str) -> dict:
    db = await get_database()
    now = datetime.now(UTC)
    proposal_dict = proposal.dict()
    proposal_dict["user_id"] = user_id
    proposal_dict["status"] = CubeStatus.PROPUESTO
    proposal_dict["created_at"] = now
    proposal_dict["updated_at"] = now
    
    result = await db.fndc.cube_proposals.insert_one(proposal_dict)
    proposal_dict["id"] = str(result.inserted_id)
    return proposal_dict


async def get_cube_proposals_by_tournament(tournament_id: str) -> List[dict]:
    db = await get_database()
    proposals = await db.fndc.cube_proposals.find({"tournament_id": tournament_id}).to_list(length=None)
    for proposal in proposals:
        proposal["id"] = str(proposal["_id"])
        del proposal["_id"]
    return proposals


async def get_enabled_cubes_by_tournament(tournament_id: str) -> List[dict]:
    db = await get_database()
    proposals = await db.fndc.cube_proposals.find({
        "tournament_id": tournament_id,
        "status": CubeStatus.HABILITADO
    }).to_list(length=None)
    for proposal in proposals:
        proposal["id"] = str(proposal["_id"])
        del proposal["_id"]
    return proposals


async def update_cube_status(proposal_id: str, status: CubeStatus) -> bool:
    db = await get_database()
    result = await db.fndc.cube_proposals.update_one(
        {"_id": ObjectId(proposal_id)},
        {"$set": {"status": status, "updated_at": datetime.now(UTC)}}
    )
    return result.modified_count > 0


# Tournament Registration CRUD operations
async def register_user_to_tournament(tournament_id: str, user_id: str) -> dict:
    db = await get_database()
    
    # Check if user is already registered
    existing_registration = await db.fndc.tournament_registrations.find_one({
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
    
    result = await db.fndc.tournament_registrations.insert_one(registration)
    registration["id"] = str(result.inserted_id)
    return registration


async def get_tournament_registrations(tournament_id: str) -> List[dict]:
    db = await get_database()
    registrations = await db.fndc.tournament_registrations.find({"tournament_id": tournament_id}).to_list(length=None)
    for registration in registrations:
        registration["id"] = str(registration["_id"])
        del registration["_id"]
    return registrations


async def check_user_registration(tournament_id: str, user_id: str) -> bool:
    db = await get_database()
    registration = await db.fndc.tournament_registrations.find_one({
        "tournament_id": tournament_id,
        "user_id": user_id
    })
    return registration is not None 