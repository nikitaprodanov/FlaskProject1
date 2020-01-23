from flask import Flask
from flask import render_template, url_for, request, redirect
from message import Message


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def new_message():
	if request.method == 'GET':
		return render_template('index.html')
	elif request.method == 'POST':
		values = (None, request.form['author'], request.form['message'])
		message = Message(*values).create()
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
		return redirect('/all')

@app.route('/all/delete/<int:id>', methods = ['POST'])
def delete_message(id):
	message = Message.find(id)
	message.delete()
	return redirect('/all')


if __name__ == "__main__":
	app.run(debug = True)