import challonge

# Credenciales para el uso del API: username, API Key y URL del torneo.
usuario = "BurningKnuckle"
apiKey = "8wvK5aoyASVddO1xttkrVWyCNKlpsxYdvnFluIF3"
tourneyUrl = "nnnijihigdrgser"

challonge.set_credentials(usuario, apiKey)

try:
    tournament = challonge.tournaments.show(tourneyUrl, include_participants = 1, include_matches = 1)
    print(tournament)
    # print(f"\nNombre del Torneo: {tournament['name']}")
    # print(f"ID del Torneo: {tournament['id']}")
    # print(f"Formato del Torneo: {tournament['tournament_type']}")
    # print(f"Cantidad de Participantes: {tournament['participants_count']}")
    # print(f"Allow Participant Match Reporting: {tournament['allow_participant_match_reporting']}")
    # print(f"Hide Bracket Preview: {tournament['hide_bracket_preview']}")
except Exception as e:
    print(f"Error al hacer el llamado API: {e}")

try:
    participantes = challonge.participants.index(tourneyUrl)
    for participante in participantes:
        print(f"Nombre del jugador: {participante['name']}, ID: {participante['id']}, Seed: {participante['seed']}")
except Exception as e:
    print(f"Error al hacer el llamado API: {e}")

    