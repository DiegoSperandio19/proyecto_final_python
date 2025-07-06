from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import time

class Restaurant(BaseModel):
    id_restaurant: UUID | None =None #para cuando se crea un usuario, no se tiene el id
    name: str
    location: str
    opening_time: time
    closing_time: time

    model_config = ConfigDict(
        from_attributes=True
    )