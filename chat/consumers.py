import json

from channels import Channel
from channels.auth import channel_session_user, channel_session_user_from_http
from django.contrib.auth.models import User

from .models import (Room)


@channel_session_user_from_http
def ws_connect(message, channel):
    reply = {"accept": False}
    try:
        User.objects.filter(username=channel).get()
    except:
        message.reply_channel.send(reply)
        return
    try:
        room = Room.find_by_hash_of(channel, message.user)
        reply = {"accept": True}
    except:
        try:
            room = Room(members=[channel, message.user.username])
            room.save()
            reply = {"accept": True}
        except:
            room = None
    try:
        assert len(room.name)
        message.reply_channel.send(reply)
        room.channel.add(message.reply_channel)
    except:
        message.reply_channel.send(reply)


def ws_receive(message, channel):
    payload = json.loads(message['text'])
    payload['channel'] = channel
    payload['reply_channel'] = message.content['reply_channel']
    Channel("chat.receive").send(payload)


@channel_session_user
def ws_disconnect(message, channel):
    room = Room.findByHashOf(message.user, channel)
    room.channel.discard(message.reply_channel)


@channel_session_user
def chat_receive(message):
    channel = message.get('channel', None)
    try:
        User.objects.filter(username=channel).get()
    except:
        ws_disconnect(message, channel)
        return
    try:
        room = Room.find_by_hash_of(message.user, channel)
        try:
            room.send(message)
        except Exception as e:
            print(str(e))
    except:
        ws_disconnect(message, channel)