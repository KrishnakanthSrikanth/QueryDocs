import io
from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import time
import pandas as pd
from script import sentence_parser
from sentence_transformers import SentenceTransformer, util
import nltk

nltk.download('punkt')

app = Flask(__name__)

# Defining testing user creds (to be replaced with a secure method)
user_credentials = {
    'Test': 'Tester123'
}


# First page
@app.route('/')
def index():
    return render_template('login.html', body_class='login')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        pwd = request.form.get('password')
        if not user_name or not pwd:
            error_msg = 'Please enter both username and password.'
            return render_template('login.html', error=error_msg, body_class='login')

        if user_name in user_credentials and user_credentials[user_name] == pwd:
            return redirect(url_for('pdf_parser', username=user_name.title()))
        else:
            error_msg = 'Invalid credentials. Please try again!'
            return render_template('login.html', error=error_msg, body_class='login')
    return render_template('login.html', body_class='login')


# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('registration.html', body_class='register')


# Check for user registration
@app.route('/register_check', methods=['GET', 'POST'])
def register_check():
    """
    !!!!!!!!!!..To be implemented..!!!!!!!!!!
    """
    return redirect(url_for('login'))


# PDF Parsing Page
@app.route('/pdf_parser')
def pdf_parser():
    username = request.args.get('username')
    return render_template('pdfParser.html', username=username, body_class='pdfParser')


# PDF Parsing and Similarity Scoring
@app.route('/parse', methods=['POST'])
def parse():
    uploaded_files = request.files.getlist("file")
    query_input = request.form.get('query_input')
    use_pypdf = request.form.get('use_pypdf')
    use_ocr = request.form.get('use_ocr')

    input_folder = 'input'
    app.config['INPUT_FOLDER'] = input_folder

    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    sentences_with_metadata = []

    for file in uploaded_files:
        temp_file_path = os.path.join(input_folder, file.filename)
        file.save(temp_file_path)

        parsed_sentences = sentence_parser(temp_file_path, parsing_method="pypdf")

        for idx, item in enumerate(parsed_sentences):
            sentences_with_metadata.append({
                'Page Number': item['Page'],
                'Filename': item['Filename'],
                'Sentence': item['Sentence']
            })

        os.remove(temp_file_path)

    df = pd.DataFrame(sentences_with_metadata)

    if not df.empty:
        model = SentenceTransformer("all-mpnet-base-v2")
        start_time = time.time()
        query_embedding = model.encode(query_input)
        sentence_embeddings = model.encode(df['Sentence']).tolist()
        scores = util.dot_score(query_embedding, sentence_embeddings)[0]

        df['Relevancy'] = scores.tolist()
        df['Relevancy'] = df['Relevancy'].apply(lambda x: round(x * 100))

        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total execution time: {total_time} seconds")

        sorted_df = df.sort_values(by='Relevancy', ascending=False)
        sorted_df['Relevancy'] = sorted_df['Relevancy'].apply(lambda x: f"{x}%")

        return render_template('results.html', tables=[sorted_df.to_html(classes='data', index=False)],
                               titles=sorted_df.columns.values, body_class='results')
    else:
        return "No data found."


# Download results to CSV
@app.route('/download', methods=['POST'])
def download():
    csv_data = request.form.get('csv_data')
    if not csv_data:
        return "No CSV data provided", 400
    df = pd.read_csv(io.StringIO(csv_data))
    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return send_file(csv_buffer,
                     mimetype='text/csv',
                     download_name='results.csv',
                     as_attachment=True)


# Main function
if __name__ == "__main__":
    app.run(debug=True, port=4100)
