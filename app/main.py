from contextlib import asynccontextmanager
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db, init_db
from app.models import Station

StationStatus = Literal["open", "closed", "maintenance"]

@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app= FastAPI(title="Stations", lifespan=lifespan)

class StationIn(BaseModel):
    code: str = Field(min_length=1)
    name: str = Field(min_length=1)
    capacity: int = Field(ge=1)
    status: StationStatus = "open"

class StationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    capacity: int
    status: str

class StationPatch(BaseModel):
    name : str | None =Field(default=None, min_length=1)
    status: StationStatus | None = None

@app.get("/health")
def health() -> dict:
    return {"status" : "ok"}


@app.post("/stations", response_model=StationOut, status_code=201)
def create_station(payload: StationIn, db: Session = Depends(get_db)) -> Station:
    row = Station(**payload.model_dump())
    db.add(row)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Code déjà utilisé.") from exc
    db.refresh(row)
    return row

@app.get("/stations", response_model=list[StationOut])
def list_stations(status: StationStatus | None = None, db: Session = Depends(get_db)) -> list[Station]:
    query = db.query(Station)
    if status is not None:
        query = query.filter(Station.status == status)
    return query.order_by(Station.id).all()

@app.get("/stations/{station_id}", response_model=StationOut)
def get_station(station_id: int, db: Session = Depends(get_db)) -> Station:
    row = db.query(Station).filter(Station.id == station_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Station inconnue")
    return row

@app.patch("/stations/{station_id}", response_model=StationOut)
def patch_station(station_id: int, payload: StationPatch, db: Session = Depends(get_db)) -> Station:
    row = db.query(Station).filter(Station.id == station_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Station inconnue")
    if payload.name is not None:
        row.name = payload.name
    if payload.status is not None:
        row.status = payload.status
    db.commit()
    db.refresh(row)
    return(row)