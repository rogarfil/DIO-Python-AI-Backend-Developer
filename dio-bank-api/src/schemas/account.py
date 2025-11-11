from pydantic import BaseModel, NonNegativeFloat


class AccountIn(BaseModel):
    user_id: int
    balance: NonNegativeFloat = 0.0


class AccountOut(BaseModel):
    id: int
    user_id: int
    balance: float
    created_at: str

    class Config:
        from_attributes = True