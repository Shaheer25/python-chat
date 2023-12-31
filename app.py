from flask import Flask,render_template,request,session,redirect , url_for
from flask_socketio import join_room , leave_room,send ,SocketIO
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config['SECRET_KEY'] = "hesoyam"
socketio= SocketIO(app)

rooms = {}

def get_code(length):
    while True:
        code = " "
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break
    return code
@app.route('/',methods=["POST","GET"])
def home():
    session.clear
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join",False)
        create = request.form.get("create",False)

        if not name :
            return render_template("home.html", error = "Please Enter a Name", code = code, name=name)
        
        if join is False and not code:
            return render_template("home.html",error="Enter a Room Code", code = code, name=name)
        
        room = code
        if create != False:
            room = get_code(4)
            rooms[room]={"members":0,"messages":[]}
        elif code not in room:
            return render_template("home.html",error = "Room Doesn't Exist", code = code, name=name)
        session["room"] = room
        session["name"] = name
        return redirect (url_for("room.html"))
    
    return render_template("home.html")

@app.route("/room")
def room():
    return render_template("room.html")


if __name__ == '__main__':
    socketio.run(app,debug=True)
