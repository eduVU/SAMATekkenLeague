import pandas as pd
import api_utils
import os

"""
Esta funcion abre y lee el archivo con los datos clave de cada jugador de la liga o del torneo
Si el archivo no existe, crea uno en blanco y notifica la accion

Parametros:
nombreArchivo(String): path relativo del archivo CSV
dfCsv(pd.DataFrame): DataFrame creado con la informacion del archivo CSV
estatus(String): "ok" significa que el archivo existe y no esta vacio. "ok_empty" indica que el archivo existe pero esta vacio
"""
def inicializar_archivos(nombreArchivo, modo=1):
    estatus = ""
    # Se verifica si el archivo existe
    if os.path.exists(nombreArchivo):
        # Si existe, se carga el contenido en un DataFrame
        try:
            if modo == 1:
                dfCsv = pd.read_csv(nombreArchivo, index_col=0)
            else:
                dfCsv = pd.read_csv(nombreArchivo)
            print(f"Archivo '{nombreArchivo}' cargado exitosamente.")
            estatus = "ok"
            return dfCsv, estatus
        except pd.errors.EmptyDataError as e:
            print(f"Advertencia: se ha encontrado el archivo '{nombreArchivo}', pero esta en blanco.")
            dfCsv = pd.DataFrame()  # Se inicializa un DataFrame vacio que corresponde al archivo CSV
            estatus = "ok_empty"
            return dfCsv, estatus
    else:
        # Si no existe, se crea un DataFrame vacio y se guarda como CSV
        dfCsv = pd.DataFrame()
        dfCsv.to_csv(nombreArchivo, index=False)
        print(f"El archivo '{nombreArchivo}' no existia, se ha creado un nuevo archivo vacio.")
        estatus = "ok_empty"
        return dfCsv, estatus


"""
Esta funcion muestra los contenidos de un DataFrame en la terminal

Parametros:
df(DataFrame): DataFrame de entrada
modo(Int): determina el modo en que se muestra el DataFrame, modo 1 incluye index=True y modo 2 usa index=False
"""
def mostrardf(df, modo=1):
    if modo == 1:
        print(df.to_string())
    else:
        print(df.to_string(index=False))


"""
Esta funcion crea un nuevo DataFrame con la informacion general del torneo consultado por medio de su URL

Parametros:
tourneyUrl(String): URL del torneo por consultar
modo(String): determina el tipo de registro que se desea ('torneo', 'jugadores', 'partidas')
datos(Dict): diccionario con toda la info recolectada mediante API
dfFinal(DataFrame): nuevo DataFrame con la informacion actualizada
estatusArchivo(Str): almacena el estado del archivo de registro asociado, "ok" significa que el archivo existe y no esta vacio
"""
def crear_registro(tourneyUrl, modo):
    if modo == "torneo":
        # Se obtiene un diccionario con los datos del torneo o de los jugadores
        datos = api_utils.obtener_datos_torneo(tourneyUrl)   
        # Se crea un DataFrame con los nuevos datos
        dfFinal = pd.DataFrame.from_dict(datos, orient='index', columns=["Settings Torneo"])
        # Se sobreescribe el archivo CSV correspondiente y se muestran los nuevos datos en la terminal
        dfFinal.to_csv("SAMATekkenLeague/challongeAPI/torneo.csv", index=True)
        print("El archivo 'SAMATekkenLeague/challongeAPI/torneo.csv' ha sido actualizado con los siguientes datos: \n")
        mostrardf(dfFinal)
    elif modo == "jugadores":
        datos = api_utils.obtener_datos_jugadores(tourneyUrl)
        dfFinal = pd.DataFrame.from_dict(datos, orient='index')
        # Asegurarse que el índice tenga nombre para que se guarde bien en el CSV
        dfFinal.index.name = "Nombre"
        dfFinal.to_csv("SAMATekkenLeague/challongeAPI/jugadores.csv", index=True)
        print("El archivo 'SAMATekkenLeague/challongeAPI/jugadores.csv' ha sido actualizado con los siguientes datos: \n")
        mostrardf(dfFinal)
    elif modo == 'partidas':
        datos = api_utils.obtener_datos_partidas(tourneyUrl)
        dfFinal = pd.DataFrame.from_dict(datos)
        dfFinal.to_csv("SAMATekkenLeague/challongeAPI/partidas.csv", index=False)
        print("El archivo 'SAMATekkenLeague/challongeAPI/partidas.csv' ha sido actualizado con los siguientes datos: \n")
        mostrardf(dfFinal, modo=2)
    estatusArchivo = "ok"
    return dfFinal, estatusArchivo
