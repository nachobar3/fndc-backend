from typing import List
from fastapi import APIRouter, Depends, HTTPException
from ..models import CubeProposalCreate, CubeProposal, CubeStatus
from ..auth import get_current_active_user, get_current_admin_user
from ..crud import (
    create_cube_proposal, get_cube_proposals_by_tournament,
    get_enabled_cubes_by_tournament, update_cube_status,
    get_tournament_by_id
)

router = APIRouter(prefix="/cubes", tags=["cubes"])


# User endpoints (authentication required)
@router.post("/propose", response_model=CubeProposal)
async def propose_cube(
    proposal: CubeProposalCreate,
    current_user: dict = Depends(get_current_active_user)
):
    """Propose a cube for a tournament (Authentication required)"""
    # Check if tournament exists
    tournament = await get_tournament_by_id(proposal.tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    try:
        created_proposal = await create_cube_proposal(proposal, current_user["id"])
        return created_proposal
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Public endpoints (no authentication required)
@router.get("/tournament/{tournament_id}/enabled", response_model=List[CubeProposal])
async def get_enabled_cubes(tournament_id: str):
    """Get all enabled cubes for a tournament (Public)"""
    # Check if tournament exists
    tournament = await get_tournament_by_id(tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    cubes = await get_enabled_cubes_by_tournament(tournament_id)
    return cubes


# Admin endpoints (admin authentication required)
@router.get("/tournament/{tournament_id}/all", response_model=List[CubeProposal])
async def get_all_cube_proposals(
    tournament_id: str,
    current_admin: dict = Depends(get_current_admin_user)
):
    """Get all cube proposals for a tournament (Admin only)"""
    # Check if tournament exists
    tournament = await get_tournament_by_id(tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    proposals = await get_cube_proposals_by_tournament(tournament_id)
    return proposals


@router.put("/{proposal_id}/status")
async def update_cube_proposal_status(
    proposal_id: str,
    status: CubeStatus,
    current_admin: dict = Depends(get_current_admin_user)
):
    """Update cube proposal status (Admin only)"""
    success = await update_cube_status(proposal_id, status)
    if not success:
        raise HTTPException(status_code=404, detail="Cube proposal not found")
    
    return {"message": f"Cube proposal status updated to {status}"} 