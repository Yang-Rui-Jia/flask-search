from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def load_data():
    with open('list.csv', newline='', encoding='cp950') as f:
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
            # 搜尋 A 欄位符合的資料，假設A欄位名稱是 'A'
            results = [row for row in DATA if row['A'] == query]
    return render_template('index.html', query=query, results=results)

if __name__ == '__main__':
    # 讓外部能連進來，port 10000 跟你之前設定的一致
    app.run(host='0.0.0.0', port=10000)
