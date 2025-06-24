# import time
import api_utils
import data_utils

#------------------------------- MAIN -----------------------------

# Credenciales para el uso del API: username, API Key y URL del torneo
usuario = "BurningKnuckle"
apiKey = "8wvK5aoyASVddO1xttkrVWyCNKlpsxYdvnFluIF3"
tourneyUrl = "nnnijihigdrgser"

# Inicializacion del archivo CSV con los datos del torneo, jugadores y partidas
dfTorneo, estatusTorneo = data_utils.inicializar_archivos("SAMATekkenLeague/challongeAPI/torneo.csv")
dfJugadores, estatusJugadores = data_utils.inicializar_archivos("SAMATekkenLeague/challongeAPI/jugadores.csv")
dfPartidas, estatusPartidas = data_utils.inicializar_archivos("SAMATekkenLeague/challongeAPI/partidas.csv", modo=2)

# Autenticacion para el API de Challonge
api_utils.login_challonge(usuario, apiKey)

# Menu principal
while(True):
    opcion = input("\nSeleccione una operacion: \n"
        "1. Mostrar datos del ultimo torneo registrado\n"
        "2. Cambiar el URL del torneo\n"
        "3. Obtener informacion general del torneo\n"
        "4. Obtener informacion general de los jugadores\n"
        "5. Obtener historial del torneo para cada jugador\n"
        "6. Generar todos los archivos de registro para este torneo\n"
        "7. Salir\n")
    if opcion == "1":
        if estatusTorneo == 'ok_empty':
            print("El archivo de registro de torneos esta vacio")
        else:
            print("Datos del ultimo torneo: ")
            data_utils.mostrardf(dfTorneo)
        if estatusJugadores == 'ok_empty':
            print("\nEl archivo de registro de participantes esta vacio")
        else:
            print("\nDatos de los participantes: ")
            data_utils.mostrardf(dfJugadores)
        if estatusPartidas == 'ok_empty':
            print("\nEl archivo de historial de peleas esta vacio")
        else:
            print("\nHistorial de partidas por jugador: ")
            data_utils.mostrardf(dfPartidas, modo=2)
    elif opcion == "2":
        tourneyUrl = input("\nIngrese la nueva URL del torneo: \n") 
        print("¡Cambio registrado con exito!")
    elif opcion == "3":
        api_utils.mostrar_info_torneo(tourneyUrl)
        opcionTorneo = input("\n¿Desea actualizar el registro del torneo? (y/n): \n")
        if opcionTorneo == 'y':
            dfTorneo, estatusTorneo = data_utils.crear_registro(tourneyUrl, "torneo")
    elif opcion == "4":
        api_utils.mostrar_info_jugadores(tourneyUrl)
        opcionJugadores = input("\n¿Desea actualizar el registro de los jugadores? (y/n): \n")
        if opcionJugadores == 'y':
            dfJugadores, estatusJugadores = data_utils.crear_registro(tourneyUrl, "jugadores")
    elif opcion == "5":
        api_utils.mostrar_info_partidas(tourneyUrl)
        opcionPartidas = input("\n¿Desea actualizar el registro de las partidas? (y/n): \n")
        if opcionPartidas == 'y':
            dfPartidas, estatusPartidas = data_utils.crear_registro(tourneyUrl, "partidas")
    elif opcion == "6":
        print('\nCreando registro del torneo...\n')
        dfTorneo, estatusTorneo = data_utils.crear_registro(tourneyUrl, "torneo")
        print('\nCreando registro de los jugadores...\n')
        dfJugadores, estatusJugadores = data_utils.crear_registro(tourneyUrl, "jugadores")
        print('\nCreando registro de partidas...\n')
        dfPartidas, estatusPartidas = data_utils.crear_registro(tourneyUrl, "partidas")
    elif opcion == "7":
        print("¡Adiós!")
        break
    else:
        print("ERROR: Ingrese una opción válida del menú.\n")

