# coding: utf-8
import os
import json
import re
import requests
from config import CONFIG
from fbmq import Attachment, Template, QuickReply, NotificationType
from fbpage import page
from rivescript import RiveScript
from rivescript_redis import RedisSessionManager
from util import topicos
from util import elimina_tildes

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

USER_SEQ = {}

bot = RiveScript(session_manager=RedisSessionManager())
bot.load_directory("./rs")
bot.sort_replies()

page.greeting("LinguaBot+, tu mejor opción para el repaso del idioma inglés.")

page.show_starting_button("START_PAYLOAD")


#MÉTODOS MODIFICADOS Y/O CREADOS


@page.callback(['START_PAYLOAD'])
def start_callback(payload, event):
    print("Let's start!")


def set_persistent_menu():
    post_fields = {
        'persistent_menu': [
            {
                'locale': 'default',
                "composer_input_disabled": False,
                "call_to_actions": [
                    {
                        "title": "My Account",
                        "type": "nested",
                        "call_to_actions": [
                            {
                                "title": "Pay Bill",
                                "type": "postback",
                                "payload": "PAYBILL_PAYLOAD"
                            },
                            {
                                "title": "History",
                                "type": "postback",
                                "payload": "HISTORY_PAYLOAD"
                            },
                            {
                                "title": "Contact Info",
                                "type": "postback",
                                "payload": "CONTACT_INFO_PAYLOAD"
                            }
                        ]
                    },
                    {
                        "type": "web_url",
                        "title": "Latest News",
                        "url": "http://petershats.parseapp.com/hat-news",
                        "webview_height_ratio": "full"
                    }
                ]
            }
        ]
    }
    requests.post("https://graph.facebook.com/v2.6/me/messenger_profile?access_token=" +
                      CONFIG['FACEBOOK_TOKEN'], json=post_fields)


def delete_persistent_menu():
    delete = {
        "fields": [
            "persistent_menu"
        ]
    }
    requests.delete("https://graph.facebook.com/v2.6/me/messenger_profile?access_token=" +
                      CONFIG['FACEBOOK_TOKEN'], data=json.dumps(delete))

@page.handle_message
def received_message(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_message = event.timestamp
    message = event.message
    print("Received message for user %s and page %s at %s with message:"
          % (sender_id, recipient_id, time_of_message))
    print(message)

    seq = message.get("seq", 0)
    message_id = message.get("mid")
    app_id = message.get("app_id")
    metadata = message.get("metadata")

    message_text = message.get("text")
    message_attachments = message.get("attachments")
    quick_reply = message.get("quick_reply")

    seq_id = sender_id + ':' + recipient_id
    if USER_SEQ.get(seq_id, -1) >= seq:
        print("Ignore duplicated request")
        return None
    else:
        USER_SEQ[seq_id] = seq

    send_typing_on(sender_id)
    send_read_receipt(sender_id)

    if message_text:
        print("Topic= ", bot.get_uservar(sender_id, "topic"))
        if quick_reply:
           entrada_usuario = event.quick_reply_payload.replace('PICK_', '')
        else:
            entrada_usuario = message_text
        res_bot = bot.reply(sender_id, elimina_tildes(entrada_usuario))
        res_ejem = re.search('¿[Qq]uieres.*', res_bot)
        res_topic = re.search('[Cc]u[aá]l(?:es)? de los (?P<topico>.*) (?:te interesa|quieres) '
                               'repasar', res_bot)
        res_tema = re.search('[Cc]u[aá]l (?P<tema>.*) (?:(?:es el que\s?)?quieres|te interesan|'
                             'saber m[aá]s)(?:\slos)? (?:ejemplos)?', res_bot)
        if res_topic:
            send_quick_reply(sender_id, res_bot, genera_quick_replies(
                topicos[elimina_tildes(res_topic.group('topico').replace(' ', '_'))]))
        elif res_tema:
            send_quick_reply(sender_id, res_bot, genera_quick_replies(
                topicos[elimina_tildes(res_tema.group('tema').replace(' ', '_'))]))
        elif res_ejem:
            send_quick_reply(sender_id, res_bot, genera_quick_replies(["si", "no"]))
        else:
            page.send(sender_id, res_bot)
            entrada_usuario = message_text
        res_bot = bot.reply(sender_id, elimina_tildes(entrada_usuario))




def manejar_saludos(sender_id, nombre_usuario):
    if bot.get_uservar(sender_id, 'nombre') is None:
        mensaje = "Parece que es la primera vez que vienes por aquí.\n" \
                  "¡Te doy la bienvenida como tu asesor de inglés!\n"\
                  "¿Cómo estás el día de hoy?"
    else:
        mensaje = "¡Qué gusto volver a verte!\n" \
                  "¿Cómo estás el día de hoy?"
    bot.set_uservar(sender_id, 'nombre', nombre_usuario)
    page.send(sender_id, "Hola" + nombre_usuario + ".\n" + mensaje)


@page.handle_postback
def received_postback(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp

    payload = event.postback_payload

    delete_persistent_menu()

    print("Received postback for user %s and page %s with payload '%s' at %s"
          % (sender_id, recipient_id, payload, time_of_postback))
    manejar_saludos(sender_id, page.get_user_profile(event.sender_id)['first_name'])


def send_quick_reply(recipient, pregunta, quick_replies):
    """
    Shortcuts are supported
    page.send(recipient, "What's your favorite movie genre?",
                quick_replies=[{'title': 'Action', 'payload': 'PICK_ACTION'},
                               {'title': 'Comedy', 'payload': 'PICK_COMEDY'}, ],
                metadata="DEVELOPER_DEFINED_METADATA")
    """
    page.send(recipient, pregunta, quick_replies=quick_replies,
              metadata="DEVELOPER_DEFINED_METADATA")


def genera_quick_replies(palabras):
    quick_replies = []
    for palabra in palabras:
        quick_replies.append({'title': palabra.title(), 'payload': 'PICK_' + palabra.upper()})
    return quick_replies

# AQUÍ TERMINAN LOS MÉTODOS MODIFICADOS Y/O CREADOS



@page.handle_optin
def received_authentication(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_auth = event.timestamp

    pass_through_param = event.optin.get("ref")

    print("Received authentication for user %s and page %s with pass "
          "through param '%s' at %s" % (sender_id, recipient_id, pass_through_param, time_of_auth))

    page.send(sender_id, "Authentication successful")


@page.handle_echo
def received_echo(event):
    message = event.message
    message_id = message.get("mid")
    app_id = message.get("app_id")
    metadata = message.get("metadata")
    print("page id : %s , %s" % (page.page_id, page.page_name))
    print("Received echo for message %s and app %s with metadata %s" % (message_id, app_id, metadata))


@page.handle_delivery
def received_delivery_confirmation(event):
    delivery = event.delivery
    message_ids = delivery.get("mids")
    watermark = delivery.get("watermark")

    if message_ids:
        for message_id in message_ids:
            print("Received delivery confirmation for message ID: %s" % message_id)

    print("All message before %s were delivered." % watermark)


@page.handle_read
def received_message_read(event):
    watermark = event.read.get("watermark")
    seq = event.read.get("seq")

    print("Received message read event for watermark %s and sequence number %s" % (watermark, seq))


@page.handle_account_linking
def received_account_link(event):
    sender_id = event.sender_id
    status = event.account_linking.get("status")
    auth_code = event.account_linking.get("authorization_code")

    print("Received account link event with for user %s with status %s and auth code %s "
          % (sender_id, status, auth_code))
