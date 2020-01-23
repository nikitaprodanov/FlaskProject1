from database import DB

class Message:
	def __init__(self, id, author, message):
		self.id = id
		self.author = author
		self.message = message

	def create(self):
		with DB() as db:
			values = (self.author, self.message)
			db.execute(
				'INSERT INTO messages (author, message) VALUES (?, ?)',
				values
	        )
			return self

	@staticmethod
	def all_messages():
		with DB() as db:
			rows = db.execute('SELECT * FROM messages').fetchall()
			return [Message(*row) for row in rows]

	def update(self):
		with DB() as db:
			db.execute('UPDATE messages SET message = ? WHERE id = ?', (self.message, self.id))
			return self

	@staticmethod
	def find(id):
		with DB() as db:
			row = db.execute('SELECT * FROM messages WHERE id = ?', (id,)).fetchone()
			return Message(*row)

	def delete(self):
		with DB() as db:
			db.execute('DELETE FROM messages WHERE id = ?', (self.id,))