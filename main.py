from fastapi import FastAPI
from user.controllers import router as user_router
from utils.controllers import router as utils_router


app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["user"])
# app.include_router(utils_router,prefix='/utils', tags=["utils"])

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)