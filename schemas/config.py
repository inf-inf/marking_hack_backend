from pydantic import BaseModel


class SetConfig(BaseModel):
    good_percent_limit: float
    warn_percent_limit: float
