import challonge
import pandas as pd

# Credenciales para el uso del API: username, API Key y URL del torneo.
usuario = "BurningKnuckle"
apiKey = "8wvK5aoyASVddO1xttkrVWyCNKlpsxYdvnFluIF3"
tourneyUrl = "nnnijihigdrgser"

challonge.set_credentials(usuario, apiKey)

try:
    torneo = challonge.tournaments.show(tourneyUrl, include_participants = 1, include_matches = 1)
    # print(len(tournament.keys()))
    # print(f"\nNombre del Torneo: {tournament['name']}")
    # print(f"ID del Torneo: {tournament['id']}")
    # print(f"Formato del Torneo: {tournament['tournament_type']}")
    # print(f"Cantidad de Participantes: {tournament['participants_count']}")
    # print(f"Allow Participant Match Reporting: {tournament['allow_participant_match_reporting']}")
    # print(f"Hide Bracket Preview: {tournament['hide_bracket_preview']}")
    # print(f"Mecanismos de desempate: {tournament['tie_breaks']}")
    # print(type(tournament['tie_breaks']))
    # print(len(tournament['tie_breaks']))
    # print(f"Mecanismos de desempate: {tournament['tie_breaks'][0]}")
    # print(type(tournament['tie_breaks'][0]))

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
    dfTorneo = pd.DataFrame(torneo)
    print(dfTorneo.to_string())

except Exception as e:
    print(f"Error al hacer el llamado API: {e}")


# empates=""
# for item in torneo['tie_breaks']:
#     empates += item
# print(empates)

# try:
#     participantes = challonge.participants.index(tourneyUrl)
#     for participante in participantes:
#         print(f"Nombre del jugador: {participante['name']}, ID: {participante['id']}, Seed: {participante['seed']}")
# except Exception as e:
#     print(f"Error al hacer el llamado API: {e}")

    