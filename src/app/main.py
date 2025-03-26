# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.core.config import settings
from src.app.middleware.error_handler import add_error_handlers

from src.app.api.v1 import users  
from src.app.api.v1 import patients 
from src.app.api.v1 import chatbot



# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION
)


# CORS Middleware (Allows frontend apps to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Use API_VERSION from config.py
API_PREFIX = f"/api/{settings.API_VERSION}"

# Register routes
# users
app.include_router(users.router, prefix=f"{API_PREFIX}/users", tags=["Users"])
# patients
app.include_router(patients.router, prefix=f"{API_PREFIX}/patients", tags=["Patients"])
# chatbot
app.include_router(chatbot.router, prefix=f"{API_PREFIX}/chatbot", tags=["Chatbot"])


# Add global error handlers
add_error_handlers(app)

# Root endpoint
@app.get("/", tags=["API Health Check"])
def root():
    return {"message": f"Welcome to HealthPro!", "status": "OK"}



# Run app only if executed directly (not imported)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=True)





