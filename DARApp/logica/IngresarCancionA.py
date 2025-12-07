from Validaciones import Validacion
from Album import Album
from Favorito import Favorito
from Dar import Dar

class Pregunta:

    def __init__(self, cancion):
        self.cancion = cancion
        self.validaciones = Validacion()
        self.dar_instancia = Dar()
        self.album = Album(self.dar_instancia)
        self.favorito = Favorito(cancion.titulo, cancion.artista, cancion.url) #Accedemos a los atributos de la clase cancion por medio del objeto

    def agregar_a(self):

        salir = False

        while not salir:
            print("Desea agregar la musica a:")
            print("1. Album")
            print("2. Favorito")
            print("3. Album y favorito")
            print("4. Ninguna opcion")

            while True: #Bucle infinito que se ejecutara hasta que sea una opcion valida
                opcion = input("Ingrese una opcion: ")

                if self.validaciones.valida_numero(opcion):
                    break
            
            opcion = int(opcion)
        
            if opcion == 1:

                while True:
                    nombre = input("Ingrese el nombre del album al cual ingresar la cancion: ")
                    if self.validaciones.valida_entrada(nombre):
                        break
                
                self.album.agregar_cancion(nombre, self.cancion.titulo, self.cancion.artista, self.cancion.url)
                salir = True
                #Tuvimos un error al importar esta clase en el inicio del programa
                #Por que haciamos una importacion circular
                #Asi que se importa cada que se necesita para evitar ese problema
                from Principal import Principal
                principal = Principal()
                principal.menu()
            
            elif opcion == 2:
                self.favorito.agregar_cancion()
                salir = True
                from Principal import Principal
                principal = Principal()
                principal.menu()
            
            elif opcion == 3:

                while True:
                    nombre = input("Ingrese el nombre del album al cual ingresar la cancion: ")
                    if self.validaciones.valida_entrada(nombre):
                        break;
                
                self.album.agregar_cancion(nombre, self.cancion.titulo, self.cancion.artista, self.cancion.url)
                self.favorito.agregar_cancion()
                salir = True
                from Principal import Principal
                principal = Principal()
                principal.menu()

            elif opcion == 4:
                print("Regresando al menu principal...")
                salir = True
                from Principal import Principal
                principal = Principal()
                principal.menu() #Regresamos al menu principal

            else:
                print("Elija una opcion valida")