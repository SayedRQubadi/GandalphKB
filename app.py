from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


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

# format sequence in lines
def format_sequence_with_indices(seq, line_length=60):
    lines = []
    for i in range(0, len(seq), line_length):
        segment = seq[i:i + line_length]
        start = i + 1
        end = i + len(segment)
        # Format line: "start sequence end"
        lines.append(f"{start:<5} {segment} {end}")
    return lines


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
    match = next((r for r in sequence_data
                  if r.get('protein_code', '').lower() == protein_code.lower()), None)
    if not match:
        return "Sequence not found", 404

    raw_seq = match.get('sequence', '').replace('\n', '').strip()
    formatted = format_sequence_with_indices(raw_seq)

    return render_template('sequence_detail.html',
                           sequence_row=match,
                           formatted_sequence=formatted)


if __name__ == '__main__':
    app.run(debug=True)
