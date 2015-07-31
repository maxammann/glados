from flask import Flask, jsonify, request
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import pympris

mpris = None
app = Flask(__name__)


@app.route("/play")
def play():
    mpris.player.Play()
    return jsonify(result="success")


@app.route("/pause")
def pause():
    mpris.player.Pause()
    return jsonify(result="success")


@app.route("/title")
def title():
    return jsonify(result=mpris.player.Metadata['xesam:title'])


@app.route("/seek")
def seek():
    mpris.player.Seek(int(request.args.get('offset')) * 10e6)
    return jsonify(result="success")


if __name__ == '__main__':
    dbus_loop = DBusGMainLoop()
    bus = dbus.SessionBus(mainloop=dbus_loop)

    players_ids = list(pympris.available_players())

    mpris = pympris.MediaPlayer(players_ids[0], bus)

    app.run(port=28781)
