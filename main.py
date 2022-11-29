import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
import utils.mongo as mongodb

from routes import auth, user

app = FastAPI(title="Daniel Smyth API", docs_url="/api/docs")

logger = logging.getLogger("uvicorn.error")

settings = config.get_settings()

ENV = settings.environment  # Environment: dev/production

FRONT_END_URL = settings.APP_URL_DEV if ENV == "dev" else settings.APP_URL

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONT_END_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.r)
app.include_router(user.r)


@app.on_event("startup")
async def start_database():
    """Initialize MongoDB connection and Beanie ORM"""
    db_name = settings.DB_NAME_DEV if ENV == "dev" else settings.DB_NAME

    await mongodb.manager.connect(settings.DB_URL, db_name)
    await mongodb.manager.init_beanie(db_name)

    logger.info(f"CORS: '{FRONT_END_URL}'")
    logger.info(f"Database: '{db_name}'")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888, debug=True)
