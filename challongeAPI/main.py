# import time
import api_utils

#------------------------------- MAIN -----------------------------

# Credenciales para el uso del API: username, API Key y URL del torneo.
usuario = "BurningKnuckle"
apiKey = "8wvK5aoyASVddO1xttkrVWyCNKlpsxYdvnFluIF3"
tourneyUrl = "nnnijihigdrgser"

api_utils.login_challonge(usuario, apiKey)  # Autenticacion para el API

while(True):
    opcion = input("\nSeleccione una operacion: \n"
        "1. Cambiar el URL del torneo.\n"
        "2. Obtener informacion general del torneo.\n"
        "3. Obtener informacion general de los jugadores.\n"
        "4. Obtener historial del torneo para cada jugador.\n"
        "7. Salir.\n")
    if opcion == "1":
        tourneyUrl = input("\nIngrese la nueva URL del torneo: \n") 
        print("¡Cambio registrado con exito!")       
    elif opcion == "2":
        api_utils.info_torneo(tourneyUrl)    
    elif opcion == "3":
        api_utils.info_participantes(tourneyUrl)
    elif opcion == "4":
        api_utils.historial_participantes(tourneyUrl)
    elif opcion == "7":
        print("¡Adiós!")
        break
    else:
        print("ERROR: Ingrese una opción válida del menú.\n")





# # inicio = time.time()
# # api_utils.tourney_ids(apiKey)
# # tiempo = time.time() - inicio
# # print(f"Duración del proceso: {tiempo} s")

# # # Tiempo estimado: 
