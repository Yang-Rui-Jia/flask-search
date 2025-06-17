import csv
from flask import Flask, render_template, request

app = Flask(__name__)

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
    page = request.args.get('page', 1, type=int)
    per_page = 10

    if request.method == 'POST':
        if 'search' in request.form:
            query = request.form.get('query', '').strip()
            if query:
                query_lower = query.lower()
                results = [row for row in data if any(query_lower in cell.lower() for cell in row)]
            else:
                results = []
        elif 'show_all' in request.form:
            results = data
        # 重新導向到第一頁，避免 POST 重複送出
        # 但為了簡化，這裡先不做 redirect，直接繼續渲染

    # 如果是GET或POST有搜尋/顯示全部，才做分頁
    total = len(results)
    start = (page - 1) * per_page
    end = start + per_page
    paged_results = results[start:end]

    total_pages = (total + per_page -1)//per_page

    return render_template('index.html',
                           query=query,
                           results=paged_results,
                           page=page,
                           total_pages=total_pages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
