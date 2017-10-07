# aonorte.py

Todos os meses recebo, do cineclube AoNorte, a lista dos filmes que vão ser exibidos no mês seguinte. A minha tarefa é, para cada filme, criar uma folha de sala com informação técnica do filme, assim como escolher duas ou três críticas ao mesmo.

Encontrar a informação técnica é entediante, demorado e repetitivo, pelo que decidi tentar criar um pequeno script que automatizasse o processo.

DIFICULDADES
- O TMDB tem muito pouca informação para filmes menos conhecidos, pelo que tenho de usar o IMDB.
- O IMDB não tem um API, por isso isto vai ter de ser feito por interpretação das páginas com expressões regulares... O mesmo para o CINECARTAZ (preciso deste para obter as sinopses em Pt)

VERSÕES

v0.1 (2017/09/28):
- Função 'sheet(films)' - A partir de uma string com a lista de filmes (lista com o formato da AoNorte), cria um ficheiro .txt com os cabeçalhos dos filmes e espaço para preencher com os dados de cada filme.

v0.2.1 (2017/10/03):
- Melhorias no código.
- Função 'infofilm(film)' - A partir dos cabeçalhos, identifica a seguinte informação: título original, realizador, AoNorte

v0.2.2 (2017/10/04): 
- Melhorias no código - comentários; compartimentar o código para poder reutilizar noutros projectos.
- Função 'infofilm(film)' - Usa a informação recolhida para pesquisar na internet (usando o duckduckgo) e identificar os links que dizem respeito à entrada do filme no IMDB e no Cinecartaz.

v0.2.3 (2017/10/07):
- Função 'infofilm(film)' - A partir dos links obtidos, identifica em cada página a informação relevante para as folhas de sala.

FUTURO

- Encontrar links para críticas: complexo, pois a pesquisa é muito mais alargada e diversificada.

- Compartimentar ainda mais o código, de modo a obter pelo menos quatro funções separadas:

    def aonorte2list: cria uma lista de tuples a partir do texto enviado    pela ao norte
    
    def filmurl: obtém uma namedtuple com os urls dos filmes
    
    def filminfo: a partir de urls, obter informação. Devolver um dicionário em vez de uma lista, para que possa utilizar noutro projecto qualquer de pesquisa de filmes.
    
    def printsheet: imprime folhas de sala com qualquer formato a partir de qualquer dicionário com informação de filmes.
    
- Experimentar o API do duckduckgo em vez de utilizar directamente o requests e comparar a rapidez de pesquisa.

- Implementar uma base de dados (JSON) em vez de named.tuples e dicionários, onde possa armazenar uma maior quantidade de informação de cada filme, assim como um histórico de todos os filmes projectados pela AoNorte.
