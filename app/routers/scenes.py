from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Scene
from app.schemas import SceneCreate, SceneOut

router = APIRouter()


@router.get('/', response_model=list[SceneOut])
def list_scenes(title_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(Scene)
    if title_id is not None:
        q = q.filter(Scene.title_id == title_id)
    return q.order_by(Scene.id).all()


@router.get('/{scene_id}', response_model=SceneOut)
def get_scene(scene_id: int, db: Session = Depends(get_db)):
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not scene:
        raise HTTPException(status_code=404, detail='Scene not found')
    return scene


@router.post('/', response_model=SceneOut)
def create_scene(payload: SceneCreate, db: Session = Depends(get_db)):
    scene = Scene(
        title_id=payload.title_id,
        name=payload.name
    )
    db.add(scene)
    db.commit()
    db.refresh(scene)
    return scene


@router.delete('/{scene_id}')
def delete_scene(scene_id: int, db: Session = Depends(get_db)):
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not scene:
        raise HTTPException(status_code=404, detail='Scene not found')
    db.delete(scene)
    db.commit()
    return {'status': 'deleted'}
