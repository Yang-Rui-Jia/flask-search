from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def load_data():
    with open('list.csv', newline='', encoding='cp950') as f:  # 繁體中文編碼
        reader = csv.DictReader(f)
        data = [row for row in reader]
    return data

DATA = load_data()

@app.route('/', methods=['GET', 'POST'])
def index():
    query = ''
    results = []
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            query_lower = query.lower()
            # 模糊搜尋：只要輸入的字串包含在 A 欄裡就找出來
            results = [row for row in DATA if query_lower in row['A'].lower()]
    return render_template('index.html', query=query, results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
