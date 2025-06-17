import csv
from flask import Flask, render_template, request

app = Flask(__name__)

# 載入資料
def load_data():
    data = []
    with open('list.txt', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    query = ''
    results = []
    data = load_data()

    if request.method == 'POST':
        if 'query' in request.form:
            query = request.form.get('query', '').strip()
            if query:
                query_lower = query.lower()
                # 模糊搜尋任一欄
                results = [row for row in data if any(query_lower in cell.lower() for cell in row)]
        elif 'show_all' in request.form:
            results = data

    return render_template('index.html', query=query, results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
