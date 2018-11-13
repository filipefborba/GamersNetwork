# GamersNetwork
### Projeto final da disciplina de Redes Sociais (6 semestre) do curso Engenharia da Computação - Insper

Filipe Borba e Martim F. José

**To-do:**
* Selecionar 40 perfis de jogadores
* Para cada perfil, pegar as últimas 12 partidas**
* Montar uma rede social, sendo cada nó um jogador e cada partida um atributo, com performance*** e parceiros de time.

** Para pegar as últimas 12 partidas:
* POST - https://aquelesite.com.br/api/statistics/11679/search/0/pt-br
* POST HEADER - Referer: https://aquelesite.com.br/jogador/0

Para calcular a performance do jogador:
* O arquivo `hltv-rating.py` tem uma função que recebe os dados da partida e retorna um rating. (Ruim < 1, Médio = 1, Bom > 1)