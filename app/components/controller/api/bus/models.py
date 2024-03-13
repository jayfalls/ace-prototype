# DEPENDENCIES
## Built-In
from typing import Optional
## Third-Party
from pydantic import BaseModel


# REQUESTS
class PostBusMessage(BaseModel):
    queue: str
    message: str
    action: str


# RESPONSES
class VerifyResponse(BaseModel):
    status: str
    action: str


# SERVICE PARAMETERS
class BusPublishPayload(BaseModel):
    message: str
    source_direction: str
    action: str