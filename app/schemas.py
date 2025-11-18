from __future__ import annotations

from pydantic import BaseModel


class TitleBase(BaseModel):
    name: str
    slug: str | None = None


class TitleCreate(TitleBase):
    pass


class TitleOut(TitleBase):
    id: int

    class Config:
        orm_mode = True


class SceneCreate(BaseModel):
    title_id: int
    name: str


class SceneOut(BaseModel):
    id: int
    title_id: int
    name: str

    class Config:
        orm_mode = True


class LineCreate(BaseModel):
    scene_id: int
    speaker_id: int | None = None
    text: str


class LineOut(BaseModel):
    id: int
    scene_id: int
    speaker_id: int | None
    text: str

    class Config:
        orm_mode = True
