# import time
import api_utils
import data_utils

#------------------------------- MAIN -----------------------------

# Credenciales para el uso del API: username, API Key y URL del torneo
usuario = "BurningKnuckle"
apiKey = "8wvK5aoyASVddO1xttkrVWyCNKlpsxYdvnFluIF3"
tourneyUrl = "nnnijihigdrgser"

# Inicializacion del archivo CSV con los datos del torneo
dfTorneo, estatusTorneo = data_utils.inicializar_archivos("SAMATekkenLeague/challongeAPI/torneo.csv")

# Inicializacion del archivo CSV con los jugadores de la liga
dfJugadores, estatusJugadores = data_utils.inicializar_archivos("SAMATekkenLeague/challongeAPI/jugadores.csv")

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
        "6. Obtener de todos los encuentros\n"
        "7. Salir\n")
    if opcion == "1":
        if estatusTorneo == 'ok_empty':
            print("El archivo de registro de torneos esta vacio")
        else:
            data_utils.mostrardf(dfTorneo)
    elif opcion == "2":
        tourneyUrl = input("\nIngrese la nueva URL del torneo: \n") 
        print("¡Cambio registrado con exito!")
    elif opcion == "3":
        api_utils.mostrar_info_torneo(tourneyUrl)
        opcionTorneo = input("\n¿Desea actualizar el registro del torneo? (y/n): \n")
        if opcionTorneo == 'y':
            dfTorneo = data_utils.crear_registro_torneo(tourneyUrl)



    elif opcion == "3":
        api_utils.info_participantes(tourneyUrl)
    elif opcion == "4":
        api_utils.historial_participantes(tourneyUrl)
    elif opcion == "5":
        api_utils.info_matches(tourneyUrl)
    elif opcion == "7":
        print("¡Adiós!")
        break
    else:
        print("ERROR: Ingrese una opción válida del menú.\n")

