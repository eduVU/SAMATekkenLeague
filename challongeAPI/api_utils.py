import challonge
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
empates(Str)
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
"""
def info_participantes(tourneyUrl):
    try:
        participantes = challonge.participants.index(tourneyUrl)
        print(len(participantes))
        for participante in participantes:
            print(f"Nombre del jugador: {participante['name']}, ID: {participante['id']}, Seed: {participante['seed']}")
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
lista de N matches jugados. Cada match es un diccionario en si, con 33 atributos propios de cada match.
Algunos atributos de interes:
id
tournament_id
state: open, closed, pending
player1_id
player2_id
winner_id
loser_id
round: numero de round en el torneo (jornada 1, por ejemplo)
scores_csv: marcadores del match
started_at
created_at
updated_at: '2025-06-16T21:22:09.489+02:00'
completed_at
suggested_play_order: numero de encuentro sugerido por challonge
forfeited
"""
def historial_participantes(tourneyUrl, id="265220791"):
    try:
        participante = challonge.participants.show(tourneyUrl, id, include_matches = 1)  # Diccionario con la info de cada jugador.
        # print(participante['matches'])  # Lista de diccionarios con la info de cada match por separado.
        # print(participante['matches'][0]['match'])  # Diccionario para cada match.
        print(participante['matches'][0]['match']['round'])  
        print(participante['matches'][0]['match']['suggested_play_order'])  
        print(participante['matches'][0]['match']['state'])  

        # for datos in participante['matches']:  # Se recorre la lista de atributos para cada match
        #     print(datos['match'])
        #     print(type(datos))
    except Exception as e:
       print(f"Error al hacer el llamado API: {e}")

"""
Matches/Index: Muestra 33 parametros de los matches jugados o pendientes partir del URL del torneo
Ref: https://api.challonge.com/v1/documents/matches/index
Algunos atributos de interes:
id
tournament_id
state: open, closed, pending
player1_id
player2_id
winner_id
loser_id
round: numero de round en el torneo (jornada 1, por ejemplo)
scores_csv: marcadores del match
started_at
created_at
updated_at: '2025-06-16T21:22:09.489+02:00'
completed_at
suggested_play_order: numero de encuentro sugerido por challonge
forfeited

Utilizando el atributo 'participant_id=<player_id>' se pueden filtrar los matches de un jugador en específico.
"""
def info_matches(tourneyUrl):
    try:
        matches = challonge.matches.index(tourneyUrl)  # Diccionario con la info de cada jugador.
        # print(matches)  # Listado de diccionarios.
        # print(matches[0])  # Cada elemento de la lista de matches es un diccionario con la info del match.

        # for datos in participante['matches']:  # Se recorre la lista de atributos para cada match
        #     print(datos['match'])
        #     print(type(datos))
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
