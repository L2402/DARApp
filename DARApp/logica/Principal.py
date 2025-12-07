from Busqueda import Busqueda, TipoBusqueda
from Dar import Dar
from Album import Album
from Recomendaciones import Recomendaciones
from Cancion import Cancion
from ListaReproduccion import ListaReproduccion
from Favorito import Favorito
from Validaciones import Validacion
from GestionaAccionesAlbum import GestionaAccionesAlbum

#Menu para interactuar con el usuario
class Principal:
    def __init__(self):
        self.dar_instance = Dar()
        self.album = Album(self.dar_instance) #Pasamos Dar instance para que tenga acceso a la clave para conectar con la API
        self.recomendacion = Recomendaciones(self.dar_instance)
        self.cancion = Cancion(None, None, None) #Le pasamos None a sus atributos ya que no se utilizaran sus atributos en este caso
        self.lista_R = ListaReproduccion(self.cancion)
        self.favorito = Favorito(self.cancion.titulo, self.cancion.artista, self.cancion.url)
        self.validaciones = Validacion() #Creamos un objeto de la clase Validacion para acceder a los metodos de validacion
        self.gestion_album = GestionaAccionesAlbum(self.album)
    
    def menu(self):
        while True:
            print("Menu")
            print("1. Buscar Musica")
            print("2. Acciones de album")
            print("3. Ver lista de reproduccion")
            print("4. Ver favoritos")
            print("5. Eliminar musica de Carpeta Favoritos")
            print("6. Ver recomendaciones de musica semanalmente")
            print("7. Salir")

            opcion = input("Ingrese una opción: ")
            
            if not self.validaciones.valida_numero(opcion): #Validamos que sea un numero la opcion ingresada
                continue

            opcion = int(opcion)
            
            if opcion == 1:
                #Llamamos a la clase busqueda para realizar las busquedas
                tipo_busqueda = TipoBusqueda()
                tipo_busqueda.tipo_de_busqueda()
                busqueda = Busqueda(tipo_busqueda, self.dar_instance)
                busqueda.realizar_busqueda()
                busqueda.seleccionar_y_reproducir()
            
            elif opcion == 2:
                self.menu_acciones_album() #Menu para gestionar las acciones del album

            elif opcion == 3:
                self.lista_R.ver_lista_reproduccion() #Mostrara todas las musicas reproducidas

            elif opcion == 4:
                self.favorito.ver_favoritos() #Mostrara todas las musicas dentro de favoritos
            
            elif opcion == 5:
                while True:
                    nombre = input("Ingrese el nombre de la musica a eliminar: ")
                    if self.validaciones.valida_entrada(nombre):
                        break
                    
                self.favorito.eliminar_cancion(nombre)

            elif opcion == 6:
                self.recomendacion.recomendacion_semanal()
            
            elif opcion == 7:
                print("Saliendo del gestor de musica...")
                break
                
            else:
                print("Escriba una opcion valida")
    
    #Menu del gestor de album
    def menu_acciones_album(self):
        while True:
            print("Acciones para albumes: ")
            print("1. Buscar Album")
            print("2. Crear Album")
            print("3. Eliminar Album")
            print("4. Ver Album")
            print("5. Reproducir Albumes guardados")
            print("6. Eliminar musica de album")
            print("7. Salir del gestionador de album")

            accion = input("Ingrese una opcion en numero: ")

            if not self.validaciones.valida_numero(accion): #valida que sea un numero
                continue

            accion = int(accion)

            if accion == 1:
                self.gestion_album.buscar_album() #Buscamos un album
            
            elif accion == 2:
                self.gestion_album.crear_album() #Creamos un album con nombre, año y artista
            
            elif accion == 3:
                self.gestion_album.eliminar_album() #Eliminamos un album creado por el usuario
            
            elif accion == 4:
                self.gestion_album.ver_album() #Mostramos todos los albumes creados y guardados por el usuario
            
            elif accion == 5:
                self.gestion_album.reproducir_album() #Reproducimos un album creado/guardado por el usuario
            
            elif accion == 6:
                self.gestion_album.eliminar_cancion() #Eliminamos una cancion del album del usuario
            
            elif accion == 7: #Regresamos al menu principal
                print("Volviendo al menu principal...")
                print("-" *30)
                break
            
            else:
                print("Opcion invalida")

if __name__ == "__main__":
    app = Principal()
    app.menu()