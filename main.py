import tensorflow as tf
tf.get_logger().setLevel('ERROR')
import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from pdf_parser import extract_text_from_pdf
from chunk_embed import chunk_text, get_embeddings, embed_query
from qdrant_manager import setup_collection, upload_to_qdrant, search_chunks
from rag_answer import generate_answer



load_dotenv()
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
QDRANT_URL = os.getenv('QDRANT_URL')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

COLLECTION_NAME = "pdf_collection"

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = ""
    if request.method == 'POST':
        pdf = request.files.get('pdf')
        question = request.form.get('question')

        if pdf:
            filename = secure_filename(pdf.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            pdf.save(filepath)

            text = extract_text_from_pdf(filepath)
            chunks = chunk_text(text)
            embeddings = get_embeddings(chunks)

            setup_collection(COLLECTION_NAME)
            upload_to_qdrant(COLLECTION_NAME, chunks, embeddings)

        if question:
            query_vector = embed_query(question)
            context_chunks = search_chunks(COLLECTION_NAME, query_vector)
            context = " ".join(context_chunks)
            answer = generate_answer(context, question)

    return render_template('index.html', answer=answer)

if __name__ == "__main__":
    app.run(debug=True)  # This starts the Flask app
