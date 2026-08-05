# 📄 Generative AI Document Assistant

A Generative AI-powered document question-answering application that allows users to upload PDF documents and ask questions based on their content.

The project implements a **Retrieval-Augmented Generation (RAG)** pipeline using document processing, text chunking, embeddings, vector search, and Large Language Models (LLMs).

---

## 🚀 Features

- 📄 Upload and process PDF documents
- 🧹 Extract and clean text from PDFs
- ✂️ Split documents into manageable text chunks
- 🧠 Generate semantic embeddings
- 🗄️ Store document embeddings in ChromaDB
- 🔍 Perform semantic similarity search
- 🤖 Generate answers using an LLM
- 📚 Ask questions based on uploaded documents
- 🎯 Retrieve relevant document chunks before generating answers
- 📑 Support document-specific retrieval
- 🚫 Detect previously indexed documents
- 💬 Interactive Streamlit interface

---

## 🧠 How It Works

The application follows a Retrieval-Augmented Generation (RAG) workflow:

1. User uploads a PDF document.
2. Text is extracted from the PDF.
3. Extracted text is cleaned.
4. The document is divided into smaller chunks.
5. Each chunk is converted into an embedding vector.
6. Embeddings and document metadata are stored in ChromaDB.
7. The user enters a question.
8. The question is converted into an embedding.
9. ChromaDB retrieves the most relevant document chunks.
10. Retrieved context is passed to the LLM.
11. The LLM generates an answer based on the retrieved document content.

### RAG Pipeline

User Uploads PDF  
↓  
PDF Text Extraction  
↓  
Text Cleaning  
↓  
Document Chunking  
↓  
Embedding Generation  
↓  
ChromaDB Vector Storage  
↓  
User Question  
↓  
Query Embedding  
↓  
Semantic Retrieval  
↓  
Relevant Context  
↓  
LLM  
↓  
Generated Answer

---

## 🛠️ Technologies Used

### Programming Language
- Python

### Generative AI / NLP
- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Sentence Transformers
- Hugging Face embedding models

### Embedding Model
- `sentence-transformers/all-MiniLM-L6-v2`

### Vector Database
- ChromaDB

### LLM Integration
- Groq
- OpenAI
- Google Generative AI

### PDF Processing
- PyMuPDF

### User Interface
- Streamlit

### Configuration
- python-dotenv

### Version Control
- Git
- GitHub

---

## 📂 Project Structure

```text
Generative_AI_Document_Assistant/
│
├── app/
│   ├── services/
│   │   ├── embedding_service.py
│   │   ├── indexing_service.py
│   │   ├── retriever_service.py
│   │   ├── vector_store.py
│   │   ├── pdf_loader.py
│   │   ├── text_cleaner.py
│   │   └── chunker.py
│   │
│   ├── document.py
│   └── embedded_chunk.py
│
├── data/
├── index_documents.py
├── main.py
├── streamlit_app.py
├── requirements.txt
├── .gitignore
└── README.md
