import requests  
import json  
import os
from Reproductor import Reproductor

class Album:  
    def __init__(self, api_key):
        self.api_key, self.B = api_key.Obtener_Valores
    
    def buscar_album_artista(self, artista):  
        # Realiza la solicitud a la API de Jamendo y le pasamos la clave y el artista a buscar directamente a la URL de albumes
        url_album = f"https://api.jamendo.com/v3.0/albums/?client_id={self.api_key}&format=json&artistname={artista}"
        #Realizamos la busqueda con requests y con GET hacemos una busqueda de tipo https y http facilitando la obtencion de los datos
        response = requests.get(url_album)
        data = response.json() #Convertimos los datos obtenidos a un JSON para facilitar su lectura y trabajar mas facil con los datos
        
        # Verifica si hay resultados para el artista
        if 'results' in data and data['results']: #Verificamos si la clave results esta en data y si data[results] contiene valores
            print(f"Álbumes de {artista}:")
            for idx, album in enumerate(data['results'], 1): #Enumeramos los resultados
                print(f"{idx}. {album['name']} (ID: {album['id']})") #Imprimimos los resultados
            try:
                seleccion = int(input(f"Seleccione el numero del album que desea ver: ")) #Preguntamos que album desea abrir para ver canciones
                if 1 <= seleccion <= len(data['results']):
                    album_seleccionado = data['results'][seleccion -1]
                    print(f"Álbum seleccionado: {album_seleccionado['name']}")

                    self.ver_canciones_album(album_seleccionado['id'], album_seleccionado['name'])
                
                else:
                    print("Seleccion no valida")
            except ValueError:
                print("Por favor, ingrese un numero válido")
        else:
            print("No se encontraron álbumes para este artista.")
    
    def ver_canciones_album(self, album_ID, nombre_album): #Obtenemos el ID del album para ver sus canciones y con la Key conectamos con la API
        url_canciones = f"https://api.jamendo.com/v3.0/tracks/?client_id={self.api_key}&format=json&album_id={album_ID}"
        response = requests.get(url_canciones)
        data = response.json()

        if 'results' in data and data['results']:
            print(f"Canciones en este álbum:")
            for idx, cancion in enumerate(data['results'], 1):
                print(f"{idx}. {cancion['name']} - {cancion['artist_name']}")
        
        reproducir = ""
        #Inicializamos reproducir como vacio para entrar en el bucle while y realizar una validacion de solo si o no
        while reproducir not in ["s", "n"]:
            reproducir = input("¿Quiere reproducir este álbum? (s/n): ")

            if reproducir.lower() == "s":
                reproductor = Reproductor(None, None) #Ponemos en none los parametros esperados por Reproductor ya que no se utilizaran
                reproductor.reproducir_album_api(nombre_album, self.api_key) #Pasamos el nombre del album a reproducir y la clave para conectar
                break
        else:
            print("No se encontraron canciones para este álbum.")
    
    def guardar_album(self, nombre_album, año, artista):
        Albunes = "AlbunesGuardados.json"  #ruta al archivo JSON de albumes
        Album_Info = {  
            "nombre": nombre_album,  
            "artista": artista,  
            "año": año,
            "canciones": [] #Realizamos una lista vacia para almacenar las musicas ahi
        }  
        
        # Comprobar si el archivo ya existe  
        if os.path.exists(Albunes):  
            with open(Albunes, "r") as fichero:  
                try:  
                    # Cargar álbumes existentes  
                    archivo = json.load(fichero)  
                    # Nos aseguramos de que 'archivo' sea una lista con isinstance del tipo list
                    if not isinstance(archivo, list):
                        raise ValueError("El archivo JSON no es una lista.")  #Raise crea un except de try e imprime un mensaje
                except (json.JSONDecodeError, ValueError):  
                    # Si el archivo está vacío o mal formateado, inicializar como lista vacía  
                    archivo = []  
        else:  
            archivo = []  

        # Agregar el nuevo álbum  al JSON
        archivo.append(Album_Info)

        # Guardar todos los álbumes  
        with open(Albunes, "w") as fichero:  
            json.dump(archivo, fichero, indent=3)  

        print(f"Álbum '{nombre_album}' guardado con éxito.")  
    
    def eliminar_album(self, nombre):  
        Albunes = "AlbunesGuardados.json"  
        
        if not os.path.exists(Albunes):  
            print(f"El álbum '{Albunes}' no existe.")  
            return  
        
        with open(Albunes, "r") as fichero:  
            archivo = json.load(fichero)  

        #Iteramos sobre el JSON para guardar solo las musicas que no coincidan con el nombre de musica ingresado
        albunes_mantener = [album for album in archivo if album["nombre"] != nombre]

        #Si la cantidad de canciones guardadas es igual a la de la lista entonces no se borro la musica y finalizamos el metodo
        if len(albunes_mantener) == len(archivo): 
            print(f"El álbum '{nombre}' no se encontró.")  
            return  
        
        #Sobreescribimos el archivo con la lista de musicas a mantener menos la que queria eliminar el usuario
        with open(Albunes, "w") as fichero:  
            json.dump(albunes_mantener, fichero, indent=3)  
        
        print(f"Álbum '{nombre}' eliminado con éxito!")  #Imprimimos mensaje de que se borro la musica

    def agregar_cancion(self, nombre_album, titulo_cancion, artista_cancion, url_cancion):
        Albunes = "AlbunesGuardados.json"

        if not os.path.exists(Albunes):
            print("No hay álbumes guardados.")
            return

        with open(Albunes, "r") as fichero:
            archivo = json.load(fichero)

        # Buscar el álbum correspondiente
        for album in archivo:
            if album["nombre"] == nombre_album:
                nueva_cancion = {
                    #Agregamos el titulo, artista y la url de la musica al album
                    "titulo": titulo_cancion,
                    "artista": artista_cancion,
                    "url": url_cancion #El url sirve para que podamos reproducir la musica
                }
                album["canciones"].append(nueva_cancion)
                print(f"Canción '{titulo_cancion}' agregada al álbum '{nombre_album}'.")
                break
        else:
            print(f"Álbum '{nombre_album}' no encontrado.")
            return

        # Guardar los cambios en el archivo
        with open(Albunes, "w") as fichero:
            json.dump(archivo, fichero, indent=3)

    def eliminar_cancion(self, nombre_album, titulo_cancion):
        Albunes = "AlbunesGuardados.json"

        if not os.path.exists(Albunes):
            print("No hay álbumes guardados.")
            return

        with open(Albunes, "r") as fichero:
            archivo = json.load(fichero)

        # Buscar el álbum correspondiente
        for album in archivo:
            if album["nombre"] == nombre_album:
                canciones_filtradas = [
                    cancion for cancion in album["canciones"] if cancion["titulo"] != titulo_cancion
                ]
                if len(canciones_filtradas) == len(album["canciones"]):
                    print(f"La canción '{titulo_cancion}' no se encontró en el álbum '{nombre_album}'.")
                else:
                    album["canciones"] = canciones_filtradas
                    print(f"Canción '{titulo_cancion}' eliminada del álbum '{nombre_album}'.")
                break
        else:
            print(f"Álbum '{nombre_album}' no encontrado.")
            return

        # Guardar los cambios en el archivo
        with open(Albunes, "w") as fichero:
            json.dump(archivo, fichero, indent=3)
    
    def ver_album(self):
        albumes = "AlbunesGuardados.json"

        if not os.path.exists(albumes):
            print("No hay albunes guardados")
            return
        
        with open(albumes, "r") as fichero:
            archivo = json.load(fichero)

        for album in archivo:
            #Iteramos sobre el album para obtener el nombre, el año y el artista
            #En caso de no contar con esos valores, le pasamos desconocido
            print(f"Nombre: {album.get('nombre', 'Desconocido')}")
            print(f"Año: {album.get('año', 'Desconocido')}")
            print(f"Artista: {album.get('artista', 'Desconocido')}")
            print("-" * 30)