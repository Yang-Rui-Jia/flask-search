import csv
from flask import Flask, render_template, request

app = Flask(__name__)

# 讀 CSV，無標題，存成 list of lists
DATA = []
with open('list.csv', newline='', encoding='cp950') as f:
    reader = csv.reader(f)
    for row in reader:
        DATA.append(row)

@app.route('/', methods=['GET', 'POST'])
def index():
    query = ''
    results = []
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            query_lower = query.lower()
            # 模糊搜尋：只要關鍵字在任一欄位就找到
            results = [row for row in DATA if any(query_lower in cell.lower() for cell in row)]
    return render_template('index.html', query=query, results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
