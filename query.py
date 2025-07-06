

import ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

def main():
    """Main function to query the local RAG."""
    # 1. Configuration
    embedding_model = "llama3"
    persist_directory = "chroma_db"
    llm_model = "llama3"
    ollama_base_url = "http://localhost:11434"

    # 2. Load the existing vector store
    print("Loading vector store...")
    embeddings = OllamaEmbeddings(model=embedding_model, base_url=ollama_base_url)
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

    # 3. Start the conversation loop
    print("\nReady to chat! (type 'exit' to quit)")
    while True:
        query = input("You: ")
        if query.lower() == 'exit':
            break

        # 4. Retrieve relevant context
        print("Retrieving context...")
        retriever = db.as_retriever()
        relevant_docs = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        # 5. Generate the prompt for the LLM
        prompt = f"""
        You are a helpful assistant. Use the following context to answer the user's question.
        If you don't know the answer, just say that you don't know. Don't try to make up an answer.

        Context:
        {context}

        Question: {query}

        Answer:
        """

        # 6. Query the LLM
        print("Generating answer...")
        response = ollama.chat(
            model=llm_model,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True
        )

        # 7. Stream the response
        print("Assistant: ", end="", flush=True)
        for chunk in response:
            print(chunk['message']['content'], end="", flush=True)
        print("\n")

if __name__ == "__main__":
    main()

