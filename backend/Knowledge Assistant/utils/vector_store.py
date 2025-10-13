import faiss
import numpy as np
import os
import pickle
from fastapi import HTTPException, UploadFile
from utils.file_utils import read_csv_by_bytes, read_pdf_by_bytes, read_excel_by_bytes
from typing import List, Dict

DB_PATH = "vector_dbs"
INDEX_PATH = "index/knowledge_index.faiss"
META_PATH = "index/metadata.pkl"

def store_embeddings(embeddings, chunks):
    os.makedirs("index", exist_ok=True)

    embeddings = np.array(embeddings).astype('float32')

    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            metadata = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(embeddings.shape[1])
        metadata = []

    index.add(embeddings)
    metadata.extend(chunks)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

def search_similar_chunks(query, model, top_k=3):

    query_vec = model.encode([query]).astype('float32')
    index = faiss.read_index(INDEX_PATH)

    D, I = index.search(query_vec, k=top_k)

    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)

    results = [metadata[i] for i in I[0]]
    return results

def file_exists():
    return os.path.exists(INDEX_PATH)
        

def save_doc_embeddings(doc_name: str, chunks: list[str], model):
    # Step 1: Generate embeddings
    vectors = model.encode(chunks)
    vectors = np.array(vectors).astype("float32")

    # Step 2: Build FAISS index
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    # Step 3: Write FAISS + metadata
    os.makedirs(DB_PATH, exist_ok=True)
    
    index_file = os.path.join(DB_PATH, f"{doc_name}.index")
    meta_file = os.path.join(DB_PATH, f"{doc_name}.pkl")

    faiss.write_index(index, index_file)
    
    with open(meta_file, "wb") as f:
        pickle.dump({"chunks": chunks}, f)

    print(f"✅ Saved: {index_file} + {meta_file}")

def list_docs():
    os.makedirs(DB_PATH, exist_ok=True)
    files = []
    for f in os.listdir(DB_PATH):
        if f.endswith(".index"):
            files.append(f.replace(".index", ""))
    return [to_dict(f) for f in files]


def to_dict(self):
    return {
            "filename": self,
        }

def delete_doc(doc_name: str):
    index_path = os.path.join(DB_PATH, f"{doc_name}.index")
    pkl_path = os.path.join(DB_PATH, f"{doc_name}.pkl")
    
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        os.remove(index_path)
        if os.path.exists(pkl_path):
            os.remove(pkl_path)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def build_prompt(query, model, history):
    # results = search_across_docs(query, model)
    results = query_vector_db(query, model)
    context = ""
    history_text = "\n".join([f"User: {h['user']}\nAI: {h['ai']}" for h in history[-5:]])  # last 5 turns

    for text in results:
        context += f"\n{text}\n"


    prompt = f"""
    You are an AI assistant helping with multi-document Q&A.
    Use only the provided context and recent chat history to answer the question.
    Chat history:
    {history_text}

    Context:
    {context}

    Question: {query}
    """
    return prompt

def load_all_indices():
    all_chunks = []
    all_vectors = []
    
    for file in os.listdir(DB_PATH):
        if file.endswith(".index"):
            base = file.replace(".index", "")
            index_path = os.path.join(DB_PATH, file)
            meta_path = os.path.join(DB_PATH, f"{base}.pkl")

            if not os.path.exists(meta_path):
                print(f"⚠️ Missing metadata for {base}")
                continue

            index = faiss.read_index(index_path)
            with open(meta_path, "rb") as f:
                data = pickle.load(f)
                chunks = data["chunks"]

            assert index.ntotal == len(chunks), f"❌ Mismatch in {base}"
            vectors = index.reconstruct_n(0, index.ntotal)

            all_vectors.extend(vectors)
            all_chunks.extend(chunks)

    if not all_vectors:
        raise ValueError("No FAISS indices found in DB folder.")

    # Build merged index in memory
    dim = all_vectors[0].shape[0]
    merged_index = faiss.IndexFlatL2(dim)
    merged_index.add(np.array(all_vectors).astype("float32"))

    return merged_index, all_chunks

def query_vector_db(query: str, model, top_k=3):
    index, chunks = load_all_indices()

    query_vec = model.encode([query]).astype("float32")
    D, I = index.search(query_vec, top_k)

    retrieved = []
    for i in I[0]:
        if 0 <= i < len(chunks):
            retrieved.append(chunks[i])

    return retrieved

async def read_file(file : UploadFile):
    filename = file.filename
    ext = filename.split(".")[-1].lower()
    print(ext)
    file_bytes = await file.read()
    if ext == "pdf":
        text = read_pdf_by_bytes(file_bytes, filename)
        return text
    elif ext == "txt":
        text = file_bytes.decode("utf-8", errors="ignore")
        return text
    elif ext in ["xlsx", "xls"]:
        text = read_excel_by_bytes(file_bytes, filename)
        return text
    elif ext == "csv":
        text = read_csv_by_bytes(file_bytes, filename)
        return text
    else:
        raise ValueError(f"Unsupported file type: {filename}")
