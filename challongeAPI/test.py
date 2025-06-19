import challonge
import pandas as pd

# Credenciales para el uso del API: username, API Key y URL del torneo.
usuario = "BurningKnuckle"
apiKey = "8wvK5aoyASVddO1xttkrVWyCNKlpsxYdvnFluIF3"
tourneyUrl = "nnnijihigdrgser"

challonge.set_credentials(usuario, apiKey)

# Tests del torneo
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
        "Nombre": torneo['name'],
        "ID":torneo['id'],
        "URL": torneo['url'],
        "Formato": torneo['tournament_type'],
        "Progreso": str(torneo['progress_meter'])+"%",
        "Participantes": torneo['participants_count'],
        "Mecanismos de desempate": empates,
        "Reporte de propios matches": torneo['allow_participant_match_reporting'],
        "Esconder bracket": torneo['hide_bracket_preview']
    }
    df = pd.Series(torneo)
    print(df.to_string())
except Exception as e:
    print(f"Error al hacer el llamado API: {e}")


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



