from dataclasses import dataclass


@dataclass
class CepData:
    street: str
    district: str
    city: str
    state: str
    cep: str
    provider: str
