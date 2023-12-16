# -*- coding: utf-8 -*-
"""pokebot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18pvXSkF1yAMF29UwaOvRXUWgXo2QJiTk
"""

!pip install vk_api
!pip install python_dotenv

import vk_api
import os
import json
from random import randrange
from urllib.request import Request, urlopen
from vk_api.longpoll import VkEventType, VkLongPoll

TOKEN = 'vk1.a.OnSJdGzkye0jOUmN2ZJQMFW3R8nm6X0YVmeLZKXW2io25wIaaG_aU2yVXRjFT0lQdmjQIGhBbzb26hzdvi3iU_nVC1GSAm5HxtZC2YsEYVPz9OcWuSZtDfJqROLrWXTi1Paasw8897w1zzzZsD7Bg8zNnIXCIwrysiMUoP0ctSwS9ioR3oTmNrg8DGeD9gJ7DTfe7on82VS0XOi_frw2PA'

vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

req = Request("https://pokeapi.co/api/v2/pokemon", headers = {'User-Agent': 'Mozilla/5.0'})
response = urlopen(req)
count = json.loads(response.read())['count']

req = Request(f'https://pokeapi.co/api/v2/pokemon/?limit={count}', headers = {'User-Agent': 'Mozilla/5.0'})
response = urlopen(req)
pokemons = json.loads(response.read())['results']

for event in longpoll.listen():
  if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text.lower():
    if event.from_user:
      for pokemon in pokemons:
        if pokemon['name'] == event.text:
          req = Request(pokemon["url"], headers={'User-Agent': 'Mozilla/5.0'})
          response = urlopen(req)
          desc = json.loads(response.read())
          message = f"Имя: {desc['name']}\nРост: {desc['height']}\nВес: {desc['weight']}"
          vk.messages.send(user_id=event.user_id, message=message, random_id=randrange(1, 1000000))
          break