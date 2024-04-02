import uvicorn, settings
from fastapi import FastAPI, APIRouter
from api.handlers import users_router
from api.login_handler import login_router

app = FastAPI()
main_router = APIRouter()

main_router.include_router(login_router, prefix="/token", tags=["token"])
main_router.include_router(users_router, prefix="/users", tags=["users"])

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)