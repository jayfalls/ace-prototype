# DEPENDENCIES
## Third-Party
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
## Local
from helpers import debug_print
from constants.settings import DebugLevels
from .provider import generate_response


# VALIDATION
class Prompt(BaseModel):
    stack_type: str
    system_prompt: str


# SETUP
api = FastAPI()


# ROUTES
@api.get("/generate", response_class=JSONResponse)
async def generate(prompt: Prompt) -> dict:
    print(f"Generating response for {prompt.stack_type}...")
    response: str = generate_response(stack_type=prompt.stack_type, system_prompt=prompt.system_prompt)
    debug_print(f"Response: {response}", debug_level=DebugLevels.INFO)
    return {"response": response}
