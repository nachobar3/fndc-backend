from typing import List
from fastapi import APIRouter, Depends, HTTPException
from ..models import TournamentCreate, Tournament
from ..auth import get_current_active_user, get_current_admin_user
from ..crud import (
    create_tournament, get_tournaments, get_tournament_by_id,
    register_user_to_tournament, get_tournament_registrations,
    check_user_registration
)

router = APIRouter(prefix="/tournaments", tags=["tournaments"])


# Admin endpoints
@router.post("/", response_model=Tournament)
async def create_new_tournament(
    tournament: TournamentCreate,
    current_admin: dict = Depends(get_current_admin_user)
):
    """Create a new tournament (Admin only)"""
    try:
        created_tournament = await create_tournament(tournament, current_admin["id"])
        return created_tournament
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Public endpoints (no authentication required)
@router.get("/", response_model=List[Tournament])
async def list_tournaments():
    """Get all tournaments (Public)"""
    tournaments = await get_tournaments()
    return tournaments


@router.get("/{tournament_id}", response_model=Tournament)
async def get_tournament(tournament_id: str):
    """Get tournament by ID (Public)"""
    tournament = await get_tournament_by_id(tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament


# Protected endpoints (authentication required)
@router.post("/{tournament_id}/register")
async def register_to_tournament(
    tournament_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Register current user to a tournament (Authentication required)"""
    # Check if tournament exists
    tournament = await get_tournament_by_id(tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    try:
        registration = await register_user_to_tournament(tournament_id, current_user["id"])
        return {
            "message": "Successfully registered to tournament",
            "registration": registration
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{tournament_id}/registrations")
async def get_registrations(
    tournament_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Get all registrations for a tournament (Authentication required)"""
    # Check if tournament exists
    tournament = await get_tournament_by_id(tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    registrations = await get_tournament_registrations(tournament_id)
    return registrations


@router.get("/{tournament_id}/my-registration")
async def check_my_registration(
    tournament_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Check if current user is registered for a tournament (Authentication required)"""
    # Check if tournament exists
    tournament = await get_tournament_by_id(tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    is_registered = await check_user_registration(tournament_id, current_user["id"])
    return {"is_registered": is_registered} 