from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query = request.form.get('query', '').strip().lower()
        if query:
            with open('data.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row and query in row[0].lower():
                        results.append({'A': row[0], 'B': row[1] if len(row) > 1 else ''})
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
