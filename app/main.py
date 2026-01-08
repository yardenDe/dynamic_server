import uvicorn
from fastapi import FastAPI
import api
from db_manager import DB_Manager
from api_manager import ApiManager


app = FastAPI()

# Initialize application services
db_manager = DB_Manager()
api_manager = ApiManager(db_manager)

api.api_manager = api_manager
api.setupRoutes(app)


if __name__ == "__main__":
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
       