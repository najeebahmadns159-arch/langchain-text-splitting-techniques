# 🧩 LangChain Text Splitting Techniques

A beginner-friendly collection of scripts that show **five different ways to split text into chunks** using LangChain. Text splitting (chunking) is one of the most important steps in building RAG (Retrieval-Augmented Generation) applications, because the quality of your chunks directly affects the quality of retrieval and answers.

Each script is small, self-contained and focused on a single technique, so you can read, run and compare them easily.

---

## 📌 Table of Contents

- [Why Text Splitting Matters](#-why-text-splitting-matters)
- [Techniques Covered](#-techniques-covered)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Environment Setup](#-environment-setup)
- [Usage](#-usage)
- [How Each Script Works](#-how-each-script-works)
- [Comparison of Techniques](#-comparison-of-techniques)
- [Key Parameters Explained](#-key-parameters-explained)
- [Known Notes and Tips](#-known-notes-and-tips)
- [Future Improvements](#-future-improvements)
- [Tech Stack](#-tech-stack)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Why Text Splitting Matters

Large Language Models have a limited context window, and embedding models work best on focused pieces of text. If we feed a whole document, we lose precision and waste tokens. If we cut text carelessly, we break sentences, code blocks or ideas in half.

A good splitter:

- keeps related content together
- stays inside a size limit (characters or tokens)
- preserves structure (paragraphs, headings, functions)
- improves retrieval accuracy in RAG systems

---

## 🧠 Techniques Covered

### 1. Length-Based Splitting
Splits text purely by size using `CharacterTextSplitter`. Simple and fast, but it does not understand meaning or structure. The demo loads a PDF with `PyPDFLoader` and splits the pages.

### 2. Recursive Character Splitting
Uses `RecursiveCharacterTextSplitter`, which tries separators in order (paragraph, line, space, character) so chunks stay as natural as possible. This is the most commonly recommended default splitter.

### 3. Markdown-Aware Splitting
Uses `RecursiveCharacterTextSplitter.from_language(Language.MARKDOWN)` so the split happens at headings, lists and code blocks instead of random positions.

### 4. Code-Aware Splitting (Python)
Uses `Language.PYTHON` so chunks break at class and function boundaries rather than in the middle of a method.

### 5. Semantic Splitting
Uses `SemanticChunker` with OpenAI embeddings. It compares the meaning of consecutive sentences and creates a new chunk whenever the topic changes (for example, from farming and IPL to terrorism).

---

## 📁 Project Structure

```
langchain-text-splitting-techniques/
│
├── 01_length_based.py          # fixed-size splitting on a PDF
├── 02_recursive_splitter.py    # recursive character splitting
├── 03_markdown_splitter.py     # markdown-aware splitting
├── 04_python_code_splitter.py  # python code-aware splitting
├── 05_semantic_splitter.py     # embedding-based semantic splitting
│
├── requirements.txt            # python dependencies
├── .env.example                # sample environment file
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/langchain-text-splitting-techniques.git
cd langchain-text-splitting-techniques
```

**2. Create a virtual environment**

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Setup

Only the semantic splitter (`05_semantic_splitter.py`) needs an API key, because it creates embeddings using OpenAI.

1. Copy the sample file:
```bash
   cp .env.example .env
```
2. Open `.env` and add your key:
```
   OPENAI_API_KEY=your_openai_api_key_here
```

> ⚠️ Never commit your real `.env` file. It is already listed in `.gitignore`.

---

## ▶️ Usage

Run any script directly:

```bash
python 02_recursive_splitter.py
python 03_markdown_splitter.py
python 04_python_code_splitter.py
python 05_semantic_splitter.py
```

For `01_length_based.py`, place your PDF in the project folder and update the file name inside the script:

```python
loader = PyPDFLoader("your-file.pdf")
```

Then run:

```bash
python 01_length_based.py
```

---

## 🔍 How Each Script Works

### `01_length_based.py`
- Loads a PDF using `PyPDFLoader`
- Splits it with `CharacterTextSplitter` (`separator=""`, `chunk_overlap=0`)
- Prints the resulting `Document` objects
- With a very large `chunk_size`, each page stays as one chunk. Lower it (for example, 1000) to see real splitting.

### `02_recursive_splitter.py`
- Takes a short paragraph about space exploration
- Splits with `chunk_size=500`, `chunk_overlap=0`
- Prints the number of chunks and the chunks themselves

### `03_markdown_splitter.py`
- Takes a sample README-style markdown text
- Uses markdown separators (headings, lists, code fences)
- Prints the number of chunks and the first chunk

### `04_python_code_splitter.py`
- Takes a small `Student` class plus example usage
- Uses Python separators (`class`, `def`, blank lines)
- Prints the number of chunks and the second chunk

### `05_semantic_splitter.py`
- Embeds sentences using `OpenAIEmbeddings`
- Detects topic shifts using `breakpoint_threshold_type="standard_deviation"` with `breakpoint_threshold_amount=3`
- Prints the number of semantic chunks and their content

---

## 📊 Comparison of Techniques

| Technique | Understands Meaning | Respects Structure | Speed | Cost | Best For |
|---|---|---|---|---|---|
| Length-based | ❌ | ❌ | ⚡ Very fast | Free | Quick prototypes, uniform data |
| Recursive | ⚠️ Partly | ✅ Paragraphs and sentences | ⚡ Fast | Free | General purpose default |
| Markdown | ⚠️ Partly | ✅ Headings and lists | ⚡ Fast | Free | Docs, READMEs, notes |
| Code (Python) | ⚠️ Partly | ✅ Classes and functions | ⚡ Fast | Free | Code search, code RAG |
| Semantic | ✅ | ✅ Topic boundaries | 🐢 Slower | Paid (embeddings) | Mixed-topic long documents |

---

## 🧾 Key Parameters Explained

| Parameter | Meaning |
|---|---|
| `chunk_size` | Maximum size of each chunk |
| `chunk_overlap` | Number of characters shared between neighbouring chunks, which helps keep context |
| `separator` | Character(s) used to split (used in `CharacterTextSplitter`) |
| `language` | Language whose syntax rules guide the split (Python, Markdown, etc.) |
| `breakpoint_threshold_type` | How the semantic splitter decides a topic change (`percentile`, `standard_deviation`, `interquartile`, `gradient`) |
| `breakpoint_threshold_amount` | Sensitivity of the breakpoint. Lower value means more chunks. |

---

## 💡 Known Notes and Tips

- Increase `chunk_overlap` (for example, 50 to 100) for real RAG use, so context is not lost at chunk edges.
- `SemanticChunker` needs an OpenAI API key and makes API calls, so it costs a little money.
- On very small sample texts, semantic splitting may return only one or two chunks. Try longer text to see the effect.
- Chunk size is measured in characters here. For token-based splitting, use `from_tiktoken_encoder`.

---

## 🚀 Future Improvements

- [ ] Add token-based splitting with `tiktoken`
- [ ] Add `MarkdownHeaderTextSplitter` to keep header metadata
- [ ] Add HTML and JSON splitters
- [ ] Add free local embeddings (HuggingFace) for the semantic splitter
- [ ] Build a small chunk-visualization notebook
- [ ] Connect the chunks to a vector store (FAISS or Chroma) for a full RAG demo

---

## 🛠 Tech Stack

- **Language:** Python 3.10+
- **Framework:** LangChain
- **Embeddings:** OpenAI
- **PDF Loader:** PyPDF
- **Config:** python-dotenv

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repo
2. Create a branch: `git checkout -b feature/new-splitter`
3. Commit your changes: `git commit -m "add new splitter demo"`
4. Push: `git push origin feature/new-splitter`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. Feel free to use it for learning and in your own projects.

---

## 👤 Author

**Najeeb**
B.Sc. Data Science and Computer Science, Jamia Millia Islamia, New Delhi

If this repo helped you, consider giving it a ⭐
