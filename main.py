from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal
from models import Song
from modelClass import SongModel
import json

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def read_root():
    return {'name': 'fastapi-songs'}


@app.get('/songs/')
def read_songs(db: Session = Depends(get_db)):
    songs = db.query(Song).all()
    resp = {}
    for i, value in enumerate(songs):
        resp[i] = SongModel(id=value.id, title=value.title, artist=value.artist, release_date=str(value.release_date))
    return resp