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

    def __post_init__(self) -> None:
        for name, value in vars(self).items():
            if value is None:
                setattr(self, name, "")

    def is_useful(self) -> bool:
        """True when the provider actually located the CEP (city and state known).

        A CEP shared by a whole city may have no street or district, so those
        fields are not required.
        """
        return bool(self.city.strip() and self.state.strip())

    def __getitem__(self, key: str | int) -> str:
        return getattr(self, keys_mapping[key])

    def __bool__(self) -> bool:
        return any(vars(self).values())
