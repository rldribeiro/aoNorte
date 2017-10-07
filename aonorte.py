date = ("2017", "Outubro")

films = """

Dia 02 – A CIDADE PERDIDA DE Z, de James Gray
(The Lost City of Z, EUA, 2016, 140', M/12)

Dia 06 – OS DESASTRES DE SOFIA, de Christophe Honoré
(Les malheurs de Sophie, FRA, 2016, 106', M/12)
 
Dia 09 – A VIDA DE UMA MULHER, Stéphane Brizé
(Une Vie, BEL/FRA, 2016, 119', M/12)
 
Dia 13 – A MÃE, de Alberto Morais
(La Madre, ESP/ FRA/ ROM, 2016, 89', M/12)
 
Dia 16 – SÃO JORGE, de Marco Martins
(São Jorge, POR, 2016, 112', M/12)

Dia 20 – OS CHAPÉUS-DE-CHUVA DE CHERBURG, de Jacques Demy
(Les Parapluies de Cherbourg, FRA, 1964, 90', M/12)
 
Dia 23 – GOOD TIME, de Josh Safdie, Benny Safdie
(Good Time, USA, 2017, 101', M/12)

Dia 27 – AS DONZELAS DE ROCHEFORT, de Jacques Demy
(Les Demoiselles de Rochefort, FRA, 1966, 120', M/12)
 
Dia 30 – A FÁBRICA DE NADA, de Pedro Pinho
(A FÁBRICA DE NADA, POR, 2017, 177', M/12)

"""



# Transformar a string numa lista, removendo espaços em branco
films = [film for film in films.split("\n") if len(film) > 1] 
films = list(zip(films[::2], films[1::2]))

# Funções

def sheet(films):
    """
    Entrada: uma string com uma lista de filmes, segundo o modelo fornecido pela AoNorte.
    
    Saída: um ficheiro .txt, com o formato das folhas de sala determinado por 'heads'.
    
    """
    
    heads = """
/////////////////////////////////////////////////////////

{}
{}

Interpretação: {}
Argumento: {}
Música: {}
Cinematografia: {}
Edição: {}

Sinopse: {}

Crítica: 



"""
    aonorte = open('AoNorte_' + date[0] + "_" + date[1] + '.txt','w')
    aonorte.write('SESSÕES CINECLUBISTAS AO NORTE | ' + date[1] + ' de ' + date[0] + "\n")
    
    print("\nA escrever no ficheiro '" + aonorte.name + "':\n")
    
    for film in films:
        print("..............", "\n")
        aonorte.write(heads.format(film[0], film[1], *filminfo(film)))
        
    aonorte.close()
    print("\nDone!")
    

def filminfo(film):
    
    """
    Para cada filme, esta função determina os links respectivos para o cinecartaz e o imdb. Depois recolhe toda a informação necessária de cada uma dessas páginas.
    
    Entrada: tuple com o seguinte formato:
    
    ('Dia 20 – OS CHAPÉUS-DE-CHUVA DE CHERBURG, de Jacques Demy', '    (Les Parapluies de Cherbourg, FRA, 1964, 90', M/12)')
    
    
    Saída: tuple com actores, argumento, musica, cinematografia, edicao, sinopse
    
    """
    
    # Importações
    import requests, re # Requests para gravar conteúdo da net; re para usar expressões regulares
    from bs4 import BeautifulSoup # Para formatar as páginas
    
    # Criar uma string única para cada filme
    film = film[0] + " " + film[1]
    print(film)
    
    # Título, realizador, ano
    info = re.search(r"Dia\s\d+.{3}(.*),\s?d?e?([\w\s]*)\s\(([\w\s]*)\,.*(\d{4})", film)
    title, director, ortitle, year = info.group(1).title(), info.group(2),  info.group(3).title(), info.group(4)
    
    # Adicionar '+' para usar nos padrões de procura
    title = "+".join(title.split())
    director = "+".join(director.split())
    ortitle = "+".join(ortitle.split())
    
    # Para cada fonte (cinecartaz, imdb, mais no futuro?) encontrar o link respectivo para cada filme
    # source = [(name of source, regex string to find the code of source, url to replace), etc]
    sources = [("cinecartaz", r"cinecartaz\.publico\.pt[\w/\-]+?(\d+)", "http://m.cinecartaz.publico.pt/Mobile/Filmes/Index/{}"), 
               ("imdb", r"imdb\.com\/title\/([\w\d]+)", "http://www.imdb.com/title/{}/fullcredits/") ]
    filmcodes = {} # Dicionário vazio para preencher com dados dos filmes
    
    for source in sources:
        print("\nÀ procura em {}...".format(source[0]))
        
        duck_url = 'http://duckduckgo.com/html/?q={}+"{}"+{}+{}'.format(source[0], ortitle, director, year)
        print(duck_url)
        
        page = str(requests.get(duck_url).content)
        filmcode = source[2].format(re.search(source[1], page).group(1))
        print("Encontrado:", filmcode)
        
        filmcodes[source[0]] = filmcode
    
    # Processar as páginas para posterior pesquisa
    cinecartaz = requests.get(filmcodes['cinecartaz'])
    cinecartaz = BeautifulSoup(cinecartaz.content, 'html.parser')
                   
    imdb = requests.get(filmcodes['imdb'])
    imdb = BeautifulSoup(imdb.content, 'html.parser')
    
    # Pesquisa
    # Interpretação (CINECARTAZ)
    actores = re.findall(r'Actores[\n\r\t]([\w\s\-\'\,]*)[\n\r\t]Votar', cinecartaz.get_text())[0]
    print("\n")
    print("Interpretação:", actores)
    
    # Argumento (IMDB)
    argumento = re.search(r'(?<=Writing Credits).*?(?=Cast)', imdb.get_text(), flags=re.S).group()
    argumento = ', '.join(re.findall(r'(\(?\w+(?:\s\w+)*\)?)', argumento))
    print("Argumento:", argumento)
    
    # Música (IMDB)
    musica = re.search(r'(?<=Music by).*?(?=Cinematography)', imdb.get_text(), flags=re.S)
    # No caso de não haver compositor, alterar o resultado para ' ' 
    musica = musica.group() if musica != None else " "
    musica = ', '.join(re.findall(r'(\(?\w+(?:\s\w+)*\)?)', musica))
    print("Música:", musica)
    
    # Cinematografia (IMDB)
    cinematografia = re.search(r'(?<=Cinematography by).*?(?=Film Editing)', imdb.get_text(), flags=re.S).group()
    cinematografia = ', '.join(re.findall(r'(\(?\w+(?:\s\w+)*\)?)', cinematografia))
    print("Cinematografia:", cinematografia)
    
    # Edição (IMDB)
    edicao = re.search(r'(?<=Film Editing by).*?(?=\w+ [bB]y)', imdb.get_text(), flags=re.S).group()
    edicao = ', '.join(re.findall(r'(\(?\w+(?:\s\w+)*\)?)', edicao))
    print("Edição:", edicao)
    
    # Sinopse (CINECARTAZ)
    sinopse = cinecartaz.find(id="ContentDescription").get_text()[:-10]
    # [:-10] para obter o texto sem o "PÚBLICO" no final.
    print("\nSinopse:", sinopse)

    return actores, argumento, musica, cinematografia, edicao, sinopse

sheet(films)
