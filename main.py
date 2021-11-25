import random
import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import secret_constants
from cac import Cities
from correct_cities import correct_cities

vk_session = vk_api.VkApi(token=secret_constants.TOKEN)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

players_in_game = []
active_games = []


def kill_game(game):
    user_ids = game.user_ids
    active_games.pop(active_games.index(game))
    players_in_game.remove(user_ids[0])


def is_correct_event(event):
    return event.to_me and event.type == VkEventType.MESSAGE_NEW


def send_message(user_id, message):
    vk_session.method("messages.send", {"user_id": user_id, "message": message, "random_id": 0})


a = ["норм", "отлично", "плохо", "хорошо", "ужасно"]


def is_play_game(event):
    game_commannd = ['начало', 'города']
    return event.text.lower() in game_commannd


def main():
    user_in_queue = None
    for event in longpoll.listen():
        if is_correct_event(event):
            if event.text == 'hi':
                send_message(event.user_id, 'Привет, я бот, а ты попуск!')
        if is_play_game(event):
            send_message(event.user_id, 'Вы встали в очередь на игру в города!')

        elif event.text == 'How are you?':
            if user_in_queue is None:
                send_message(event.user_id, random.choice(a))
                user_in_queue = event.user_id
            elif event.user_id != user_in_queue:
                send_message(user_in_queue, 'Мы нашли вам игру, удачи!')
                send_message(event.user_id, 'Оппонент уже ожидает вас')
                first_user = active_games.append(Cities(user_in_queue))
                send_message(first_user, 'Вы первый! Назовите любой город')
                players_in_game.append(user_in_queue)
                players_in_game.append(event.user_id)
                first_user = active_games[-1].user_ids[-1].user_ids[active_games[-1].current_step]
                send_message(first_user, 'Ты первый, НАЧИНАЙ!')
                user_in_queue = None
        elif event.user_id in players_in_game:
            bad = False
            igra = ''
            for game in active_games:
                if event.user_id in game.user_ids:
                    if game.user_ids.index(event.user_id) == game.current_step:
                        bad = True
                        break
                    else:
                        igra = game
            if bad:
                send_message(event.user_id, 'Ты шо дурачёк не твой ход!!!!!')
                continue
            user2 = igra.user_ids[1 - igra.current_step]
            if not game.is_correct_first_char(event.text[0].upper()):
                kill_game(igra)
                send_message(event.user_id, 'Ты назвал город не на ту букву - чё совсем дурачёк?')
                send_message(igra.user_ids[1 - igra.current_step], 'Красава')
                send_message(igra.user_ids[1 - igra.current_step], 'Красава')
                kill_game(igra)
                continue

            city = event.text.capitalize()
            if city not in correct_cities:
                send_message(event.user_id, 'Такого города нет в нашем списке!')
                send_message(user2, 'Вы победили!')
                kill_game(igra)
                continue
            if igra.is_unused_city(city):
                send_message(event.user_id, 'Такой город уже назван, ты проиграл!')
                send_message(user2, 'Вы победили!')
            igra.used_cities.append(city)
            igra.change_last_char(city)
            igra.current_step = 1 - igra.current_step
            send_message(user2, 'Ваш ход! Оппонент назвал город: ' + city + '.\nВам на букву: ' + igra.last_char)


main()
