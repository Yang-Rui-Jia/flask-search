from flask import Flask, request, render_template, jsonify
import csv

app = Flask(__name__)

# 讀取 CSV 資料
def load_data():
    data = []
    with open('list.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

DATA = load_data()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    results = [row for row in DATA if query in row["A"].lower()]
    return jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
