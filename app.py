from flask import Flask, render_template, request, redirect, url_for
import csv

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
    data = load_data()
    per_page = 10

    if request.method == 'POST':
        # 轉成 GET 參數導向，避免 POST 分頁問題
        query = request.form.get('query', '').strip()
        show_all = 'show_all' in request.form
        if show_all:
            return redirect(url_for('index', show_all=1, page=1))
        else:
            return redirect(url_for('index', query=query, page=1))

    # GET 請求
    query = request.args.get('query', '').strip()
    show_all = request.args.get('show_all')
    page = request.args.get('page', 1, type=int)

    if show_all:
        results = data
    elif query:
        query_lower = query.lower()
        results = [row for row in data if any(query_lower in cell.lower() for cell in row)]
    else:
        results = []

    total = len(results)
    start = (page - 1) * per_page
    end = start + per_page
    paged_results = results[start:end]

    total_pages = (total + per_page - 1) // per_page

    return render_template('index.html',
                           query=query,
                           results=paged_results,
                           page=page,
                           total_pages=total_pages,
                           show_all=show_all)
