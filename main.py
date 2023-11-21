#PIA PROGRAMACION - EQUIPO ENIAC
#SE NECESITA INGRESAR API EN EL ARCHIVO
import os
import funct1 as fpro1
import funct2 as fpro2
import subprocess
import sys

def instalarModulos(module):
    try:
        subprocess.check_call(['pip', 'install', module])
        print(f"Instalado exitosamente: {module}")
    except subprocess.CalledProcessError:
        print(f"No se pudo instalar: {module}")

def checarModulos():
    modulos_requeridos = ['requests', 'funct2', 'os', 'datetime', 'collections', 'matplotlib.pyplot', 're', 'openpyxl', 'collections']

    nomodulos = []

    for modulo in modulos_requeridos:
        try:
            __import__(modulo)
        except ImportError:
            nomodulos.append(modulo)

    if nomodulos:
        print("Faltan los siguientes modulos:")
        for modulo in nomodulos:
            print(f"- {modulo}")
            instalarModulos(modulo)
    else:
        print("Todos los modulos necesarios estan instalados.")

try:
    # Reemplaza 'archivo.key' con la ruta y nombre de tu archivo .key
    with open('API keys/archivo.key.txt', 'r') as archivo:
        api_key = archivo.read()
        print(f"Llave leída del archivo:\n{api_key}")
except FileNotFoundError:
    print("El archivo .key no fue encontrado.")
    print('Ingrese key en el archivo.key.txt localizado en la carpeta API LOL\\API Keys')
    sys.exit()
except IOError as e:
    print(f"Error de entrada/salida al leer el archivo .key: {e}")
    sys.exit()
except Exception as e:
    print(f"Error inesperado: {e}")
    sys.exit()
params = {'api_key': api_key}
# Main
if __name__ == "__main__":
    checarModulos()
    cen = 0
    if len(sys.argv) < 1:
        nombresys = sys.argv[1]
        regionsys = sys.argv[2].lower()
        if len(sys.argv) != 3:
            print("Uso: python nombre_del_script.py <nombre_del_jugador> <region>")
            sys.exit(1)
        if regionsys not in ['a', 'b', 'c', 'd', 'e']:
            print("Region no valida. Por favor, ingrese una region valida.")
            sys.exit(1)
        else:
            if regionsys == 'a':
                regionsys = "na1"
            elif regionsys == 'b':
                regionsys = "br1"
            elif regionsys == 'c':
                regionsys = "EUW1"
            elif regionsys == 'd':
                regionsys = "LA1"
            elif regionsys == 'e':
                regionsys = "LA2"
            data = fpro1.datosUsuarioIngresado(nombresys, regionsys, params)
            fpro1.verPartidas(data, params)
    while True:
        nombre = input("\033[1;94mIngrese el nombre del jugador: \033[0m")
        region = fpro2.obtener_cadena_por_region()
        data = fpro1.datosUsuarioIngresado(nombre, region, params)
        if data is not None:
            break
        else:
            print("\033[91mNo se encontraron datos para el jugador. Por favor, ingrese un nombre valido.\033[0m")
    while True:
        os.system('cls')
        print("\033[1;94mMenu Principal:\033[0m")
        print("\033[94ma)\033[0m Ver ultimas 5 partidas")
        print("\033[94mb)\033[0m Tasa de victorias y derrotas")
        print("\033[94mc)\033[0m KDA")
        print("\033[94md)\033[0m Personaje mas jugado")
        print("\033[94me)\033[0m Reportes")
        print("\033[94mf)\033[0m Salir")

        opcion = input("\033[94mSeleccione una opcion:\033[0m ").lower()
        print("")

        if opcion == 'a':
            fpro1.verPartidas(data, params)
        elif opcion == 'b':
            fpro1.tasaVictoriasDerrotas(data, params)
        elif opcion == 'c':
            fpro1.kda(data, params)
        elif opcion == 'd':
            fpro1.personajeMasJugado(data, params)
        elif opcion == 'e':
            fpro2.imprimir_reportes()
        elif opcion == 'f':
            break
        else:
            print("Opcion no valida. Por favor, seleccione una opcion valida.")
