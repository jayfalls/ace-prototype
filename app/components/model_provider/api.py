# DEPENDENCIES
## Built-In
from threading import Thread
## Third-Party
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
## Local
from .provider import startup, llm_stack


# VALIDATION
class Prompt(BaseModel):
    stack_type: str
    system: str


# SETUP
api = FastAPI()
Thread(target=startup)


# ROUTES
@api.get("/generate", response_class=JSONResponse)
async def generate(prompt: Prompt) -> dict:
    response: str = getattr(llm_stack, prompt.stack_type).generate(prompt.system)
    return {"response": response}
