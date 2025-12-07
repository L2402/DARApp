import requests
class Recomendaciones:
    def __init__ (self, dar_instance):
        self.__Api_key, self.Base_Url = dar_instance.Obtener_Valores

    def recomendacion_semanal(self):
        params = {

        'client_id': self.__Api_key,
        'format': 'json',
        'limit':10,
        'order':'popularity_week', #Pasamos que sea recomendacion semanal
        'include':'musicinfo',

    }
        
        # Realizar la solicitud
        response = requests.get(self.Base_Url, params=params)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Convertir la respuesta a formato JSON
            data = response.json()
            # Imprimir el resultado
            for track in data['results']:
                print(f"Title: {track['name']}, Artist: {track['artist_name']}")
        else:
            print(f"Error: {response.status_code}")