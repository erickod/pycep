# PyCEP

Consulta CEPs em vários serviços (ViaCep, OpenCep, BrasilAPI, ApiCep) de maneira totalmente assíncrona

## Comece por aqui

Nesta seção você encontrará instruções de como instalar o pacote e também encontrará exemplos de uso

### Requerimentos

Esse projeto é compatível com as versões `3.10` a `3.14` do python no momento. A compatibilização com versões anteriores está prevista, e qualquer contribuição é bem vinda.

### Instalação

##### PIP

```
pip install pycep
```

##### Poetry

```
poetry add pycep
```

### Fazendo uma consulta

Os serviços são consultados ao mesmo tempo e nenhum espera pelo outro. A lib retorna o primeiro resultado *útil* (com cidade e UF); respostas "não encontrado" e falhas de um serviço são ignoradas enquanto outro ainda puder responder.

- Se nenhum serviço encontrar o CEP, os atributos vêm vazios (`cep.city == ""`).
- Se nenhum serviço responder (todos falharam ou estourou o `timeout`), é levantado `pycep.CepQueryError`.
- O tempo total pode ser ajustado: `Cep("75140070", timeout=5)` (padrão: 10 segundos).

```python
from pycep import Cep

cep = Cep("75140070")
```

### Acessando os dados da consulta

Você pode usar os atributos listados abaixo para acessar os dados do Cep:

```python
from pycep import Cep

cep = Cep("75140070")

print(cep.number) # 75140070
print(cep.state) # GO
print(cep.city) # Anápolis
print(cep.street) # Rua Senador Mardocheu Diniz
print(cep.district) # Dom Pedro II
print(cep.query_service) #ViaCepService
print(cep.status) # query_done
```

Você também pode converter os dados para dict

```python
from pycep import Cep

cep = Cep("75140070")
print(dict(cep))

{
 'street': 'Rua Senador Mardocheu Diniz',
 'district': 'Dom Pedro II',
 'city': 'Anápolis',
 'state': 'GO',
 'cep': '75140070',
 'provider': 'ViaCepService'
 }

```

## Este projeto utiliza

- [HttpX](https://www.python-httpx.org/) - Adapter padrão para requisições HTTP
- [AioHTTP](https://docs.aiohttp.org/en/stable/) - Adapter alternativo para requisições HTTP
- [Poetry](https://python-poetry.org/) - Gerenciamento de dependências e publicação
- [Pytest](https://docs.pytest.org/) - Testes automatizados

## Autor

- **Erick Duarte** - _Implementação inicial_ - [erickod](https://github.com/erickod)

## Licença

O projeto está disponível através da licença MIT - Consulte o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.
