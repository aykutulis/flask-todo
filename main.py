from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


@app.get('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.post('/add')
def add():
    title = request.form.get('title')
    todo = Todo(title=title, completed=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.get('/complete/<int:todo_id>')
def complete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.completed = True
    db.session.commit()
    return redirect(url_for('index'))


@app.get('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    completed = db.Column(db.Boolean)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
