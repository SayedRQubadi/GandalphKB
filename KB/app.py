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
    # Debug: print out how many records we have and what query we received
    print("Query:", query)
    print("Loaded protein data:", len(protein_data), "records")
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

if __name__ == '__main__':
    app.run(debug=True)
