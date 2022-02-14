import models
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Game
from datetime import datetime
from fastapi.encoders import jsonable_encoder

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

class GameRequest(BaseModel):
    vendorId:int
    vendor:str
    gameName:str
    active:bool
    mobile:bool
    visible:bool  

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
@app.get("/form")
async def form(request: Request):
    return templates.TemplateResponse("form.html",{
        "request": request
    })
        
@app.get("/")
async def dashboard(request: Request, vendorId=None, gameName=None, active=None, visible=None, db: Session = Depends(get_db)):
    
    games =db.query(Game)
    
    if vendorId:
        games = games.filter(Game.vendorId == vendorId)
    
    if gameName:
        games = games.filter(Game.name == gameName)
        
    if active:
        if active=="on":
            games = games.filter(Game.active == True)
            
    if visible:
        if visible=="on":
            games = games.filter(Game.visible ==True)

    
    return templates.TemplateResponse("dashboard.html",{
        "request": request,
        "games":games,
        "vendorId":vendorId,
        "gameName":gameName,
        "active":active,
        "visible":visible
    })


@app.post("/game")
async def create_game(game_request: GameRequest, db: Session = Depends(get_db)):
    game = Game()
    game.vendorId = game_request.vendorId
    game.vendor = game_request.vendor
    game.name = game_request.gameName
    game.active = game_request.active
    game.mobile = game_request.mobile
    game.visible = game_request.visible
    
    db.add(game) 
    db.commit()
    
    today = datetime.now()
    
    return {
        "game":game,
        "date":today,
        "code": "success",
        "message": "game created"
    }

@app.get("/games")
async def fetch_games(db: Session = Depends(get_db)):
    games =db.query(Game).all()
    
    today = datetime.now()
    
    return {
        "game":games,
        "date":today,
        "code": "success",
        "message": "list created"
    }
    
@app.get("/games/{vendorId}")
async def fetch_game(vendorId: int, db: Session = Depends(get_db)):
    game =db.query(Game).filter(Game.vendorId==vendorId).first()
    
    today = datetime.now()
    
    if game:
        return {
            "game":game,
            "date":today,
            "code": "success",
            "message": "return game"
        }
    else:
        return {
            "date":today,
            "code": "error",
            "message": "none game"
        }
        
@app.delete("/games/{vendorId}")
async def delete_game(vendorId: int, db: Session = Depends(get_db)):
   game = db.query(Game).filter(Game.vendorId==vendorId).one()
   
   db.delete(game)
   db.commit()
   
   today = datetime.now()
    
   return {
            "game":game,
            "date":today,
            "code": "success",
            "message": "game deleted"
            }
   
@app.put("/games/{vendorId}")
async def update_game(vendorId: int, game_request: GameRequest, db: Session = Depends(get_db)):
    game =db.query(Game).filter(Game.vendorId==vendorId).one()
    
    game.vendorId = game_request.vendorId
    game.vendor = game_request.vendor
    game.name = game_request.gameName
    game.active = game_request.active
    game.mobile = game.mobile
    game.visible=game.visible

    db.commit()
    
    today = datetime.now()
    
    return {
            "game":game,
            "date":today,
            "code": "success",
            "message": "game updated"
            }