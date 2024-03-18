from fastapi import FastAPI
from user.controllers import router as user_router
import uvicorn

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["user"])


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)