from Validaciones import Validacion
from Reproductor import Reproductor

class GestionaAccionesAlbum:
    def __init__(self, album_instancia):
        self.album_instancia = album_instancia #Creamos un objeto de la clase album para acceder a sus metodos
        self.validaciones = Validacion()
    
    def buscar_album(self):
        while True:
            artista = input("Ingrese el nombre del artista para buscar album: ")
            if self.validaciones.valida_entrada(artista):
                break

        self.album_instancia.buscar_album_artista(artista)

    def crear_album(self):
        while True:
            nombre = input("Ingrese el nombre del album: ")
            if self.validaciones.valida_entrada(nombre):
                break
                
        while True:
            año = input("Ingrese el año: ")
            if self.validaciones.valida_numero(año):
                año = int(año)
                break
                
        while True:
            artista = input("Ingrese el nombre del artista: ")
            if self.validaciones.valida_entrada(artista):
                break

        self.album_instancia.guardar_album(nombre, año, artista)

    def eliminar_album(self):
        while True:
            nombre = input("Ingrese el nombre del album guardado a eliminar: ")
            if self.validaciones.valida_entrada(nombre):
                break
            
        self.album_instancia.eliminar_album(nombre)
    
    def eliminar_cancion(self):
        while True:
            nombre_album = input("Ingrese el nombre del album: ")
            if self.validaciones.valida_entrada(nombre_album):
                break
        
        while True:
            nombre_cancion = input("Ingrese el nombre de la cancion a eliminar: ")
            if self.validaciones.valida_entrada(nombre_cancion):
                break
        
        self.album_instancia.eliminar_cancion(nombre_album, nombre_cancion)

    def ver_album(self):
        self.album_instancia.ver_album()

    def reproducir_album(self):
        while True:
            nombre = input("Ingrese el nombre del album a reproducir: ")
            if self.validaciones.valida_entrada(nombre):
                break
        
        reproductor = Reproductor(None, None)
        reproductor.reproducir_album_guardado(nombre)

    def accion_invalida(self):
        print("Opcion invalida")