# Estudos de Banco de Dados Cassandra com Python

Este repositório contém exemplos e informações relacionados aos meus estudos de Cassandra com Python. O Cassandra é projetado para funcionar em clusters distribuídos, onde os dados são distribuídos em vários nós para alta disponibilidade e escalabilidade linear.

## Visão Geral

- [Estudos de Banco de Dados Cassandra com Python](#estudos-de-banco-de-dados-cassandra-com-python)
  - [Visão Geral](#visão-geral)
  - [O que é Cassandra?](#o-que-é-cassandra)
  - [Configuração](#configuração)

## O que é Cassandra?

O Apache Cassandra é um banco de dados distribuído e altamente escalável que oferece alta disponibilidade, escalabilidade linear e flexibilidade de esquema, tornando-o adequado para uma ampla variedade de aplicativos, especialmente aqueles que requerem escalabilidade e tolerância a falhas.
Neste repositório, estou explorando como usar o Cassandra em conjunto com Python.
Para popular o banco realizo o consumo de dados via API do Spotify, utilizando a lib python Spotipy.

[Spotipy](https://spotipy.readthedocs.io/en/2.12.0/)


## Configuração

Antes de começar a trabalhar com o Cassandra em Python, você precisará configurar o ambiente. Você pode fazer isso instalando as bibliotecas necessáris. Use o seguinte comando para instalá-la:

```bash
pip install requirements.txt
```
Após a instalação da lib, você deve realizar a criação de um arquivo ```.env``` contendo as variavéis que serão utilizadas para provionar o cluster do cassandra no arquivo ```docker-compose```.

Para realizar a criação do container utilize o comando :
```bash 
docker-compose --env-file {seu_arquivo.env}  up -d 
```
Para acesso ao dados do Spotify deve ser registrado um app no spotify para garantir o acesso a api, abaixo o link da documentação com mais detalhes.

[API_Spotify](https://developer.spotify.com/documentation/web-api)

