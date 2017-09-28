# IMPORTS

import re

# DATE OF SESSIONS, LIST OF FILMS

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

films = [film for film in films.split("\n") if len(film) > 1] # Removes empty strings in the list.
films = list(zip(films[::2], films[1::2]))

# FUNCTIONS

def sheet(films):
    """
    It prints a sheet from a list of films. Each entry has the following format:
    
    Dia 30 – A FÁBRICA DE NADA, de Pedro Pinho
    (POR, 2017, 177', M/12)
    
    The sheet is formated as specified by 'heads'.
    
    """
    
    heads = """
/////////////////////////////////////////////////////////

{}
{}

Interpretação: 
Argumento: 
Música: 
Cinematografia:
Edição: 

Sinopse: 

Crítica: 



"""
    aonorte = open('AoNorte_' + date[0] + "_" + date[1] + '.txt','w')
    aonorte.write('SESSÕES CINECLUBISTAS AO NORTE | ' + date[1] + ' de ' + date[0] + "\n")
    
    print("\nWriting to file '" + aonorte.name + "':\n")
    
    for film in films:
        print(film[0])
        aonorte.write(heads.format(film[0], film[1]))
        
        print("Director: {} | Title: {} | Year: {}".format(*filminfo(film)))
        
    aonorte.close()
    print("\nDone!")
    
def filminfo(film):
    """
    From each film entry in the following format:
    
    Dia 20 – OS CHAPÉUS-DE-CHUVA DE CHERBURG, de Jacques Demy
    (Les Parapluies de Cherbourg, FRA, 1964, 90', M/12)
    
    It grabs the Original Title, Director, and Year and returns a tuple:
    (Director, Original Title, Year)
    """
    film = film[0]+ " " + film[1]
    info = re.search(r",\s?d?e? ([\w\s]*)\s\(([\w\s]*).*(\d{4})", film)
    return (info.group(1), info.group(2).title(), info.group(3))
    
sheet(films)
#filminfo(film)
