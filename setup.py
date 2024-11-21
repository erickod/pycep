from setuptools import setup

setup(
    name="pycep",
    version="1.0.4",
    description="Consulta CEPs em vários serviços (Correios, ViaCep, OpenCep) de maneira totalmente assíncrona",
    author="Erick Duarte",
    author_email="erickod@gmail.com",
    packages=["pycep"],  # same as name
    install_requires=[
        "wheel",
        "httpx==0.24.1",
        "aiohttp==3.8.1",
    ],
)
