import challonge
import pandas as pd
import threading, concurrent.futures

# Funcion para establecer los credenciales de Challonge.
def login_challonge(usuario, apiKey):
    challonge.set_credentials(usuario, apiKey)

"""
Tournaments/Show: Muestra informacion de un torneo usando su URL
Ref: https://api.challonge.com/v1/documents/tournaments/show
Algunos atributos de interes:
name
id
url
tournament_type
progress_meter
participants_count
tie_breaks
allow_participant_match_reporting
hide_bracket_preview

Cuando se usa la opcion 'include_participants = 1' en el API call, se crea un subdiccionario bajo el nombre 'participant{}' para cada jugador registrado.
Algunos atributos de interes:
id
name
seed

Cuando se usa la opcion 'include_matches = 1' en el API call, se crea un array de subdiccionarios llamado 'matches[]', que incluye un diccionario para cada match jugado llamado 'match{}'.
Algunos atributos de interes:
id
tournament_id
player1_id
player2_id
winner_id
loser_id
round
scores_csv
started_at
created_at
updated_at: '2025-06-16T21:22:09.489+02:00'
completed_at
suggested_play_order
forfeited
"""
def info_torneo(tourneyUrl):
    try:
        torneo = challonge.tournaments.show(tourneyUrl)
        print(f"\nNombre del torneo: {torneo['name']}")
        print(f"ID del torneo: {torneo['id']}")
        print(f"Formato del torneo: {torneo['tournament_type']}")
        print(f"Progreso del torneo: {torneo['progress_meter']}%")
        print(f"Cantidad de participantes: {torneo['participants_count']}")
        print(f"Mecanismos de desempate: {torneo['tie_breaks']}")
        print(f"Permitir que los participantes reporten sus matches: {torneo['allow_participant_match_reporting']}")
        print(f"Esconder el preview del bracket: {torneo['hide_bracket_preview']}")
    except Exception as e:
        print(f"Error al hacer el llamado API: {e}")

"""
Participants/Index: Muestra parametros importantes de todos los participantes de un torneo a partir de su URL
Ref: https://api.challonge.com/v1/documents/participants/index
Algunos atributos de interes:
id
name
seed
"""
def info_participantes(tourneyUrl):
    try:
        participantes = challonge.participants.index(tourneyUrl)
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

Cuando se usa la opcion 'include_matches = 1' en el API call, se crea un array de subdiccionarios llamado 'matches[]', que incluye un diccionario para cada match jugado llamado 'match{}'.
Algunos atributos de interes:
id
tournament_id
player1_id
player2_id
winner_id
loser_id
round
scores_csv
started_at
created_at
updated_at: '2025-06-16T21:22:09.489+02:00'
completed_at
suggested_play_order
forfeited
"""
def info_participantes(tourneyUrl, id="265220791"):
    try:
        participante = challonge.participants.show(tourneyUrl, id, include_matches = 1)
        print(participante['match'])

        #for datos in participante:
            #print(f"Nombre del jugador: {datos['name']}, ID: {datos['id']}, Seed: {datos['seed']}")
    except Exception as e:
       print(f"Error al hacer el llamado API: {e}")



# thread_local = threading.local()

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
