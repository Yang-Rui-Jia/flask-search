import csv
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
CSV_FILE = 'list.csv'

def load_data():
    data = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline='', encoding='cp950') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
    return data

def save_data(data):
    with open(CSV_FILE, 'w', newline='', encoding='cp950') as f:
        writer = csv.writer(f)
        writer.writerows(data)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = load_data()
    query = ''
    results = []
    if request.method == 'POST':
        query = request.form.get('query', '').strip().lower()
        if query:
            results = [row for row in data if any(query in cell.lower() for cell in row)]
    return render_template('index.html', query=query, results=results)

@app.route('/view')
def view_all():
    data = load_data()
    return render_template('index.html', results=data)

@app.route('/add', methods=['POST'])
def add_entry():
    name = request.form.get('name', '').strip()
    link = request.form.get('link', '').strip()
    if name and link:
        data = load_data()
        data.append([name, link])
        save_data(data)
    return redirect(url_for('view_all'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete_entry(index):
    data = load_data()
    if 0 <= index < len(data):
        data.pop(index)
        save_data(data)
    return redirect(url_for('view_all'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
