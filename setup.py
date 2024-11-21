from setuptools import find_packages, setup

setup(
    name="pycep",
    version="1.0.4",
    description="Consulta CEPs em vários serviços (Correios, ViaCep, OpenCep) de maneira totalmente assíncrona",
    author="Erick Duarte",
    author_email="erickod@gmail.com",
    packages=find_packages(),
    install_requires=[
        "wheel",
        "httpx==0.24.1",
        "aiohttp==3.8.1",
    ],
)
