import challonge
import numpy as np
import threading, concurrent.futures

# thread_local = threading.local() 
# Inicializacion del threading

""" 
Funcion para establecer los credenciales de Challonge.

Parametros:
usuario(Str): username de Challonge
apiKey(Str): API Key unica creada para el usuario
"""
def login_challonge(usuario, apiKey):
    challonge.set_credentials(usuario, apiKey)

"""
Tournaments/Show: Muestra en la terminal la informacion de un torneo usando su URL
Ref: https://api.challonge.com/v1/documents/tournaments/show
Se muestran 98 distintos parametros del torneo, algunos atributos de interes:
name
id
url
tournament_type
progress_meter
participants_count
tie_breaks: metodos elegidos como criterio de desempate
allow_participant_match_reporting: permitir o no que cada jugador reporte sus propios resultados
hide_bracket_preview: esconder el bracket hasta que el torneo inicie

Parametros:
tourneyUrl(Str): URL del torneo, generada por Challonge
torneo(Dict): diccionario con todos los parametros del torneo
"""
def mostrar_info_torneo(tourneyUrl):
    try:
        torneo = challonge.tournaments.show(tourneyUrl)
        print(f"\nNombre del torneo: {torneo['name']}")
        print(f"ID del torneo: {torneo['id']}")
        print(f"URL del torneo: {torneo['url']}")
        print(f"Formato del torneo: {torneo['tournament_type']}")
        print(f"Progreso del torneo: {torneo['progress_meter']}%")
        print(f"Cantidad de participantes: {torneo['participants_count']}")
        print(f"Mecanismos de desempate: ")
        for item in torneo['tie_breaks']:
            print("              "+item)
        print(f"Permitir que los participantes reporten sus matches: {torneo['allow_participant_match_reporting']}")
        print(f"Esconder el preview del bracket: {torneo['hide_bracket_preview']}")
    except Exception as e:
        print(f"Error al hacer el llamado API: {e}")

"""
Esta funcion obtiene la info del torneo en un formato mas estructurado y la devuelve en forma de diccionario

Parametros:
tourneyUrl(Str): URL del torneo, generada por Challonge
torneo(Dict): diccionario con todos los parametros del torneo
empates(Str): en esta variable se guardan todos los mecanismos de desempate en un solo string para mejor presentacion de los datos
"""
def obtener_datos_torneo(tourneyUrl):
    try:
        # Se extrae toda la info del torneo en un diccionario
        torneo = challonge.tournaments.show(tourneyUrl)

        # Se manipulan las entradas de 'Tie breaks' para que quepan en una sola fila
        empates=""
        for i in range(len(torneo['tie_breaks'])):
            if i == 0:
                empates = "".join([empates, torneo['tie_breaks'][i]])
            else:
                empates = ", ".join([empates, torneo['tie_breaks'][i]])

        # Se conservan solo los parametros de interes
        torneo = {
        "Nombre": [torneo['name']],
        "ID":[torneo['id']],
        "URL": [torneo['url']],
        "Formato": [torneo['tournament_type']],
        "Progreso": [str(torneo['progress_meter'])+"%"],
        "Participantes": [torneo['participants_count']],
        "Mecanismos de desempate": [empates],
        "Reporte de propios matches": [torneo['allow_participant_match_reporting']],
        "Esconder bracket": [torneo['hide_bracket_preview']]
        }
        return torneo
    except Exception as e:
        print(f"Error al hacer el llamado API: {e}")

"""
Participants/Index: Muestra 11 parametros importantes de todos los participantes de un torneo a partir de su URL
Ref: https://api.challonge.com/v1/documents/participants/index
Algunos atributos de interes:
id
name
seed

Parametros:
tourneyUrl(Str): URL del torneo por consultar
participantes(List): listado de participantes del torneo
participantes[i](Dict): diccionario con los datos de un participante en particular
"""
def mostrar_info_jugadores(tourneyUrl):
    try:
        participantes = challonge.participants.index(tourneyUrl)
        print(f"Este torneo cuenta con {len(participantes)} participantes: \n")
        for participante in participantes:
            print(f"Nombre: {participante['name']}, ID: {participante['id']}, Seed: {participante['seed']}")
    except Exception as e:
       print(f"Error al hacer el llamado API: {e}")

"""
Esta funcion obtiene la info de los participantes en un formato mas estructurado y la devuelve en forma de diccionario

Parametros:
tourneyUrl(Str): URL del torneo, generada por Challonge
participantes(List): listado de participantes del torneo y su informacion obtenida del API
jugadores(Dict): diccionario anidado con los datos de cada jugador
nombre(Str): nombre de cada jugador, sirve como key de cada diccionario y para crear el index del DataFrame
"""
def obtener_datos_jugadores(tourneyUrl):
    try:
        # Se extrae la información de los participantes
        participantes = challonge.participants.index(tourneyUrl)

        # Diccionario con los participantes, donde la clave es el nombre del jugador
        jugadores = {}
        for player in participantes:
            nombre = player['name']
            jugadores[nombre] = {
                "ID": player['id'],
                "Seed": player['seed'],
            }
        return jugadores
    except Exception as e:
        print(f"Error al hacer el llamado API: {e}")

"""
Participants/Show: Muestra parametros especificos de un participante a partir de su ID y del URL del torneo
Ref: https://api.challonge.com/v1/documents/participants/show
Algunos atributos de interes:
id
name
seed

Cuando se usa la opcion 'include_matches = 1' en el API call, se crea una entrada del diccionario llamada 'matches{}', que contiene una 
lista de N matches jugados. Cada match es un diccionario en si, con 33 atributos propios de cada match
Algunos atributos de interes:
state: open, closed, pending
player1_id
player2_id
winner_id
round: numero de round en el torneo (jornada 1, por ejemplo)
scores_csv: marcadores del match
suggested_play_order: numero de encuentro sugerido por challonge

Parametros:
tourneyUrl(Str): URL del torneo, generada por Challonge
jugadores(Dict): diccionario con todos los jugadores del torneo obtenidos por API
idsJugadores(Dict): diccionario depurado que contiene los pares id:nombre para cada jugador
partidas(List): lista de diccionarios con la info de todas las partidas para cada jugador
orden(Str): almacena el orden del jugador consultado en cada pelea (J1 o J2)
oponente(Str): almacena el orden del jugador rival en cada pelea (J1 o J2)
resultado(Str): almacena el resultado del match para el jugador consultado (Victoria o Derrota)
sets(List): lista con los marcadores de las peleas de cada match (ej: 3-1)
roundsTotales(List): listado de los rounds ganados por cada jugador, obtenidos al depurar la informacion los marcadores
roundsJ1(List): listado con los rounds ganados por el jugador 1 en cada pelea
roundsJ2(List): listado con los rounds ganados por el jugador 2 en cada pelea
rondasJ1(NumpyArray): array de enteros creado a partir de la lista roundsJ1
rondasJ2(NumpyArray): array de enteros creado a partir de la lista roundsJ2
diferenciaRelativa(Int): valor de la diferencia de rounds obtenida para el jugador consultado en cada match (diferencia = rounds ganados - rounds perdidos)
"""
def mostrar_info_partidas(tourneyUrl):
    try:
        jugadores = challonge.participants.index(tourneyUrl)  # Se llama a este API para obtener el id de cada jugador
        # Rutina para crear un diccionario de IDs y nombres de los jugadores del torneo
        idsJugadores = {}
        for jugador in jugadores:
            idsJugadores[jugador['id']] = jugador['name']
    
        # Se llama a este API para obtener las partidas de cada jugador segun su ID
        for id in idsJugadores:
            partidas = challonge.participants.show(tourneyUrl, id, include_matches=1)  # Lista de diccionarios con la info de todas las partidas para cada jugador
            print(f"Jugador: {partidas['name']}")

            # Se accede a cada registro de peleas por jugador, uno a uno
            for partida in partidas['matches']:
                # Solo se muestran las partidas que ya se jugaron
                if partida['match']['state'] == 'complete':
                    print(f"Ronda: {partida['match']['round']}")
                    print(f"     No. Partida: {partida['match']['suggested_play_order']}")

                    # Rutina logica para determinar el nombre del oponente de cada ronda
                    if partida['match']['player1_id'] == id:
                        orden = "primero"
                        oponente = idsJugadores.get(partida['match']['player2_id'])
                    else:
                        orden = "segundo"
                        oponente = idsJugadores.get(partida['match']['player1_id'])
                    print(f"     Oponente: {oponente}")
                    
                    # Rutina logica para determinar si el jugador fue el vencedor de la pelea
                    if partida['match']['winner_id'] == id:
                        resultado = 'Victoria'
                    else:
                        resultado = 'Derrota'
                    print(f'     Resultado: {resultado}')
                    print(f"     Marcadores: {partida['match']['scores_csv']}")

                    roundsJ1 = []
                    # Rutina logica para determinar la diferencia de rounds para esta pelea
                    roundsJ2 = []
                    roundsTotales = []
                    sets = partida['match']['scores_csv'].split(',')
                    for pelea in sets:
                        roundsTotales = pelea.split('-')  # roundsTotales almacena los runds de J1 y los del J2, ej [3, 1]
                        roundsJ1.append(int(roundsTotales[0]))  # La primera posicion corresponde al J1
                        roundsJ2.append(int(roundsTotales[1]))  # La segunda posicion corresponde al J2
                    rondasJ1 = np.array(roundsJ1)
                    rondasJ2 = np.array(roundsJ2)
                    diferenciaRelativa = rondasJ1.sum() - rondasJ2.sum()  # Diferencia de rounds considerando que el jugador es J1
                    # Ajuste en caso de que el jugador sea J2
                    if orden == 'segundo':
                        diferenciaRelativa *= -1
                    print(f"     Diferencia de rounds: {diferenciaRelativa}")
            print("\n")
    except Exception as e:
        print(f"Error al hacer el llamado API: {e}")

"""
Esta funcion obtiene la info de las partidas de cada jugador en un formato mas estructurado y la devuelve en forma de lista de diccionarios

Parametros:
tourneyUrl(Str): URL del torneo, generada por Challonge
jugadores(Dict): diccionario con todos los jugadores del torneo obtenidos por API
partidas(List): lista de diccionarios con la info de todas las partidas para cada jugador
orden(Str): almacena el orden del jugador consultado en cada pelea (J1 o J2)
oponente(Str): almacena el orden del jugador rival en cada pelea (J1 o J2)
resultado(Str): almacena el resultado del match para el jugador consultado (Victoria o Derrota)
sets(List): lista con los marcadores de las peleas de cada match (ej: 3-1)
roundsTotales(List): listado de los rounds ganados por cada jugador, obtenidos al depurar la informacion los marcadores
roundsJ1(List): listado con los rounds ganados por el jugador 1 en cada pelea
roundsJ2(List): listado con los rounds ganados por el jugador 2 en cada pelea
rondasJ1(NumpyArray): array de enteros creado a partir de la lista roundsJ1
rondasJ2(NumpyArray): array de enteros creado a partir de la lista roundsJ2
diferenciaRelativa(Int): valor de la diferencia de rounds obtenida para el jugador consultado en cada match (diferencia = rounds ganados - rounds perdidos)
historialTotal(List): lista con los diccionarios que contienen los datos de partidas para cada jugador
historialIndividual(Dict): diccionario volatil con los datos que se recolectan para cada jugador
"""
def obtener_datos_partidas(tourneyUrl):
    try:
        historialTotal = []  # Esta lista tendra un diccionario para cada jugador y sus partidas
        jugadores = challonge.participants.index(tourneyUrl)  # Se llama a este API para obtener el id de cada jugador
        # Rutina logica para obtener todos los datos de las partidas para cada jugador
        for jugador in jugadores:
            partidas = challonge.participants.show(tourneyUrl, jugador['id'], include_matches=1)  # Lista de diccionarios con la info de todas las partidas para un solo jugador

            # Se accede a cada registro de peleas para un jugador, una a una
            for partida in partidas['matches']:
                historialIndividual = {}  # Este diccionario tendra el historial de partidas de un solo jugador
                # Solo se muestran las partidas que ya se jugaron
                if partida['match']['state'] == 'complete':
                    historialIndividual['Jugador'] = partidas['name']  # Se agrega el nombre del jugador consultado al historial individual
                    historialIndividual['Ronda'] = partida['match']['round']  # Se agrega la ronda al historial individual
                    historialIndividual['No. Partida'] = partida['match']['suggested_play_order']  # Se agrega el no. de pelea al historial individual

                    # Rutina logica para determinar el nombre del oponente de cada ronda
                    if partida['match']['player1_id'] == jugador['id']:
                        orden = "primero"
                        datosOponente = challonge.participants.show(tourneyUrl, partida['match']['player2_id'])
                        oponente = datosOponente['name']
                    else:
                        orden = "segundo"
                        datosOponente = challonge.participants.show(tourneyUrl, partida['match']['player1_id'])
                        oponente = datosOponente['name']
                    historialIndividual['Oponente'] = oponente  # Se agrega el nombre del oponente al historial individual

                    # Rutina logica para determinar si el jugador fue el vencedor de la pelea
                    if partida['match']['winner_id'] == jugador['id']:
                        resultado = 'Victoria'
                    else:
                        resultado = 'Derrota'
                    historialIndividual['Resultado'] = resultado  # Se agrega el resultado de la pelea al historial individual

                    # Rutina logica para registrar el resultado de cada set en un campo aparte
                    sets = partida['match']['scores_csv'].split(',')
                    for i in range(len(sets)):
                        historialIndividual[f'Set {i+1}'] = sets[i]  # Se agrega el resultado de cada set al historial individual

                    # Rutina logica para determinar la diferencia de rounds para esta pelea
                    roundsJ1 = []
                    roundsJ2 = []
                    roundsTotales = []
                    for pelea in sets:
                        roundsTotales = pelea.split('-')  # roundsTotales almacena los runds de J1 y los del J2, ej [3, 1]
                        roundsJ1.append(int(roundsTotales[0]))  # La primera posicion corresponde al J1
                        roundsJ2.append(int(roundsTotales[1]))  # La segunda posicion corresponde al J2
                    rondasJ1 = np.array(roundsJ1)
                    rondasJ2 = np.array(roundsJ2)
                    diferenciaRelativa = rondasJ1.sum() - rondasJ2.sum()  # Diferencia de rounds considerando que el jugador es J1
                    # Ajuste en caso de que el jugador sea J2
                    if orden == 'segundo':
                        diferenciaRelativa *= -1
                    historialIndividual['Diferencia de rounds'] = diferenciaRelativa  # Se agrega la diferencia relativa de rounds al historial individual
                    historialTotal.append(historialIndividual)  # Al historial total se agregan los datos del jugador consultado
        return historialTotal
    except Exception as e:
        print(f"Error al hacer el llamado API: {e}")


# # Esta funcion crea una sesión de requests local para threading en caso de que no exista una.
# def crear_sesion():
#     if not hasattr(thread_local, "sesion"):
#         thread_local.sesion = req.Session()
#     return thread_local.sesion

# # Esta funcion hace un llamado API tipo GET a Challonge para obtener la info de los torneos creados.
# def tourney_ids(key):
#     sesion = crear_sesion()  # Crea una sesion para threading
#     url = f"https://api.challonge.com/v1/tournaments.json"
#     #headers = {"api_key": f"{key}"}
#     #with sesion.get(url, headers=headers) as info:
#     with sesion.get(url, headers=headers) as info:
#         print (info)
#         print(info.status_code)



# # Esta función hace un llamado al API y obtiene la info disponible para una película según su ID.
# def obtener_pelicula(id):
#     sesion = crear_sesion()  # Crea una sesión para threading.
#     url = f"https://api.themoviedb.org/3/movie/{id}?api_key=b096f7e1a5e3291eb3b771afa219d33e"
#     headers = {"accept": "application/json"}
#     with sesion.get(url, headers=headers) as pelicula:
#         return pelicula

# # Esta función hace el llamado al API usando la lista de ids dada y guarda el título, calificación y fecha de lanzamiento para 
# # cada película lanzada en el año 2000 o posterior.
# def llamar_api(ids):
#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#         peliculasValidas = {}  # Este diccionario contiene las películas lanzadas en el año 2000 o luego obtenidas del API.
#         indice = 0  # Contador para el nombre de las entradas del diccionario.
#         for i in range(ids):
#             executor.pelicula = obtener_pelicula(i)  # Llama al API y obtiene la ficha de datos de la película con el id dado.
#             if executor.pelicula.status_code == 200:
#                 anioLanzamiento = filtrar_fecha_lanzamiento(executor.pelicula.json()["release_date"])  # Filtra el año de lanzamiento de la película.
#                 chequeoTitulo = filtrar_titulo(executor.pelicula.json()["original_title"])  # Filtra el título de las películas que NO contengan "Action".
#                 if anioLanzamiento >= 2000 and chequeoTitulo == False: 
#                     peliculasValidas[f"{indice}"] = {"Titulo": executor.pelicula.json()["original_title"],
#                             "Calificación": executor.pelicula.json()["vote_average"],
#                             "Fecha_de_lazamiento": executor.pelicula.json()["release_date"]}
#                     indice = indice + 1
#     return peliculasValidas

# # Esta función reúne los datos del llamado al API y crea un DataFrame con la información obtenida.
# def crear_data_frame(ids):
#     listaPeliculas = llamar_api(ids)
#     tablaPeliculas=pd.DataFrame(listaPeliculas)  # La entrada "entries" del resultado del API es la que contiene la info importante en forma de una lista de diccionarios.
#     tablaTranspuesta = tablaPeliculas.T  # Transposición del dataframe para un manejo más sencillo del mismo.
#     return tablaTranspuesta
