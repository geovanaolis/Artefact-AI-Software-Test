# 🎸 Artefact AI – Intelligent Store Assistant

An AI-powered virtual assistant designed to provide intelligent customer support for a musical instruments store. The agent combines **Google Gemini**, **Retrieval-Augmented Generation (RAG)**, and **SQL database queries** to answer customer questions using both store policies and real-time operational data.

## ✨ Features

- **AI-Powered Conversations:** Uses Google Gemini to understand natural language queries and generate contextual responses.
- **RAG (Retrieval-Augmented Generation):** Retrieves relevant information from the store's documentation to answer questions about policies, warranties, refunds, and other procedures.
- **SQL Integration:** Queries the store's database to retrieve structured information, such as product availability, prices, and inventory.
- **Context-Aware Responses:** Combines information from multiple sources to provide accurate and comprehensive answers.
- **Interactive Terminal:** Allows users to interact with the assistant directly through the command line.

## 🛠️ Technologies

- **Python:** Core programming language.
- **Google Gemini:** Large Language Model (LLM) for natural language understanding and response generation.
- **SQLite:** Relational database for storing and querying operational data.
- **ChromaDB:** Vector database for semantic search and document retrieval.
- **RAG:** Architecture for grounding AI responses in the store's knowledge base.

## 📁 Project Structure

```text
Artefact-AI-Software-Test/
│
├── src/
│   └── agent.py
│
├── tests/
│   └── test_agent.py
│
├── requirements.txt
├── README.md
└── .env
```

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone <https://github.com/geovanaolis/Artefact-AI-Software-Test>
cd Artefact-AI-Software-Test
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment:

**Windows (Git Bash):**
```bash
source venv/Scripts/activate
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project's root directory and add your Google Gemini API key:

```ini
GOOGLE_API_KEY=your_actual_gemini_api_key_here
```

> **Note:** Keep your API key private. Never commit your `.env` file to version control.

## ▶️ Running the Agent

To start the interactive virtual assistant, execute:

```bash
python src/agent.py
```

Once running, you can interact with the assistant directly through your terminal.

## 💬 Example Queries

The following examples demonstrate the agent's capabilities:

**1. Store Policies (RAG)**

Retrieve information from the store's documentation:

```text
Qual é a política de reembolso para instrumentos musicais?
```

**2. Operational Data (SQL)**

Retrieve structured information from the store's database:

```text
Quais guitarras temos disponíveis em estoque e qual o preço?
```

**3. Combined Queries (RAG + SQL)**

Combine operational data and business policies in a single response:

```text
Gostaria de comprar um violão Yamaha. Qual o valor e posso parcelar em 3x sem juros segundo as regras da loja?
```

## 🧪 Running Automated Tests

The project includes an automated test script to evaluate the agent's responses across different scenarios.

Run the following command from the project root:

```bash
python tests/test_agent.py
```

The test suite covers:

- Store information, including address and opening hours.
- Product availability and inventory queries.
- Warranty policies and documentation retrieval.

Each test displays the query, the agent's response, and its execution status.

## 🔐 Environment & Security

- Store API keys and credentials in environment variables.
- Never expose sensitive credentials in source code.
- Add `.env` and `venv/` to `.gitignore`.
- Keep dependencies documented in `requirements.txt`.

## 📌 Project Goals

This project demonstrates the integration of Large Language Models with traditional database systems and semantic information retrieval.

Its primary goal is to build an intelligent assistant capable of handling natural language queries while combining structured and unstructured data sources to deliver relevant, context-aware responses.

---

**Developed as part of the Artefact AI Software Test.**