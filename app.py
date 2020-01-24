from flask import Flask
from flask import render_template, url_for, request, redirect
from message import Message

import logging


app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug') 

logging.basicConfig(filename = 'Info.log', level = logging.INFO)
log.disabled = True

@app.route('/', methods = ['GET', 'POST'])
def new_message():
	if request.method == 'GET':
		return render_template('index.html')
	elif request.method == 'POST':
		values = (None, request.form['author'], request.form['message'])
		message = Message(*values).create()
		logging.info('%s created new message!', message.author)
		return redirect('/all')

@app.route('/all')
def get_messages():
	return render_template('all.html', messages=Message.all_messages())

@app.route('/all/edit/<int:id>', methods = ['GET', 'POST'])
def edit_message(id):
	if request.method == 'GET':
		message = Message.find(id)
		return render_template('edit.html', message = message)
	elif request.method == 'POST':
		message = Message.find(id)
		message.message = request.form['edit_message'] 
		message.update()
		logging.info('%s edited message with id = %d!', message.author, message.id)
		return redirect('/all')

@app.route('/all/delete/<int:id>', methods = ['POST'])
def delete_message(id):
	message = Message.find(id)
	message.delete()
	logging.info('%s deleted message with id = %d', message.author, id)
	return redirect('/all')


if __name__ == "__main__":
	app.run(debug = True)