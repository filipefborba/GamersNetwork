# GamersNetwork
Filipe Borba, Martim F. José  
6º Semestre  
Engenharia da Computação Insper  
Redes Sociais  

## Sumário

- [Dados](#dados)
- [Código](#código)
- [Análise](#análise)

## Dados

Os dados coletados foram da plataforma GamersClub, através de uma API e do próprio código HTML das páginas de partidas dos campeonatos. Com eles, podemos verificar para cada jogador quem foram seus companheiros de equipe, além do seu desempenho médio por campeonato utilizando o rating 2.0.

## Código
A coleta de dados é feita em diferentes etapas. Primeiro, é necessário receber todos os dados do site. Para tanto, é necessário entrar na pasta API_Scrapers e dentro de `apiscraper_gamersclub` certificar-se de que as requisições funcionam e que os ids de campeonatos estão corretos. Após instalar as dependências, rode o arquivo usando o comando ```python3 apiscraper_gamersclub.py```. O arquivo ```campeonatos_completo``` será salvo na pasta.
Depois, use o ```python3 clean_scraped_data.py``` e ```python3 create_network_data.py``` para obter os dados finais com o nome de ```network_cleaned_data```.

## Análise
Para verificar a análise feita em cima dos dados, basta instalar o [Jupyter Notebook](http://jupyter.org/) e abrir o arquivo ```GamersNetwork.ipynb```. Nesse notebook estão algumas explicações, assim como o artigo pode ser encontrado no arquivo ```Filipe_Martim_RedesSociais.pdf```.
