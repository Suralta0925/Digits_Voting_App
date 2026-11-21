

from pydantic import BaseModel, Field, ConfigDict
from datetime import date, time

class Election(BaseModel):
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)


    id : int = Field(default=None, validation_alias='election_id')
    title: str = Field(validation_alias='election_name')
    start_time: time | None = Field(default=None, validation_alias='start_time')
    end_time: time | None = Field(default=None, validation_alias='end_time')
    starts_at: date | None = Field(default=None, validation_alias='starts_at')