from pydantic import BaseModel

class File(BaseModel):
    id: str
    job_id: str