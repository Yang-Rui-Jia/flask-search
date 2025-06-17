import csv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 輔助函數：讀取 TXT 資料
def read_txt():
    data = []
    with open('list.txt', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

# 輔助函數：新增資料到 TXT
def append_to_txt(a_value, b_value):
    with open('list.txt', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([a_value, b_value])

@app.route('/', methods=['GET', 'POST'])
def index():
    query = ''
    results = []
    data = read_txt()

    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            query_lower = query.lower()
            results = [row for row in data if any(query_lower in cell.lower() for cell in row)]
    return render_template('index.html', query=query, results=results)

@app.route('/add', methods=['POST'])
def add():
    a_value = request.form.get('a_value', '').strip()
    b_value = request.form.get('b_value', '').strip()
    if a_value and b_value:
        append_to_txt(a_value, b_value)
    return redirect(url_for('index'))

@app.route('/view-txt')
def view_txt():
    data = read_txt()
    return render_template('view_csv.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
