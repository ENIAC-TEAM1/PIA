import requests
from collections import Counter
import matplotlib.pyplot as plt
import funct2 as fpro2
import os
from datetime import datetime

# Funcion que obtiene los datos principales del jugador
def datosUsuarioIngresado(jugador, region, params):
    try:
        # Request
        api_url_get_name = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{jugador}"
        response = requests.get(api_url_get_name, params=params)
        
        fpro2.guardar_consulta_api(api_url_get_name)
        
        response.raise_for_status()
        
        # Diccionario
        data = response.json()
        
        # Datos jugador
        print(f"\033[96mDatos del jugador {jugador}:\033[0m")
        print(f"\033[96mAccountId: {data['accountId']}\033[0m")
        print(f"\033[96mNivel: {data['summonerLevel']}\033[0m")
        input("Continuar?")
        
        # Retorna datos
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos del jugador: {e}")
        # Retorna none
        return None

# Funcion para mostrar datos de las ultimas 5 partidas
def verPartidas(datos, params):
    try:
        # Request
        api_url_get_match = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{datos['puuid']}/ids?start=0&count=5"
        response = requests.get(api_url_get_match, params=params)
        
        fpro2.guardar_consulta_api(api_url_get_match)
        
        # Diccionario
        data = response.json()
        i = 1
        
        # Crea variables en caso de requerir abrir un archivo de texto
        carpeta_reportes = 'Reportes'
        os.makedirs(carpeta_reportes, exist_ok=True)

        prefijo_archivo = f"reporte-partidas-{datos['name']}"
        patron_archivo = f"{prefijo_archivo}.*"
        siguiente_numero = fpro2.obtener_siguiente_numero_archivos(carpeta_reportes, patron_archivo)
        fecha_hora_actual = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        ruta_archivo_txt = os.path.join(carpeta_reportes, f"{prefijo_archivo}({siguiente_numero})_{fecha_hora_actual}.txt")
        
        # Variable para guardar detalles de la partida en una cadena para el archivo de texto
        detalles_partidas = f"JUGADOR: {datos['name']} - REPORTE PARTIDAS\n\n"
        
        for ele in data:
                try:
                    api_url_get_matches = f"https://americas.api.riotgames.com/lol/match/v5/matches/{ele}"
                    response = requests.get(api_url_get_matches, params=params)
                    
                    fpro2.guardar_consulta_api(api_url_get_matches)
                    
                    response.raise_for_status()
                    
                    data_for = response.json()
                    tiempopartida = (data_for['info']['gameDuration']//60)
                    # Imprimir detalles de la partida en la consola
                    print(f"\033[1;94mPARTIDA {i}:\033[0m")
                    print(f"  Duracion de la partida: {tiempopartida} minutos")
                    print(f"  Mode de juego: {data_for['info']['gameMode']}")
                    
                    jugadores = []
                    campeones = []

                    for e, jugador in enumerate(data_for['info']['participants']):
                        if datos['puuid'] == jugador['puuid']:
                            numjugador = e
                        jugadores.append(jugador['summonerName'])
                        campeones.append(jugador['championName'])
                    
                    if (data_for['info']['participants'][numjugador]['win']) == True:
                        print("\033[92m  Victoria\033[0m")
                    else:
                        print("\033[91m  Derrota\033[0m")
                    
                    print(f"  Kills: {data_for['info']['participants'][numjugador]['kills']}")
                    print(f"  Asistencias: {data_for['info']['participants'][numjugador]['assists']}")
                    print(f"  Muertes: {data_for['info']['participants'][numjugador]['deaths']}")
                    print(f"\033[93m  Oro ganado:\033[0m {data_for['info']['participants'][numjugador]['goldEarned']} \033[93mOro gastado:\033[0m {data_for['info']['participants'][numjugador]['goldSpent']}")
                    print(f"  Participantes: {jugadores}")
                    print(f"  Campeones Usados: {campeones}")
                    print("")
                    
                    tiempopartida = (data_for['info']['gameDuration']//60)
                    
                    detalles_partidas += f"PARTIDA {i}:"
                    detalles_partidas += f"  Duracion de la partida: {tiempopartida} minutos\n"
                    detalles_partidas += f"  Mode de juego: {data_for['info']['gameMode']}\n"
                    
                    if (data_for['info']['participants'][numjugador]['win']) == True:
                        detalles_partidas += "  Victoria"
                    else:
                        detalles_partidas += "  Derrota"
                    
                    detalles_partidas += f"  Kills: {data_for['info']['participants'][numjugador]['kills']}\n"
                    detalles_partidas += f"  Asistencias: {data_for['info']['participants'][numjugador]['assists']}\n"
                    detalles_partidas += f"  Muertes: {data_for['info']['participants'][numjugador]['deaths']}\n"
                    detalles_partidas += f"  Oro ganado: {data_for['info']['participants'][numjugador]['goldEarned']} Oro gastado: {data_for['info']['participants'][numjugador]['goldSpent']}\n"
                    detalles_partidas += f"  Participantes: {jugadores}\n"
                    detalles_partidas += f"  Campeones Usados: {campeones}\n\n"
                    
                    i += 1
                except requests.exceptions.RequestException as e:
                    detalles_partidas += f"Error al obtener datos de la partida {ele}: {e}\n"

        # Pregunta al usuario si desea guardar los detalles de las partidas en un archivo
        guardar_en_archivo = input("¿Desea guardar los detalles de las partidas en un archivo? (Si = guardar): ")
        if guardar_en_archivo.lower().startswith('s'):
            with open(ruta_archivo_txt, 'w', encoding='utf-8') as archivo_txt:
                archivo_txt.write(detalles_partidas)
            print(F"\033[92mDetalles de las partidas guardados exitosamente en {ruta_archivo_txt}\033[0m")
        else:
            print("\033[93mDetalles de las partidas no guardados.\033[0m")

        input("Continuar?")
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de partidas: {e}")
# Funcion para calcular la tasa de victorias
def tasaVictoriasDerrotas(datos, params):
    try:
        # Request
        api_url_get_match = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{datos['puuid']}/ids?start=0&count=5"
        response = requests.get(api_url_get_match, params=params)
        
        fpro2.guardar_consulta_api(api_url_get_match)
        
        response.raise_for_status()
        
        # Diccionario
        data = response.json()
        
        victorias = 0
        partidas = 5
        
        # Crea variables en caso de requerir abrir un archivo de texto
        carpeta_reportes = 'Reportes'
        os.makedirs(carpeta_reportes, exist_ok=True)

        prefijo_archivo = f"reporte-tasa-victoria-{datos['name']}"
        patron_archivo = f"{prefijo_archivo}.*"
        siguiente_numero = fpro2.obtener_siguiente_numero_archivos(carpeta_reportes, patron_archivo)
        fecha_hora_actual = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        ruta_archivo_txt = os.path.join(carpeta_reportes, f"{prefijo_archivo}({siguiente_numero})_{fecha_hora_actual}.txt")
        
        # Variable para guardar detalles de la partida en una cadena para el archivo de texto
        detalles_partidas = f"JUGADOR: {datos['name']} - REPORTE TASA VICTORIA Y DERROTA\n\n"
        
        for ele in data:
            try:
                api_url_get_matches = f"https://americas.api.riotgames.com/lol/match/v5/matches/{ele}"
                response = requests.get(api_url_get_matches, params=params)
                fpro2.guardar_consulta_api(api_url_get_matches)
                response.raise_for_status()
                data_for = response.json()
                for i, jugador in enumerate(data_for['info']['participants']):
                    if datos['puuid'] == jugador['puuid']:
                        numjugador = i
                        break
                if numjugador is not None and data_for['info']['participants'][numjugador]['win']:
                    victorias += 1
            except requests.exceptions.RequestException as e:
                print(f"Error al obtener datos de la partida {ele}: {e}")
                detalles_partidas += f"Error al obtener datos de la partida {ele}: {e}\n"

        tasa_victorias = (victorias / partidas) * 100
        tasa_derrotas = 100 - tasa_victorias
        sizes = [tasa_victorias, tasa_derrotas]
        print(f"Tasa de \033[92mVictorias:\033[0m {tasa_victorias}")
        print(f"Tasa de \033[91mDerrotas:\033[0m {tasa_derrotas}")
        
        detalles_partidas += f"  Tasa de Victorias: {tasa_victorias}\n"
        detalles_partidas += f"  Tasa de Derrotas: {tasa_derrotas}\n"
        print("")
        while True:
            print("\033[1;96m  ¿Quieres mostrar los datos en grafica?\033[0m")
            print("\033[96m  a)\033[0m Desplegar grafica y guardarla")
            print("\033[96m  b)\033[0m Guardar")
            print("\033[96m  c)\033[0m No quiere desplegarla ni guardarla")
            opcion = input("\033[96m  Seleccione una opcion: \033[0m").lower()

            if opcion == 'a' or opcion == 'b' or opcion == 'c':
                fpro2.graficar_estadisticas_victorias(datos['name'], opcion, sizes)
                print("")
                # Pregunta al usuario si desea guardar los detalles de las partidas en un archivo
                guardar_en_archivo = input("\033[96m¿Desea guardar los detalles de la tasa victoria en un archivo? (Si = guardar): \033[0m")
                if guardar_en_archivo.lower().startswith('s'):
                    with open(ruta_archivo_txt, 'w', encoding='utf-8') as archivo_txt:
                        archivo_txt.write(detalles_partidas)
                        print(F"\033[92mDetalles de las partidas guardados exitosamente en {ruta_archivo_txt}\033[0m")
                else:
                    print("\033[93mDetalles de las partidas no guardados.\033[0m")
                input("Continuar?")
                break
            else:
                print("Opcion no valida. Por favor, seleccione una opcion valida.")
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de partidas: {e}")
# Funcion para mostrar el KDA (se muestra datos significativos(Promedio))
def kda(datos, params):
    try:
        grafica = ""
        # Request
        api_url_get_match = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{datos['puuid']}/ids?start=0&count=5"
        response = requests.get(api_url_get_match, params=params)
        fpro2.guardar_consulta_api(api_url_get_match)
        response.raise_for_status()
        partidas_ids = response.json()

        kills_lista = []
        asistencias_lista = []
        muertes_lista = []
        
        carpeta_reportes = 'Reportes'
        os.makedirs(carpeta_reportes, exist_ok=True)

        prefijo_archivo = f"reporte-kda-{datos['name']}"
        patron_archivo = f"{prefijo_archivo}.*"


        siguiente_numero = fpro2.obtener_siguiente_numero_archivos(carpeta_reportes, patron_archivo)

        fecha_hora_actual = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        ruta_archivo_txt = os.path.join(carpeta_reportes, f"{prefijo_archivo}({siguiente_numero})_{fecha_hora_actual}.txt")
        detalles_partidas = f"JUGADOR: {datos['name']} - REPORTE KDA\n\n"
        
        print("Partida   Kills, Muertes, Asistencias")
        
        # Guardar detalles de la partida en una cadena para el archivo de texto
        detalles_partidas += f"  Partida   Kills, Muertes, Asistencias\n"
        for a, partida_id in enumerate(partidas_ids):
            try:
                # Request
                api_url_get_matches = f"https://americas.api.riotgames.com/lol/match/v5/matches/{partida_id}"
                response = requests.get(api_url_get_matches, params=params)
                response.raise_for_status()
                
                fpro2.guardar_consulta_api(api_url_get_matches)
                
                # Diccionario
                data_for = response.json()

                numjugador = None
                for i, jugador in enumerate(data_for['info']['participants']):
                    if datos['puuid'] == jugador['puuid']:
                        numjugador = i
                        break

                if numjugador is not None:
                    kills_lista.append(data_for['info']['participants'][numjugador]['kills'])
                    asistencias_lista.append(data_for['info']['participants'][numjugador]['assists'])
                    muertes_lista.append(data_for['info']['participants'][numjugador]['deaths'])
                    print(f"Partida {a + 1}:  {kills_lista[a]}\t {muertes_lista[a]}\t\t{asistencias_lista[a]}")
                    
                    detalles_partidas += f"  Partida {a + 1}:   {kills_lista[a]}\t\t{muertes_lista[a]} \t \t{asistencias_lista[a]}\n"
            except requests.exceptions.RequestException as e:
                print(f"Error al obtener datos de la partida {partida_id}: {e}")        

        partidas = [f"Partida {i+1}" for i in range(len(kills_lista))]
        promedio_kills = sum(kills_lista) / len(kills_lista) if kills_lista else 0
        promedio_muertes = sum(muertes_lista) / len(muertes_lista) if muertes_lista else 0
        promedio_asistencias = sum(asistencias_lista) / len(asistencias_lista) if asistencias_lista else 0

        # Imprimir el promedio
        print(f"Promedio: {promedio_kills}\t{promedio_muertes}\t{promedio_asistencias}")
        while True:
            print("")
            print("\033[1;96m  ¿Quieres mostrar los datos en grafica?\033[0m")
            print("\033[96m  a)\033[0m Desplegar grafica y guardarla")
            print("\033[96m  b)\033[0m Guardar")
            print("\033[96m  c)\033[0m No quiere desplegarla ni guardarla")
            opcion = input("\033[96m  Seleccione una opcion: \033[0m").lower()

            if opcion == 'a' or opcion == 'b' or opcion == 'c':
                fpro2.graficar_estadisticas_partidas(datos['name'], opcion, partidas, kills_lista, asistencias_lista, muertes_lista)
                print("")
                guardar_en_archivo = input("\033[96m¿Desea guardar los detalles del KDA en un archivo? (Si = guardar): \033[0m")
                if guardar_en_archivo.lower().startswith('s'):
                    with open(ruta_archivo_txt, 'w', encoding='utf-8') as archivo_txt:
                        archivo_txt.write(detalles_partidas)
                    print(F"\033[92mDetalles de las partidas guardados exitosamente en {ruta_archivo_txt}\033[0m")
                else:
                    print("\033[93mDetalles de las partidas no guardados.\033[0m")
                input("Continuar?")
                break
            else:
                print("Opcion no valida. Por favor, seleccione una opcion valida.")
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de partidas: {e}")
# Funcion para mostrar personaje mas jugado (se muestra datos significativos(Moda))
def personajeMasJugado(datos, params):
    try:
        # Request
        api_url_get_match = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{datos['puuid']}/ids?start=0&count=10"
        response = requests.get(api_url_get_match, params=params)
        response.raise_for_status()
        data = response.json()

        champion_names = []
        
        # Crea variables en caso de requerir abrir un archivo de texto
        carpeta_reportes = 'Reportes'
        os.makedirs(carpeta_reportes, exist_ok=True)

        prefijo_archivo = f"reporte-personaje-mas-jugado-{datos['name']}"
        patron_archivo = f"{prefijo_archivo}.*"
        siguiente_numero = fpro2.obtener_siguiente_numero_archivos(carpeta_reportes, patron_archivo)
        fecha_hora_actual = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        ruta_archivo_txt = os.path.join(carpeta_reportes, f"{prefijo_archivo}({siguiente_numero})_{fecha_hora_actual}.txt")
        
        # Guardar detalles de la partida en una cadena para el archivo de texto
        detalles_partidas = f"JUGADOR: {datos['name']} - REPORTE PERSONAJE MAS JUGADO\n\n"
        
        for match_id in data:
            try:
                # Request
                api_url_get_matches = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
                response = requests.get(api_url_get_matches, params=params)
                response.raise_for_status()
                
                # Diccionario
                data_for = response.json()

                for i, jugador in enumerate(data_for['info']['participants']):
                    if datos['puuid'] == jugador['puuid']:
                        champion_names.append(jugador['championName'])
            except requests.exceptions.RequestException as e:
                print(f"Error al obtener datos de la partida {match_id}: {e}")

        # Retorna un diccionario
        counter = Counter(champion_names)

        if counter:
            campeon_mas_usado, veces_jugado = counter.most_common(1)[0]
            print("")
            print(f"El campeon mas usado es \033[94m{campeon_mas_usado}\033[0m, jugado {veces_jugado} veces.")
            print("")
            
            # Guardar detalles de la partida en una cadena para el archivo de texto
            detalles_partidas += f"    El campeon mas usado es {campeon_mas_usado}, jugado {veces_jugado} veces.\n"
            detalles_partidas += f"    Campeones Usados: {champion_names}\n"
            while True:
                print("\033[1;96m  ¿Quieres mostrar los datos en grafica?\033[0m")
                print("\033[96m  a)\033[0m Desplegar grafica y guardarla")
                print("\033[96m  b)\033[0m Guardar")
                print("\033[96m  c)\033[0m No quiere desplegarla ni guardarla")
                opcion = input("\033[96m  Seleccione una opcion: \033[0m").lower()

                if opcion == 'a' or opcion == 'b' or opcion == 'c':
                    fpro2.graficar_campeones_usados(datos['name'], opcion, champion_names)
                    print("")
                    # Preguntar al usuario si desea guardar los detalles de las partidas en un archivo
                    guardar_en_archivo = input("¿\033[96mDesea guardar los detalles de los personajes mas usados en un archivo? (Si = guardar): \033[0m")
                    if guardar_en_archivo.lower().startswith('s'):
                        with open(ruta_archivo_txt, 'w', encoding='utf-8') as archivo_txt:
                            archivo_txt.write(detalles_partidas)
                        print(F"\033[92mDetalles de las partidas guardados exitosamente en {ruta_archivo_txt}\033[0m")
                    else:
                        print("\033[93mDetalles de las partidas no guardados.\033[0m")
                    input("Continuar?")
                    break
                else:
                    print("Opcion no valida. Por favor, seleccione una opcion valida.")
        else:
            print("No se encontraron datos de partidas.")

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de partidas: {e}")
