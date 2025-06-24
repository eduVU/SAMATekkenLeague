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
# try:
#     historialTotal = []  # Esta lista tendra un diccionario para cada jugador y sus partidas
#     jugadores = challonge.participants.index(tourneyUrl)  # Se llama a este API para obtener el id de cada jugador
#     # Rutina logica para obtener todos los datos de las partidas para cada jugador
#     for jugador in jugadores:
#         partidas = challonge.participants.show(tourneyUrl, jugador['id'], include_matches=1)  # Lista de diccionarios con la info de todas las partidas para un solo jugador

#         # Se accede a cada registro de peleas para un jugador, una a una
#         for partida in partidas['matches']:
#             historialIndividual = {}  # Este diccionario tendra el historial de partidas de un solo jugador
#             # Solo se muestran las partidas que ya se jugaron
#             if partida['match']['state'] == 'complete':
#                 historialIndividual['Jugador'] = partidas['name']  # Se agrega el nombre del jugador consultado al historial individual
#                 historialIndividual['Ronda'] = partida['match']['round']  # Se agrega la ronda al historial individual
#                 historialIndividual['No. Partida'] = partida['match']['suggested_play_order']  # Se agrega el no. de pelea al historial individual

#                 # Rutina logica para determinar el nombre del oponente de cada ronda
#                 if partida['match']['player1_id'] == jugador['id']:
#                     orden = "primero"
#                     datosOponente = challonge.participants.show(tourneyUrl, partida['match']['player2_id'])
#                     oponente = datosOponente['name']
#                 else:
#                     orden = "segundo"
#                     datosOponente = challonge.participants.show(tourneyUrl, partida['match']['player1_id'])
#                     oponente = datosOponente['name']
#                 historialIndividual['Oponente'] = oponente  # Se agrega el nombre del oponente al historial individual

#                 # Rutina logica para determinar si el jugador fue el vencedor de la pelea
#                 if partida['match']['winner_id'] == jugador['id']:
#                     resultado = 'Victoria'
#                 else:
#                     resultado = 'Derrota'
#                 historialIndividual['Resultado'] = resultado  # Se agrega el resultado de la pelea al historial individual

#                 # Rutina logica para registrar el resultado de cada set en un campo aparte
#                 sets = partida['match']['scores_csv'].split(',')
#                 for i in range(len(sets)):
#                     historialIndividual[f'Set {i+1}'] = sets[i]  # Se agrega el resultado de cada set al historial individual

#                 # Rutina logica para determinar la diferencia de rounds para esta pelea
#                 roundsJ1 = []
#                 roundsJ2 = []
#                 roundsTotales = []
#                 for pelea in sets:
#                     roundsTotales = pelea.split('-')  # roundsTotales almacena los runds de J1 y los del J2, ej [3, 1]
#                     roundsJ1.append(int(roundsTotales[0]))  # La primera posicion corresponde al J1
#                     roundsJ2.append(int(roundsTotales[1]))  # La segunda posicion corresponde al J2
#                 rondasJ1 = np.array(roundsJ1)
#                 rondasJ2 = np.array(roundsJ2)
#                 diferenciaRelativa = rondasJ1.sum() - rondasJ2.sum()  # Diferencia de rounds considerando que el jugador es J1
#                 # Ajuste en caso de que el jugador sea J2
#                 if orden == 'segundo':
#                     diferenciaRelativa *= -1
#                 historialIndividual['Diferencia de rounds'] = diferenciaRelativa  # Se agrega la diferencia relativa de rounds al historial individual
#                 historialTotal.append(historialIndividual)  # Al historial total se agregan los datos del jugador consultado

#     df = pd.DataFrame(historialTotal)
#     print(df.to_string(index=False))

# except Exception as e:
#     print(f"Error al hacer el llamado API: {e}")

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



