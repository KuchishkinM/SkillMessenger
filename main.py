from flask import Flask, request, render_template

app = Flask(__name__)
all_messages = []


@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


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
    # Ограничение: не более 100 сообщений в чате
    if len(all_messages) > 99:
        all_messages.pop(0)
        all_messages.append(new_message)
    else:
        all_messages.append(new_message)


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
                'Текс не может быть короче 1 символов.'
            )
        if len(text) > 100:
            raise TypeError(
                'Текс не может быть длиннее 3000 символов.'
            )
    add_message(sender, text)
    return {'result': True}


@app.route('/chat')
def chat_page():
    return render_template('form.html')


app.run(debug=True)
