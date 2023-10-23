import xml.etree.ElementTree as ET

from pycep.adapters.aiohttp_client import AioHttpHttpClient, HttpResponse
from pycep.cep_data import CepData
from pycep.protocols.http_client import HttpClient
from pycep.protocols.query_service import QueryService


class CorreiosService:
    def __init__(self, http_client: HttpClient = AioHttpHttpClient()) -> None:
        self.__endpoint = "https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente"
        self.__http_client = http_client

    async def query_cep(self, cep: str) -> CepData:
        self.__cep_number = cep
        response: HttpResponse = await self.__http_client.post(
            self.__endpoint, data=self.__get_request_data(cep)
        )
        et = ET.fromstring(response.text())
        return self.__fit_to_cep_model(et)

    def __fit_to_cep_model(self, response) -> CepData:
        element = response[0][0][0]
        cep_data = CepData(
            cep=self.__cep_number,
            street=element.find("end").text or "",
            district=element.find("bairro").text or "",
            city=element.find("cidade").text or "",
            state=element.find("uf").text or "",
            provider=self.__class__.__name__,
        )
        complemento = element.find("complemento2").text
        if complemento:
            cep_data.street += f" {complemento}"
        return cep_data

    def __get_request_data(self, cep: str) -> bytes:
        return (
            b'<?xml version="1.0"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cli="http://cliente.bean.master.sigep.bsb.correios.com.br/"><soapenv:Header /><soapenv:Body><cli:consultaCEP><cep>'
            + cep.encode()
            + b"</cep></cli:consultaCEP></soapenv:Body></soapenv:Envelope>"
        )


def make() -> QueryService:
    return CorreiosService()
