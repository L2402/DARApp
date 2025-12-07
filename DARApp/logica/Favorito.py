import os
import json

class Favorito:
    
    def __init__(self, titulo, artista, url):
        self.titulo = titulo
        self.artista = artista
        self.url = url

    def agregar_cancion(self): 
        Carpeta_Favorito = "Favorito.json"  
        Cancion_info = {  
            "nombre": self.titulo,  
            "artista": self.artista,  
            "url": self.url  
        }  
        
        # Verificar si el archivo ya existe y cargar su contenido
        if os.path.exists(Carpeta_Favorito):  
            with open(Carpeta_Favorito, "r") as fichero:  
                try:  
                    archivo = json.load(fichero)  
                    if not isinstance(archivo, list):  
                        raise ValueError("El archivo JSON no es una lista.")  
                except (json.JSONDecodeError, ValueError):  
                    archivo = []  # Si está vacío o mal formateado, inicializar lista vacía
        else:  
            archivo = []

        # Añadir la nueva canción a la lista y guardar en el archivo JSON
        archivo.append(Cancion_info)
        with open(Carpeta_Favorito, "w") as fichero:
            json.dump(archivo, fichero, indent=4)

    def eliminar_cancion(self, nombre):
        Carpeta_Favorito = "Favorito.json"  
        
        if not os.path.exists(Carpeta_Favorito):
            print("No existe el archivo de favoritos.")
            return
        
        with open(Carpeta_Favorito, "r") as fichero:
            archivo = json.load(fichero)
        
        canciones_mantener = [cancion for cancion in archivo if cancion["nombre"] != nombre]
        
        if len(canciones_mantener) == len(archivo):
            print(f"La musica '{nombre}' no se encontro")
            return

        with open(Carpeta_Favorito, "w") as fichero:
            json.dump(archivo, fichero, indent=4)

        print(f"Musica '{nombre}' eliminada con exito de la carpeta favoritos")
    
    def ver_favoritos(self):
        favorito = "Favorito.json"

        if not os.path.exists(favorito):
            print("No existe el archivo")
            return

        with open(favorito, "r") as fichero:
            archivo = json.load(fichero)
        
        for fav in archivo:
            print(f"Nombre: {fav.get('nombre', 'desonocido')}")
            print(f"Artista: {fav.get('artista', 'desconocido')}")
            print("*" * 30)
