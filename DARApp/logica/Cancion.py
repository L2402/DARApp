class Cancion():
    def __init__(self, titulo, artista, url):
        #Esperamos estos parametros para pasarlos a otras clases y asi hacemos inyeccion de dependencias
        #Esto evita que estemos creando tantas instancias de todas las clases en busqueda
        self.titulo = titulo
        self.artista = artista
        self.url = url
