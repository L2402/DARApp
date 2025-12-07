import requests
import io
import pygame
import keyboard
import threading
import os
import json
from commands import PlayCommand, PauseCommand, StopCommand, RepeatCommand, AddToCommand, ControlInvoker

class Reproductor:
    def __init__(self, titulo, artista):
        self.titulo = titulo
        self.artista = artista
        self.is_paused = False #Pausamos la musica
        self.is_playing = False #Verifica si esta reproduciondo la musica
        self.stop_playing = False  # Variable para detener la música

    def reproducir(self, url_audio):
        if not self.is_playing:  # Solo reproducir si no está en reproducción
            self.is_playing = True
            def play():
                pygame.mixer.init() #Inicializamos el gestor de audio de Pygame
                print(f"Reproduciendo: {self.titulo} - {self.artista}")
                audio_data = requests.get(url_audio)
                audio_file = io.BytesIO(audio_data.content) #Almacenamos en memoria el audio en binarios para reproducirlos
                pygame.mixer.music.load(audio_file) #Cargamos el audio
                pygame.mixer.music.play() #Reproducimos

                # Mientras se esté reproduciendo, verifica si está detenido o en pausa
                while pygame.mixer.music.get_busy() and not self.stop_playing:
                    pygame.time.Clock().tick(10) #Realizamos una espera de 10 segundos para evitar que se realice la reproduccion muy rapido
                self.is_playing = False  # La música ha terminado de reproducirse

            hilo_reproduccion = threading.Thread(target=play)
            hilo_reproduccion.daemon = True
            hilo_reproduccion.start()
    
    def reproducir_album_guardado(self, nombre_album):
        from Cancion import Cancion
        Albunes = "AlbunesGuardados.json"

        if not os.path.exists(Albunes):
            print("No hay álbumes guardados.")
            return

        with open(Albunes, "r") as fichero:
            archivo = json.load(fichero)

        # Buscar el álbum correspondiente
        for album in archivo:
            if album["nombre"] == nombre_album:
                print(f"Reproduciendo álbum '{nombre_album}'...")

                # Reutilizar el reproductor para cada canción
                for cancion in album["canciones"]:
                    titulo = cancion["titulo"]
                    artista = cancion["artista"]
                    url = cancion["url"]

                    # Configuramos el reproductor con la canción actual
                    reproductor = Reproductor(titulo, artista)
                    cancion = Cancion(titulo, artista, url)
                    reproductor.controles(url, cancion)

                    # Esperar a que la canción termine antes de pasar a la siguiente
                    while reproductor.is_playing:
                        pygame.time.Clock().tick(10)

                print(f"Álbum '{nombre_album}' terminado.")
                return

        print(f"Álbum '{nombre_album}' no encontrado.")
    
    def reproducir_album_api(self, nombre_album, api):
        from Cancion import Cancion
        # Obtener el álbum de la API de Jamendo por nombre
        url_busqueda_album = f"https://api.jamendo.com/v3.0/albums/tracks/?name={nombre_album}&client_id={api}"
        response = requests.get(url_busqueda_album)

        if response.status_code != 200:
            print("Error al obtener el álbum desde la API.")
            return

        data = response.json()
        if 'results' not in data or len(data['results']) == 0:
            print(f"Álbum '{nombre_album}' no encontrado en la API.")
            return

        album = data['results'][0]  # Tomamos el primer álbum encontrado
        print(f"Reproduciendo álbum '{album['name']}' de {album['artist_name']}...")

        # Reproducir todas las canciones del álbum
        for cancion in album['tracks']:
            titulo = cancion['name']
            artista = album['artist_name']
            url_audio = cancion['audio']

            # Configurar el reproductor con la canción actual
            reproductor = Reproductor(titulo, artista)
            cancion = Cancion(titulo, artista, url_audio)
            reproductor.controles(url_audio, cancion)

            # Esperar a que la canción termine antes de pasar a la siguiente
            while reproductor.is_playing:
                pygame.time.Clock().tick(10)

        print(f"Álbum '{album['name']}' terminado.")

    def pausar(self):
        if self.is_playing:
            if not self.is_paused:
                pygame.mixer.music.pause()
                print("La música está en pausa")
                self.is_paused = True
            else:
                pygame.mixer.music.unpause()
                print("La música se ha reanudado")
                self.is_paused = False

    def detener(self):
        pygame.mixer.music.stop()
        self.stop_playing = True
        print("La música se ha detenido")
        self.is_playing = False

    def repetir(self):
        pygame.mixer.music.play(loops=-1)  # Repite en bucle
        print("La música está en bucle")

    def controles(self, url_audio, cancion):
        invoker = ControlInvoker()

        # Asociar comandos a acciones
        invoker.set_command('i', PlayCommand(self, url_audio))
        invoker.set_command('p', PauseCommand(self))
        invoker.set_command('d', StopCommand(self))
        invoker.set_command('r', RepeatCommand(self))
        invoker.set_command('f', AddToCommand(self, cancion))

        while True:
            # Modo no bloqueante: cuando se detecta una tecla, delegar al invocador
            if keyboard.is_pressed('i') and not self.is_playing:
                invoker.handle('i')
                # Esperar a que se suelte la tecla para evitar ejecuciones repetidas
                while keyboard.is_pressed('i'):
                    pygame.time.Clock().tick(10)

            elif keyboard.is_pressed('p'):
                invoker.handle('p')
                while keyboard.is_pressed('p'):
                    pygame.time.Clock().tick(10)

            elif keyboard.is_pressed('d'):
                invoker.handle('d')
                while keyboard.is_pressed('d'):
                    pygame.time.Clock().tick(10)

            elif keyboard.is_pressed('r'):
                invoker.handle('r')
                while keyboard.is_pressed('r'):
                    pygame.time.Clock().tick(10)

            elif keyboard.is_pressed('f'):
                # Detener antes de preguntar, como en la versión anterior
                invoker.handle('d')
                invoker.handle('f')
                while keyboard.is_pressed('f'):
                    pygame.time.Clock().tick(10)

            pygame.time.Clock().tick(10)  # Evita que el ciclo consuma demasiados recursos
    
    def pregunta(self, cancion):
        from IngresarCancionA import Pregunta
        pregunta_usuario = Pregunta(cancion)
        pregunta_usuario.agregar_a() #Llamamos al metodo para preguntar al usuario donde desea agregar la musica
