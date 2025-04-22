from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

# Load protein data from CSV
def load_protein_data():
    proteins = []
    with open('proteins.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            proteins.append(row)
    return proteins

def load_sequence_data():
    sequences = []
    with open('sequences.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sequences.append(row)
    return sequences

sequence_data = load_sequence_data()


# In-memory cache of CSV data
protein_data = load_protein_data()

@app.route('/')
def index():
    # Render the main search page
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    # Retrieving the query from request args
    query = request.args.get('query', '').strip()
    if query:
        # Case-insensitive substring match over both 'protein_code' and 'protein_name'
        query_lower = query.lower()
        results = [p for p in protein_data if query_lower in p['protein_code'].lower() or query_lower in p['protein_name'].lower()]
    else:
        results = []
    return jsonify(results)

@app.route('/protein/<protein_code>')
def protein_detail(protein_code):
    # Find the protein ignoring case
    match = None
    for p in protein_data:
        if p['protein_code'].lower() == protein_code.lower():
            match = p
            break
    if not match:
        return "Protein not found", 404

    # Render a simple detail page with all protein fields
    return render_template('protein_detail.html', protein=match)

@app.route('/sequence/<protein_code>')
def sequence_detail(protein_code):
    # Find the matching row
    match = None
    for row in sequence_data:
        if row['protein_code'].lower() == protein_code.lower():
            match = row
            break

    if not match:
        return "Sequence not found", 404

    # 'match' now has { "protein_code": "XXX", "sequence": "ATCG..." }
    return render_template('sequence_detail.html', sequence_row=match)


if __name__ == '__main__':
    app.run(debug=True)
