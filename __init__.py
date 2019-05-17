import os, random, subprocess
from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_socketio import SocketIO, join_room, leave_room, emit, send

from util import db, commands

app = Flask(__name__) #create instance of class flask

app.secret_key = os.urandom(32)
socketio = SocketIO(app)

rooms = {}

@app.route('/')
def root():
    return render_template("index.html", guest='user' not in session)

@socketio.on('joinRoom')
def joinRoom(roomInfo):
    if len(roomInfo) == 0:
        return
    join_room(roomInfo)
    rooms[request.sid] = roomInfo

@socketio.on('message')
def message(msg):
    if len(msg) != 0:
        send(msg, room = rooms[request.sid])

@app.route('/base')
def base():
    guest = 'user' not in session
    user = None
    if not guest: user = session['user']
    return render_template("base.html", guest = guest, user = user)

@app.route('/lobby')
def lobby():
    guest = 'user' not in session
    user = None
    if not guest: user = session['user']
    return render_template("lobby.html", guest=guest, user = user)

@app.route('/game/<code>')
def game(code):
    guest = 'user' not in session
    user = None
    if not guest: user = session['user']
    return render_template("game.html", guest=guest, user = user, code = code)

@app.route('/join_game', methods = ['POST'])
def join_game():
    print(request.form)
    inv_code = request.form['inv_code']
    return redirect('/game/{code}'.format(code=inv_code))


@app.route('/create_game', methods = ['POST'])
def create_game():
    print(request.form)
    game_name = request.form['game_name']
    max_players = int(request.form['max_players'])
    private_game = 'private_game' in request.form
    print(game_name)
    print(max_players)
    print(private_game)
    if game_name == "":
        flash("Enter a name",category="create_game_error")
        return redirect(url_for('lobby'))
    inv_code = ''.join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")for n in range(32)])
    if max_players == 0:
        max_players = 2
        flash("Max players has defaulted to " + str(max_players))
        return redirect('/game/{code}'.format(code=inv_code))
    return redirect('/game/{code}'.format(code=inv_code))

@app.route('/user')
def user():
    guest = 'user' not in session
    if guest:
        return redirect("/login")
    user = None
    if not guest: user = session['user']
    return render_template("user.html", guest=guest, user = user)

@app.route('/login')
def login():
    guest = 'user' not in session
    if not guest:
        return redirect(url_for('user'))
    return render_template('login.html', guest=guest)

@app.route('/login_auth', methods = ['POST'])
def login_auth():
    username = request.form['username']
    password = request.form['password']
    if commands.auth_user(username, password):
        session['user'] = username
        flash("You have logged in")
        return redirect('/')
    else:
        flash("Invalid username and password combination")
        return render_template('login.html')

@app.route('/signup')
def signup():
    guest = 'user' not in session
    return render_template("signup.html", guest=guest)

@app.route('/signup_auth', methods = ['POST'])
def register_auth():
    username = request.form['username']
    password = request.form['password']
    retyped_pass = request.form['repass']
    if username == "":
        flash("Enter a username")
        return redirect(url_for('signup'))
    elif password == "":
        flash("Enter a password")
        return redirect(url_for('signup'))
    elif password != retyped_pass:
        flash("Passwords do not match")
        return redirect(url_for('signup'))
    else:
        if commands.add_user(username, password):
            flash("You have successfully registered")
        else:
            flash("This username is already in use")
            return redirect(url_for('signup'))
    commands.auth_user(username, password)
    session['user'] = username
    return redirect('/')


@app.route('/logout', methods = ['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('/'))


@app.route('/uhoh')
def uhoh():
    return render_template('uhoh.html')

@app.route('/git_it', methods = ['POST'])
def git_it():
    username = request.form['username']
    woah = "uh sir"
    return render_template('uhoh.html', woah = username)


if __name__ == '__main__':
    db.create_table()
    socketio.run(app, debug = True)
