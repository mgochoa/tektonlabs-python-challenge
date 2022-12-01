from dataclasses import dataclass
import requests


@dataclass
class BaseHttpService:
    base_url: str


