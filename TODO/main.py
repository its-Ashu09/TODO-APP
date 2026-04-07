from fastapi import FastAPI
from routers import user,auth,task
from .database import engine
from . import models

app = FastAPI(
    
    title="My To-Do API",
    description="A production-ready To-Do app backend"

)
#  Create tables (async way)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await init_db()




#  Include router
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task.router)

@app.get("/",tags=['Home'])
def root():
    return {"message": "Welcome to the To-Do API! Go to /docs to test the endpoints."}