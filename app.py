from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
import json
import google.generativeai as genai

#Flask Setup
app = Flask(__name__)
DB_NAME = "tasks.db"
API_KEY = "AIzaSyAagh9NiZlZNEg-so--9ZbvYSe60TN63Og"

#Gemini Task Prioritizer
class GeminiTaskPrioritizer:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

    def prioritize_tasks(self, tasks):
        prompt = "You are a productivity assistant. Prioritize the following tasks by urgency and importance:\n\n"
        for idx, task in enumerate(tasks, 1):
            prompt += f"{idx}. {task['title']} - {task['description']} (Due: {task['deadline']})\n"
        prompt += (
            "\nReturn the tasks as a raw JSON array of objects using this format:\n"
            '[{"title": "...", "description": "...", "deadline": "..."}]\n'
            "Do NOT include markdown formatting or triple backticks."
        )

        response = self.model.generate_content(prompt)
        return json.loads(response.text.strip("` "))

#DB Functions
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            deadline TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_all_tasks():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, description, deadline FROM tasks")
    rows = c.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "description": row[2], "deadline": row[3]} for row in rows]


def add_task(title, description, deadline):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, deadline) VALUES (?, ?, ?)", (title, description, deadline))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def update_task(task_id, title, description, deadline):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tasks SET title=?, description=?, deadline=? WHERE id=?", (title, description, deadline, task_id))
    conn.commit()
    conn.close()

#Routes
@app.route('/')
def index():
    tasks = get_all_tasks()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    deadline = request.form['deadline']
    add_task(title, description, deadline)
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete(task_id):
    delete_task(task_id)
    return redirect(url_for('index'))


@app.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    title = request.form['title']
    description = request.form['description']
    deadline = request.form['deadline']
    update_task(task_id, title, description, deadline)
    return redirect(url_for('index'))


@app.route('/prioritize')
def prioritize():
    tasks = get_all_tasks()
    if not tasks:
        return jsonify({"error": "No tasks to prioritize"}), 400
    gemini = GeminiTaskPrioritizer(API_KEY)
    try:
        prioritized = gemini.prioritize_tasks(tasks)
        return jsonify(prioritized)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
