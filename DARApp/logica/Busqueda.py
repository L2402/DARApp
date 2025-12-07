import requests
from Reproductor import Reproductor
from Cancion import Cancion
from ListaReproduccion import ListaReproduccion

class TipoBusqueda:
    def __init__ (self):
        #Definimos los atributos en None por que luego los obtendremos al interactuar con el usuario
        self.artista = None
        self.cancion = None
        self.genero = None
        self.tipo_busqueda = None
    
    def tipo_de_busqueda(self):
        while True:
            self.tipo_busqueda = input("Ingrese si quiere buscar por artista, cancion o genero: ").lower()
            if self.tipo_busqueda.lower() in ["artista", "cancion", "genero"]: #Verificamos que la respuesta este en la lista
                break
            else:
                print("Por favor, elija una opcion valida")
        
        if self.tipo_busqueda.lower() == "artista": #Si la respuesta es artista llamamos al metodo para solicitar nombre
            self.artista = self.solicitar_artista()
        
        elif self.tipo_busqueda.lower() == "cancion": #Si la respuesta es cancion llamamos el metodo para solicitar el titulo
            self.cancion = self.solicitar_cancion()
                
        else:
            self.genero = self.solicitar_genero() #Si no es ninguna de las respuestas anteriores llamamos al metodo para solicitar genero
        
    def solicitar_artista(self):
        while True:
                nombre_artista = input("Ingrese el nombre del artista: ")
                if nombre_artista: #Veficiamos que la respuesta no sea None
                    return nombre_artista
                else:
                    print("Ingrese el nombre en cadena")

    def solicitar_cancion(self):
            while True:
                nombre_cancion = input("Ingrese el nombre de la cancion: ")
                if nombre_cancion:
                    return nombre_cancion
                else:
                    print("Ingrese el nombre en cadena")

    def solicitar_genero(self):
        while True:
                genero_musica = input("Ingrese el nombre del genero: ")
                if genero_musica:
                    return genero_musica
                else:
                    print("Ingrese el genero en cadena")

class Busqueda:
    def __init__(self, tipo_busqueda_instance, dar_instance):
        self.tipo_busqueda_instance = tipo_busqueda_instance #Obtenemos el tipo de busqueda que quiere realizar
        self.__Api_key, self.Base_Url = dar_instance.Obtener_Valores #Obtenemos la clave y la URL para buscar las musicas
        self.resultados_filtrados = [] #Variable de tipo lista para almacenar los resultados obtenidos
    
    def realizar_busqueda(self):
        tipo_busqueda = self.tipo_busqueda_instance.tipo_busqueda
        if tipo_busqueda.lower() == "artista":
            self.busqueda_por_artista(self.tipo_busqueda_instance.artista)
        elif tipo_busqueda.lower() == "cancion":
            self.busqueda_por_nombre_cancion(self.tipo_busqueda_instance.cancion)
        elif tipo_busqueda.lower() == "genero":
            self.busqueda_por_genero(self.tipo_busqueda_instance.genero)

    def busqueda_por_artista(self, artista):
        params = {
            'client_id': self.__Api_key, #Accedemos a la clave para conectar con la API
            'format': 'json',
            'search': artista,
            'limit': 10
        }
        response = requests.get(self.Base_Url, params=params)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Convertir la respuesta a formato JSON
            data = response.json()
            # Imprimir el resultado
            self.resultados_filtrados = [
                track for track in data['results']
                if track['artist_name'].lower() == artista.lower() and 'audio' in track #Verificamos que este el audio para poder reproducir
            ]


            if self.resultados_filtrados:
                for i, track in enumerate(self.resultados_filtrados, 1):
                    print(f"{i}. Title: {track['name']}, Artist: {track['artist_name']}")
            else:
                print("No se encontraron resultados")
        else:
            print(f"Error: {response.status_code}")

    def busqueda_por_nombre_cancion(self, cancion):
        params = {

        'client_id': self.__Api_key,
        'format': 'json',
        'search': cancion,
        'limit':10

    }
        response = requests.get(self.Base_Url, params=params)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Convertir la respuesta a formato JSON
            data = response.json()
            # Imprimir el resultado

            self.resultados_filtrados = [
                track for track in data['results']
                if track['name'].lower() == cancion.lower() and 'audio' in track
            ]

            if self.resultados_filtrados:
                for i, track in enumerate(self.resultados_filtrados, 1):
                    print(f"{i}. Title: {track['name']}, Artist: {track['artist_name']}")
            else:
                print("No se encontraron resultados")

        else:
            print(f"Error: {response.status_code}")

    def busqueda_por_genero(self, genero):
        params = {

        'client_id': self.__Api_key,
        'format': 'json',
        'tags': genero.lower(),
        'limit':10

    }
        
        response = requests.get(self.Base_Url, params=params)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Convertir la respuesta a formato JSON
            data = response.json()
             #Teniamos un error al obtener los datos con get en data[results], ya que verificamos que este un valor ya obtenido y anulaba todo
            if 'results' in data and data['results']:
                self.resultados_filtrados = data['results']
                for i, track in enumerate(self.resultados_filtrados):
                    print(f"{i+1}. Title: {track['name']}, Artist: {track['artist_name']}")
            else:
                print("No se encontraron resultados")
        else:
            print(f"Error: {response.status_code}, Mensaje: {response.text}")
    
    def seleccionar_y_reproducir(self):
        if not self.resultados_filtrados:
            print("No hay canciones para seleccionar.")
            return

        while True:
            try:
                seleccion = input("Seleccione el número de la canción que desea reproducir: ").strip()
                if not seleccion.isdigit(): #Verificamos que la seleccion sea de tipo numerico
                    raise ValueError("La entrada debe ser un número.")
                
                seleccion = int(seleccion)
                if 1 <= seleccion <= len(self.resultados_filtrados):
                    track = self.resultados_filtrados[seleccion - 1] #Almacenamos los resultados filtrados en la variable
                    url_audio = track.get('audio') #Obtenemos el audio del diccionario guardado en resultados filtrados
                    if url_audio:  # Verifica que la URL no sea None
                        titulo = track['name']
                        artista = track['artist_name']
                        print(f"Intentando reproducir: {titulo} - {artista}")

                        #Pasamos titulo, artista, y url a la clase cancion
                        cancion = Cancion(titulo, artista, url_audio)
                        #Pasamos el objeto de la clase cancion a lista de reproduccion para guardar la musica
                        lista_reproduccion = ListaReproduccion(cancion)
                        lista_reproduccion.agregar_cancion()
                        
                        try:
                            reproductor = Reproductor(titulo, artista) #Pasamos el titulo y el artista para mostrar que musica se reproduce
                            reproductor.controles(url_audio, cancion) #Pasamos la url para reproducir
                            print("Reproducción iniciada con éxito.")
                        except Exception as e:
                            print(f"Error al reproducir la canción: {e}")
                        break
                    else:
                        print("No se encontró una URL de audio para esta canción.")
                else:
                    print(f"Por favor seleccione un número entre 1 y {len(self.resultados_filtrados)}")
            except ValueError as e:
                print(f"Entrada no válida: {e}")

        