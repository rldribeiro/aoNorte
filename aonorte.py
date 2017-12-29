# Input

date = ("2018", "Janeiro")

films = """

 
Dia 05 – ROSAS DE ERMERA, de Luís Filipe Rocha
(POR, 2017, 125', M/12)
 
Dia 08 – 120 BATIMENTOS POR MINUTO, de Robin Campillo
(120 Battements par Minute, FRA, 2017, 140', M/16)
 
Dia 12 – A LIBERDADE DO DIABO, de Everardo González
(La Libertad del Diablo, MEX, 2017, 74', M/12)
 
Dia 15 – LUCKY, de John Carroll Lynch
(EUA, 2017, 88', M/14)
 
Dia 19 – CORPO E ALMA, de Ildikó Enyedi
(Teströl és lélekröl, HUN, 2017, 116', M/12)
 
Dia 26 – VERÃO DANADO, de Pedro Cabeleira
(POR, 2017, 127', M/14)
 
Dia 29 – UMA MULHER FANTÁSTICA, de Sebastián Lelio
(Una Mujer Fantastica, EUA/ ALE/ ESP/ Chile, 2017, 104', M/12)
 

"""



# String to list, removing whitespaces.
films = [film for film in films.split("\n") if len(film) > 1] 
films = list(zip(films[::2], films[1::2]))



def sheet(films):
    """
    Input: String with a list of films formated according to AoNorte.
    
    Output: txt file with the detailed info for each film.
    
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
    
    print("\nWriting to file '" + aonorte.name + "':\n")
    
    for film in films:
        print("..............", "\n")
        aonorte.write(heads.format(film[0], film[1], *filminfo(film)))
        
    aonorte.close()
    print("\nDone!")
    

def filminfo(film):
    
    """
    For each film, this function finds the corresponding links to cinecartaz and imdb, using duckduckgo search, then it retrieves all info from each page.
    
    Input: tuple with following format:
    
    ('Dia 20 – OS CHAPÉUS-DE-CHUVA DE CHERBURG, de Jacques Demy', '    (Les Parapluies de Cherbourg, FRA, 1964, 90', M/12)')
    
    
    Output: tuple with actors, writers, music, cinematography, editing, sinopse.
    
    """
    
    import requests, re # requests to grab content from net; re to use regular expressions
    from bs4 import BeautifulSoup # BeautifulSoup to format the retrieved pages
    
    film = film[0] + " " + film[1]
    print(film)
    
    # Title, Director, year
    info = re.search(r"Dia\s\d+.{3}([\w\s'´`]*),\s?d?e?\s([\w\s]*)\s\(([\w\s'´`]*)\,.*(\d{4})", film)
    title, director, ortitle, year = info.group(1).title(), info.group(2),  info.group(3).title(), info.group(4)
    
    # Adding + to use in duckduckgo search pattern
    title = "+".join(title.split())
    director = "+".join(director.split())
    ortitle = "+".join(ortitle.split())
    
    # Find cinecartaz and imdb links
    # source = [(name of source, regex string to find the code of source, url to replace), etc]
    sources = [("cinecartaz", r"cinecartaz\.publico\.pt[\w/\-]+?(\d+)", "http://m.cinecartaz.publico.pt/Mobile/Filmes/Index/{}"), 
               ("imdb", r"imdb\.com\/title\/([\w\d]+)", "http://www.imdb.com/title/{}/fullcredits/") ]
    filmcodes = {}
    
    for source in sources:
        print("\nÀ procura em {}...".format(source[0]))
        
        duck_url = 'http://duckduckgo.com/html/?q={}+"{}"+{}+{}'.format(source[0], ortitle, director, year)
        print(duck_url)
        
        page = str(requests.get(duck_url).content)
        filmcode = source[2].format(re.search(source[1], page).group(1))
        print("Encontrado:", filmcode)
        
        filmcodes[source[0]] = filmcode
    
    # Format pages to ease the search
    cinecartaz = requests.get(filmcodes['cinecartaz'])
    cinecartaz = BeautifulSoup(cinecartaz.content, 'html.parser')
                   
    imdb = requests.get(filmcodes['imdb'])
    imdb = BeautifulSoup(imdb.content, 'html.parser')
    

    # Actors (cinecartaz)
    actores = re.findall(r'Actores[\n\r\t]([\w\s\-\'\,]*)[\n\r\t]Votar', cinecartaz.get_text())
    print(actores)
    actores = actores[0] if len(actores) > 0  else " "
    print("\n")
    print("Interpretação:", actores)
    
    # Writers (IMDB)
    argumento = re.search(r'(?<=Writing Credits).*?(?=Cast)', imdb.get_text(), flags=re.S)
    argumento = argumento.group() if argumento != None else " "
    argumento = ', '.join(re.findall(r'(\(?\w+(?:\s\w+)*\)?)', argumento))
    print("Argumento:", argumento)
    
    # Music (IMDB)
    musica = re.search(r'(?<=Music by).*?(?=Cinematography)', imdb.get_text(), flags=re.S)
    musica = musica.group() if musica != None else " "
    musica = ', '.join(re.findall(r'(\(?\w+(?:\s\w+)*\)?)', musica))
    print("Música:", musica)
    
    # Cinematography (IMDB)
    cinematografia = re.search(r'(?<=Cinematography by).*?(?=Film Editing)', imdb.get_text(), flags=re.S)
    cinematografia = cinematografia.group() if cinematografia != None else " "
    cinematografia = ', '.join(re.findall(r'(\(?\w+(?:\s\w+)*\)?)', cinematografia))
    print("Cinematografia:", cinematografia)
    
    # Editing (IMDB)
    edicao = re.search(r'(?<=Film Editing by).*?(?=\w+ [bB]y)', imdb.get_text(), flags=re.S)
    edicao = edicao.group() if edicao != None else " "
    edicao = ', '.join(re.findall(r'(\(?\w+(?:\s\w+)*\)?)', edicao))
    print("Edição:", edicao)
    
    # Sinopse (CINECARTAZ)
    sinopse = cinecartaz.find(id="ContentDescription")
    sinopse = sinopse.get_text()[:-9] if sinopse != None else " "
    print("\nSinopse:", sinopse)

    return actores, argumento, musica, cinematografia, edicao, sinopse

sheet(films)
