import requests
import time

# Reemplaza YOUR_API_KEY con tu client id y YOUR_ACCESS_TOKEN con tu token de acceso
api_key = "YOUR_API_KEY" # CLIENT ID
access_token ="YOUR_ACCESS_TOKEN"

# Lista de animes Corregida
anime_list ="output.txt"

# Dirección URL de la API de MyAnimeList
api_url1 = "https://api.myanimelist.net/v1"
api_url2 = "https://api.myanimelist.net/v2"


response2 = requests.get(f"{api_url1}/users/@me/animelist?limit=1000", headers={
  'Authorization':f'Bearer {access_token}'
})


# Abre el archivo de texto con la lista de animes
with open(anime_list) as f:
  # Lee cada línea del archivo
  for line in f:
    # Elimina el carácter de nueva línea del final de la línea
    anime_name = line.strip()

    # Utiliza la API de MyAnimeList para buscar el anime
    response = requests.get(f"{api_url1}/anime?q={anime_name}", headers={
      "X-MAL-CLIENT-ID": f"{api_key}"
    })
    # Si la respuesta es exitosa
    if response.status_code == 200:
      # Obtén la información del anime
      anime_info = response.json()

      # Si se encontró el anime
      if anime_info:

        if not any(d.get('node', {}).get('id') == anime_info["data"][0]['node']['id'] for d in response2.json()['data']):
        
          # Obtén el primer anime de la lista de resultados
          anime = anime_info["data"][0]
          #print(anime)
          
          data = {'status': 'completed','score': '5','num_watched_episodes': '1'}

          headers = {'Authorization':f'Bearer {access_token}'}
          
          
          # Agrega el anime a la lista de animes vistos
          response = requests.put(f"{api_url2}/anime/{anime['node']['id']}/my_list_status", headers=headers, data=data)

          # Si la respuesta es exitosa
          if response.status_code == 201 or response.status_code == 200:
            # Imprime un mensaje de éxito
            print(f"{anime['node']['title']} agregado a la lista de animes vistos\n\n")

          # Si hay un error
          else:
            # Imprime un mensaje de error
            print(f"Error al agregar {anime['node']['title']} a la lista de animes vistos: {response.status_code}\n\n")
          time.sleep(0.2)

        # Si no se encontró el anime
        else:
          print(f"WARNING:: El anime: {anime_name} ya esta en tu MAL")
          
      else:
        # Imprime un mensaje de error
        print(f"No se pudo encontrar el anime {anime_name}\n\n")
    # Si hay un error

    else:
      # Imprime un mensaje de error
      print(f"Error al buscar el anime {anime_name}: {response.json()['error']}\n \n")
    # Espera 1 segundo antes de enviar la siguiente solicitud para no exceder el límite de solicitudes por hora
    time.sleep(1)
