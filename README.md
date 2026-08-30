# 🤖 Simple RAG Chatbot

A simple **Retrieval-Augmented Generation (RAG) chatbot** that allows users to upload a PDF document and ask questions about its content.

The application extracts text from the uploaded PDF, splits it into smaller chunks, stores the information in a vector database, and uses Google Gemini to generate answers based on the relevant document content.

## ✨ Features

* 📄 Upload PDF documents
* 🔍 Extract text from PDFs
* ✂️ Split documents into smaller chunks
* 🧠 Create document embeddings
* 🗄️ Store embeddings using ChromaDB
* 🤖 Ask questions about the uploaded document
* 💬 Interactive Streamlit chat interface
* 🌙 Modern dark-themed UI
* 🔐 API key stored securely using `.env`

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **Google Gemini API**
* **ChromaDB**
* **PyPDF**
* **scikit-learn**
* **python-dotenv**

## 📂 Project Structure

```text
Simple-Rag-Chatbot/
│
├── data/
├── app.py
├── document_loader.py
├── text_splitter.py
├── vector_store.py
├── rag_pipeline.py
├── requirements.txt
├── .env
└── .gitignore
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Simple-Rag-Chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Add your Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

**Important:** Never upload your `.env` file or API key to GitHub.

### 6. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## 🚀 How It Works

```text
PDF Upload
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Question
    ↓
Relevant Document Chunks
    ↓
Google Gemini
    ↓
Answer
```

## 💡 Example Questions

After uploading a PDF, you can ask questions such as:

* What is this document about?
* What are the key aspects of this document?
* Summarize the main points.
* What are the important findings?
* Explain this topic in simple words.

## 🔐 Security

API keys are stored in the `.env` file and excluded from Git using `.gitignore`.

Never commit or share your API key publicly.

## 📌 Project Purpose

This project demonstrates the basic implementation of a **Retrieval-Augmented Generation (RAG) system** using Python, vector search, and a generative AI model.

---

**Built with Python, Streamlit, ChromaDB, and Google Gemini.**
