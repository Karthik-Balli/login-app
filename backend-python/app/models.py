from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr
    password: str | None = None
    role: str = "user"
    provider: str = "local"
