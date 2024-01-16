from dataclasses import dataclass

keys_mapping = {
    "street": "street",
    "city": "city",
    "state": "state",
    "cep": "cep",
    "provider": "provider",
    "query_service": "provider",
    "district": "district",
    "number": "cep",
    "uf": "state",
}


@dataclass
class CepData:
    street: str = ""
    district: str = ""
    city: str = ""
    state: str = ""
    cep: str = ""
    complement: str = ""
    provider: str = ""

    def __getitem__(self, key: str | int) -> str:
        return getattr(self, keys_mapping[key])

    def __bool__(self) -> bool:
        return any(vars(self).values())
