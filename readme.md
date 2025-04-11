Intelligent Task Manager
________________________

A web-based productivity tool that lets you manage and prioritize your tasks with the help of Google Gemini AI. Add, edit, delete, and automatically prioritize tasks based on urgency and importance.

----Features----
-Add tasks with title, description, and deadline
-Edit and delete existing tasks
-View current tasks in a clean layout
-AI-powered task prioritization using Gemini 2.0 Flash
-Persistent storage using SQLite
-Lightweight UI with Milligram CSS framework


Technologies Used
_________________

Frontend: HTML, CSS (Milligram), Vanilla JavaScript
Backend: Python (Flask)
AI Integration: Google Generative AI (Gemini 2.0 Flash)
Database: SQLite



Setup Instructions
__________________

Install dependencies
-pip install -r requirements.txt

Run the app
-python app.py
-Visit http://127.0.0.1:5000/ in your browser.



🧠 How Task Prioritization Works
The app sends your current task list to Gemini with a prompt asking it to rank tasks by urgency and importance. The model returns a JSON-formatted list in the new order, which is then rendered in the browser.