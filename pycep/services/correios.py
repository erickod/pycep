import xml.etree.ElementTree as ET
from typing import Any

import httpx

from pycep.protocols.query_service import QueryService


class CorreiosService:
    def __init__(self, http_client=httpx) -> None:
        self.__endpoint = "https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente"
        self.__http_client = http_client

    async def query_cep(self, cep: str) -> Any:
        response = self.__http_client.post(
            self.__endpoint, data=self.__get_request_data(cep)
        ).text
        et = ET.fromstring(response)
        return self.__fit_to_cep_model(et)

    @classmethod
    def __fit_to_cep_model(cls, response) -> Any:
        cep = {}
        element = response[0][0][0]
        cep["district"] = element.find("bairro").text or ""
        cep["city"] = element.find("cidade").text or ""
        cep["address"] = element.find("end").text or ""
        cep["state"] = element.find("uf").text or ""
        cep["provider"] = cls.__name__
        complemento = element.find("complemento2").text
        if complemento:
            cep["address"] += f" {complemento}"

        return cep

    def __get_request_data(self, cep: str) -> bytes:
        return (
            b'<?xml version="1.0"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cli="http://cliente.bean.master.sigep.bsb.correios.com.br/"><soapenv:Header /><soapenv:Body><cli:consultaCEP><cep>'
            + cep.encode()
            + b"</cep></cli:consultaCEP></soapenv:Body></soapenv:Envelope>"
        )


def make() -> QueryService:
    return CorreiosService()
