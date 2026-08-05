from pydantic import BaseModel


class SponsorResponse(BaseModel):
    id: str
    name: str
    category: str
    fit: int
    estimatedPrice: str
    responseProb: int
    status: str
