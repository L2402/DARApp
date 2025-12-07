class Dar:

    def __init__ (self):
        self.__Api_Key = '2ff35d77'
        self.Base_Url = 'https://api.jamendo.com/v3.0/tracks/'

    @property
    def Obtener_Valores(self):
        return self.__Api_Key, self.Base_Url