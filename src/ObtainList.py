import requests
import difflib
import time

# Definir la URL base de la API de MyAnimeList
API_BASE_URL = 'https://api.jikan.moe/v4'

anime_list = 'input.txt'

# Abrir el archivo de entrada
with open(anime_list, 'r') as file:
  # Leer todas las líneas del archivo
  lines = file.readlines()

# Crear una lista para almacenar los animes conocidos
known_animes = []

no_corrected_animes = []
# Recorrer cada línea del archivo
for line in lines:
  # Limpiar la línea eliminando los espacios en blanco al principio y al final
  anime = line.strip()

  # Buscar el anime en la API de MyAnimeList
  response = requests.get(f'{API_BASE_URL}/anime?q={anime}&limit=1')
  data = response.json()
  

  # Si se encontró el anime, agregar su título a la lista de animes conocidos
  try:
    if data['data']:
      known_animes.append(data['data'][0]['title'])
  except:
    pass
  print("Buscando animes...")
  time.sleep(0.6)

# Crear una lista para almacenar los animes corregidos
corrected_animes = []

# Recorrer cada línea del archivo de nuevo
for line in lines:
  # Limpiar la línea eliminando los espacios en blanco al principio y al final
  anime = line.strip()

  # Si el anime está en la lista de animes conocidos, agregarlo a la lista de animes corregidos
  if anime in known_animes:
    corrected_animes.append(anime)
  # De lo contrario, buscar el anime más cercano en la lista de animes conocidos utilizando la función difflib.get_close_matches
  else:
    try:
      corrected_anime = difflib.get_close_matches(anime, known_animes,n=1,cutoff=0.5)[0]
      corrected_animes.append(corrected_anime)
      print(f"INFO::Encontrado:: Anime: {corrected_anime}")
    except:
      print(f"INFO::NO encontrado:: Anime: {corrected_anime} ")
      no_corrected_animes.append(anime)


print("\n\nAnimes no corregidos/No encontrados\n")
print(no_corrected_animes)
print("---------------\n")
# Abrir el archivo de salida
with open('output.txt', 'w') as file:
  # Escribir cada anime corregido en una línea del archivo
  for anime in known_animes:
    #print(anime)
    file.write(anime + '\n')

