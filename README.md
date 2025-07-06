# Lemon-Bot

Lemon-Bot is a Retrieval-Augmented Generation (RAG) chatbot that can answer questions about a website. It works by scraping a website, storing the content in a vector database, and then using a large language model (LLM) to answer questions based on the scraped content.

## How it Works

The project is divided into two main scripts:

1.  **`ingest.py`**: This script is responsible for:
    *   Scraping a website starting from a specified URL.
    *   Splitting the scraped text into smaller chunks.
    *   Generating embeddings for each chunk using a local LLM (via Ollama).
    *   Storing these embeddings in a Chroma vector database.

2.  **`query.py`**: This script provides a command-line interface to:
    *   Take a user's question.
    *   Retrieve the most relevant text chunks from the vector database.
    *   Use a local LLM (via Ollama) to generate an answer based on the retrieved context and the user's question.

## Prerequisites

*   Python 3.6+
*   Ollama running with a local LLM (e.g., Llama 3). You can download Ollama from [https://ollama.ai/](https://ollama.ai/).

## Setup

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:ikeaforever/lenmon-bot.git
    cd lemon-bot
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Pull the LLM model for Ollama:**
    ```bash
    ollama pull llama3
    ```

## Usage

1.  **Ingest the website content:**

    *   Open `ingest.py` and change the `start_url` and `domain` variables to the website you want to scrape.
    *   Run the script:
        ```bash
        python ingest.py
        ```
    *   This will create a `chroma_db` directory containing the vector store.

2.  **Query the chatbot:**

    *   Run the query script:
        ```bash
        python query.py
        ```
    *   You can now ask questions in the terminal. Type `exit` to quit.

## Configuration

You can customize the following parameters in `ingest.py` and `query.py`:

*   **`start_url`**: The initial URL to start scraping from (`ingest.py`).
*   **`domain`**: The domain to stay within when scraping (`ingest.py`).
*   **`max_pages`**: The maximum number of pages to scrape (`ingest.py`).
*   **`chunk_size` / `chunk_overlap`**: Parameters for splitting the text (`ingest.py`).
*   **`embedding_model`**: The name of the Ollama model to use for embeddings (`ingest.py` and `query.py`).
*   **`llm_model`**: The name of the Ollama model to use for generating answers (`query.py`).
*   **`persist_directory`**: The directory to save the Chroma database to (`ingest.py` and `query.py`).
*   **`ollama_base_url`**: The base URL for the Ollama API (`ingest.py` and `query.py`).
