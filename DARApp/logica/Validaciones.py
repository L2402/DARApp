class Validacion:
    
    def valida_numero(self, entrada):
            #Intentamos hacer que se convierta en un numero, 
            # de esa forma sabemos si el dato ingresado es numero o algun otro caracter
            try:
                int(entrada)
                return True
            except ValueError:
                print("La opcion ingresada no es un numero")
                return False

    def valida_entrada(self, entrada):
        #Validamos que la entrada no este vacia y eliminamos los espacios de la izquierda y de la derecha
        if not entrada.strip():
             print("La entrada no debe estar vacia")
             return False
        return True