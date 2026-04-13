import os
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Generation
from app.schemas import (
    GenerationCreate,
    GenerationResponse,
    GenerationListResponse,
    FavoriteUpdate,
)
from AppPoliticasOrganizativas.backend.app.services.llm import generate_policy_content

router = APIRouter()

@router.post("/generar", response_model=GenerationResponse, status_code=status.HTTP_201_CREATED)
def create_generation(generation: GenerationCreate, db: Session = Depends(get_db)):
    result = generate_policy_content(generation.input_text)
    
    db_generation = Generation(
        input_text=generation.input_text,
        politicas=result["politicas"],
        buenas_practicas=result["buenas_practicas"],
        acciones_prohibidas=result["acciones_prohibidas"],
        riesgos=result["resgos"],
        explicacion=result["explicacion"],
    )
    db.add(db_generation)
    db.commit()
    db.refresh(db_generation)
    return db_generation


@router.get("/generaciones", response_model=List[GenerationListResponse])
def list_generaciones(skip: int = 0, limit: int = 50, favorite_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(Generation).order_by(Generation.created_at.desc())
    if favorite_only:
        query = query.filter(Generation.is_favorite == True)
    return query.offset(skip).limit(limit).all()


@router.get("/generaciones/{generacion_id}", response_model=GenerationResponse)
def get_generation(generacion_id: UUID, db: Session = Depends(get_db)):
    generation = db.query(Generation).filter(Generation.id == generacion_id).first()
    if not generation:
        raise HTTPException(status_code=404, detail="Generacion no encontrada")
    return generation


@router.delete("/generaciones/{generacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_generation(generacion_id: UUID, db: Session = Depends(get_db)):
    generation = db.query(Generation).filter(Generation.id == generacion_id).first()
    if not generation:
        raise HTTPException(status_code=404, detail="Generacion no encontrada")
    db.delete(generation)
    db.commit()
    return None


@router.put("/generaciones/{generacion_id}/favorito", response_model=GenerationResponse)
def update_favorite(
    generacion_id: UUID,
    favorite: FavoriteUpdate,
    db: Session = Depends(get_db)
):
    generation = db.query(Generation).filter(Generation.id == generacion_id).first()
    if not generation:
        raise HTTPException(status_code=404, detail="Generacion no encontrada")
    generation.is_favorite = favorite.is_favorite
    db.commit()
    db.refresh(generation)
    return generation


@router.post("/regenenerar/{generacion_id}", response_model=GenerationResponse, status_code=status.HTTP_201_CREATED)
def regenerate_generation(generacion_id: UUID, db: Session = Depends(get_db)):
    original = db.query(Generation).filter(Generation.id == generacion_id).first()
    if not original:
        raise HTTPException(status_code=404, detail="Generacion no encontrada")
    
    result = generate_policy_content(original.input_text)
    
    nueva_generation = Generation(
        input_text=original.input_text,
        politicas=result["politicas"],
        buenas_practicas=result["buenas_practicas"],
        acciones_prohibidas=result["acciones_prohibidas"],
        riesgos=result["resgos"],
        explicacion=result["explicacion"],
    )
    db.add(nueva_generation)
    db.commit()
    db.refresh(nueva_generation)
    return nueva_generation