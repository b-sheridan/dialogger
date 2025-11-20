from __future__ import annotations

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str


class ProjectCreate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int

    class Config:
        orm_mode = True


class SceneCreate(BaseModel):
    project_id: int
    name: str


class SceneOut(BaseModel):
    id: int
    project_id: int
    name: str

    class Config:
        orm_mode = True


class EntryCreate(BaseModel):
    scene_id: int
    text: str


class EntryOut(BaseModel):
    id: int
    scene_id: int
    text: str
    translation: str | None
    notes: str | None

    class Config:
        orm_mode = True
