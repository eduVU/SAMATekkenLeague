import challonge
import pandas as pd
import numpy as np

# Credenciales para el uso del API: username, API Key y URL del torneo.
usuario = "BurningKnuckle"
apiKey = "8wvK5aoyASVddO1xttkrVWyCNKlpsxYdvnFluIF3"
tourneyUrl = "nnnijihigdrgser"

challonge.set_credentials(usuario, apiKey)

# Tests del torneo
# try:
#     # Se extrae toda la info del torneo en un diccionario
#     torneo = challonge.tournaments.show(tourneyUrl)

#     # Se manipulan las entradas de 'Tie breaks' para que quepan en una sola fila
#     empates=""
#     for i in range(len(torneo['tie_breaks'])):
#         if i == 0:
#             empates = "".join([empates, torneo['tie_breaks'][i]])
#         else:
#             empates = ", ".join([empates, torneo['tie_breaks'][i]])

#     # Se conservan solo los parametros de interes
#     torneo = {
#         "Nombre": torneo['name'],
#         "ID":torneo['id'],
#         "URL": torneo['url'],
#         "Formato": torneo['tournament_type'],
#         "Progreso": str(torneo['progress_meter'])+"%",
#         "Participantes": torneo['participants_count'],
#         "Mecanismos de desempate": empates,
#         "Reporte de propios matches": torneo['allow_participant_match_reporting'],
#         "Esconder bracket": torneo['hide_bracket_preview']
#     }
#     df = pd.Series(torneo)
#     print(df.to_string())
# except Exception as e:
#     print(f"Error al hacer el llamado API: {e}")

# --------------------------------------------------------
# Tests de los participantes
# try:
#     # Se extrae toda la info de los participantes en una lista
#     participantes = challonge.participants.index(tourneyUrl)
#     # print(participantes)

#     # Diccionario que va a contener subdiccionarios para cada participante
#     jugadores = {}

#     # Se crea un diccionario con los datos relevantes de cada participante y se agrega al diccionario principal
#     for i in range(len(participantes)):
#         jugadores[str(i+1)] = {
#             "Nombre": participantes[i]['name'],
#             "ID": participantes[i]['id'],
#             "Seed": participantes[i]['seed'],
#         }

#     # print(jugadores)
#     df = pd.DataFrame(jugadores)
#     print(df.transpose().to_string())

# except Exception as e:
#     print(f"Error al hacer el llamado API: {e}")

#-----------------------------------------------------------
# Tests de las partidas
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
state: open, closed, pending
player1_id
player2_id
winner_id
round: numero de round en el torneo (jornada 1, por ejemplo)
scores_csv: marcadores del match
suggested_play_order: numero de encuentro sugerido por challonge

Parametros:

"""
try:
    jugadores = challonge.participants.index(tourneyUrl)  # Se llama a este API para obtener el id de cada jugador
    # Rutina para crear un diccionario de IDs y nombres de los jugadores del torneo
    idsJugadores = {}
    for jugador in jugadores:
        idsJugadores[jugador['id']] = jugador['name']
    historialTotal = {}  # Este diccionario tendra un subdiccionario para cada jugador y sus partidas
 
    # Se llama a este API para obtener las partidas de cada jugador segun su ID
    for id in idsJugadores:
        historialIndividual = {}  # Este diccionario tendra el historial de partidas de un solo jugador
        partidas = challonge.participants.show(tourneyUrl, id, include_matches=1)  # Lista de diccionarios con la info de todas las partidas para cada jugador.
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
                    print('     Resultado: Victoria')
                else:
                    print('     Resultado: Derrota')
                print(f"     Marcadores: {partida['match']['scores_csv']}")
                # Rutina logica para determinar la diferencia de rounds para esta pelea
                roundsJ1 = []
                roundsJ2 = []
                roundsTotales = []
                sets = partida['match']['scores_csv'].split(',')
                for pelea in sets:
                    roundsTotales = pelea.split('-')
                    roundsJ1.append(int(roundsTotales[0]))
                    roundsJ2.append(int(roundsTotales[1]))
                roundsJ1 = np.array(roundsJ1)
                roundsJ2 = np.array(roundsJ2)
                diferenciaRelativa = roundsJ1.sum() - roundsJ2.sum()
                if orden == 'segundo':
                    diferenciaRelativa *= -1
                print(f"     Diferencia de rounds: {diferenciaRelativa}")

                
                
                
                
        print("\n")

except Exception as e:
    print(f"Error al hacer el llamado API: {e}")

#-----------------------------------------------------------

# Ejemplo de DataFrame con diccionario anidado
# empleados = {
#     "departamento_ventas": {
#         "empleado1": {
#             "nombre": "Ana",
#             "edad": 30,
#             "cargo": "Vendedor"
#         },
#         "empleado2": {
#             "nombre": "Luis",
#             "edad": 25,
#             "cargo": "Gerente de ventas"
#         }
#     },
#     "departamento_marketing": {
#         "empleado3": {
#             "nombre": "Carlos",
#             "edad": 28,
#             "cargo": "Marketing Manager"
#         }
#     }
# }

# df = pd.DataFrame(empleados)
# print(df.to_string())



