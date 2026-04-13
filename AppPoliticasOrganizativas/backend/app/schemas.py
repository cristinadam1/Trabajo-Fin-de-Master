from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class GenerationBase(BaseModel):
    input_text: str = Field(..., min_length=1, 
                            description="Texto de entrada para generar las políticas organizativas", 
                            example="¿Cuáles son las mejores prácticas para la seguridad de la información en una empresa en Francia?")


class GenerationCreate(GenerationBase):
    pass


class GenerationResponse(BaseModel):
    id: UUID
    input_text: str
    politicas: str
    buenas_practicas: str
    acciones_prohibidas: str
    riesgos: str
    explicacion: str
    is_favorite: bool
    created_at: datetime

    class Config:
        from_attributes = True


class GenerationListResponse(BaseModel):
    id: UUID
    input_text: str
    is_favorite: bool
    created_at: datetime

    class Config:
        from_attributes = True


class FavoriteUpdate(BaseModel):
    is_favorite: bool
