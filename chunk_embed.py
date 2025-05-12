from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size - overlap)]

def get_embeddings(chunks):
    return model.encode(chunks).tolist()

def embed_query(query):
    return model.encode([query])[0].tolist()
