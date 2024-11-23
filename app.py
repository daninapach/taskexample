from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Pending')

class KnowledgeBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'POST':
        data = request.get_json()
        new_task = Task(title=data['title'], description=data.get('description', ''), status=data.get('status', 'Pending'))
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully'}), 201
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'description': task.description, 'status': task.status} for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def update_delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'PUT':
        data = request.get_json()
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        db.session.commit()
        return jsonify({'message': 'Task updated successfully'})
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/knowledge', methods=['GET', 'POST'])
def manage_knowledge():
    if request.method == 'POST':
        data = request.get_json()
        new_entry = KnowledgeBase(title=data['title'], content=data['content'])
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'message': 'Knowledge base entry created successfully'}), 201
    entries = KnowledgeBase.query.all()
    return jsonify([{'id': entry.id, 'title': entry.title, 'content': entry.content} for entry in entries])

if __name__ == '__main__':
    app.run(debug=True)
