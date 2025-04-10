from pydantic import BaseModel

class Job(BaseModel):
    id: str
    name: str
    main_activies: str
    prerequisities: str
    diferentials: str