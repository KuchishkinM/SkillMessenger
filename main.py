from flask import Flask, request, render_template
import json

app = Flask(__name__)
DATA_FILE = 'data.json'


def load_messages():
    with open(DATA_FILE, 'r') as json_file:
        data = json.load(json_file)
        return data['all_messages']


all_messages = load_messages()


def save_messages():
    with open(DATA_FILE, 'w') as json_file:
        data = {'all_messages': all_messages}
        json.dump(data, json_file)


@app.route('/')
def hello_world():
    return "<p>Hello, welcome to <b>Skill</b> <i>Messenger</i>!</p>" \
           "<p><a href=\"/chat\">Chat</a></p>" \
           "<p><a href=\"/info\">Info</a></p>"


@app.route('/get_messages')
def get_messages():
    return {'messages': all_messages}


def add_message(sender, text):
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    new_message = {
        "sender": sender,
        "text": text,
        "time": current_time,
    }
    all_messages.append(new_message)
    save_messages()
    # Ограничение: не более 100 сообщений в чате
    # if len(all_messages) > 99:
    #    all_messages.pop(0)
    #    all_messages.append(new_message)
    #    save_messages()
    # else:
    #    all_messages.append(new_message)
    #    save_messages()


@app.route('/send_message')
def send_message():
    sender = request.args['sender']
    if len(sender) < 3 or len(sender) > 100:
        raise TypeError(
            'Имя не может быть короче 3 символов.'
        )
    if len(sender) > 100:
        raise TypeError(
            'Имя не может быть длиннее 100 символов.'
        )
    text = request.args['text']
    if len(text) < 1 or len(sender) > 3000:
        if len(text) < 3 or len(sender) > 100:
            raise TypeError(
                'Текст не может быть короче 1 символов.'
            )
        if len(text) > 100:
            raise TypeError(
                'Текст не может быть длиннее 3000 символов.'
            )
    add_message(sender, text)
    return {'result': True}


@app.route("/info")
def info_page():
    return f"<p>Total of messages in chat: <b>{len(all_messages)}</b></p>" \
           f"<p><a href=\"/../chat\">Chat</a></p>" \
           f"<p><a href=\"/..\">Main page</a></p>"


@app.route('/chat')
def chat_page():
    return render_template('form.html')


if __name__ == '__main__':
    app.run()
