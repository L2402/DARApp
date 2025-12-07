import os
import json

class ListaReproduccion:
    def __init__(self, cancion):
        self.cancion = cancion
        self.titulo = cancion.titulo
        self.artista = cancion.artista
        self.url = cancion.url

    def agregar_cancion(self): 
        carpeta_ListaReproduccion = "ListaReproduccion.json"  
        Cancion_info = {  
            "nombre": self.titulo,  
            "artista": self.artista,  
            "url": self.url  
        }  
        
        # Verifica si el archivo ya existe y carga su contenido
        if os.path.exists(carpeta_ListaReproduccion):  
            with open(carpeta_ListaReproduccion, "r") as fichero:  
                try:  
                    archivo = json.load(fichero)  
                    if not isinstance(archivo, list):  
                        raise ValueError("El archivo JSON no es una lista.")  
                except (json.JSONDecodeError, ValueError):  
                    archivo = []  # Si está vacío, inicializa una lista vacía
        else:  
            archivo = []

        # Añade la nueva canción a la lista y guardar en el archivo JSON
        archivo.append(Cancion_info)
        with open(carpeta_ListaReproduccion, "w") as fichero:
            json.dump(archivo, fichero, indent=4)
        
    def ver_lista_reproduccion(self):
        lista_reproduccion = "ListaReproduccion.json"

        if not os.path.exists(lista_reproduccion):
            print("No hay nada que mostrar")
            
        with open(lista_reproduccion, "r") as fichero:
            archivo = json.load(fichero)
            
        if not archivo:
            print("No hay musica que recientemente ha visto")
            
        for lista in archivo:
            print(f"Nombre: {lista.get('nombre', 'desonocido')}")
            print(f"Artista: {lista.get('artista', 'desconocido')}")
            print("*" *30)
