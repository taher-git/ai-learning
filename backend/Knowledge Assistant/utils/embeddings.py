from sentence_transformers import SentenceTransformer
from itertools import chain

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(chunks):
    flat_chunks = list(chain.from_iterable(chunks))
    embeddings = model.encode(flat_chunks)
    return embeddings
