from dataclasses import dataclass


@dataclass
class BaseHttpService:
    base_url: str
