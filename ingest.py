
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from urllib.parse import urljoin, urlparse

def scrape_website(start_url, domain, max_pages=10):
    """
    Recursively scrapes a website starting from start_url,
    staying within the given domain.
    """
    visited_urls = set()
    urls_to_visit = [start_url]
    all_text = ""
    pages_scraped = 0

    while urls_to_visit and pages_scraped < max_pages:
        url = urls_to_visit.pop(0)
        if url in visited_urls:
            continue

        print(f"Scraping: {url}")
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            visited_urls.add(url)
            pages_scraped += 1

            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.body.get_text(separator=' ', strip=True)
            all_text += text + "\n\n"

            # Find and add new links
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                parsed_full_url = urlparse(full_url)

                # Stay on the same domain and avoid already visited URLs
                if parsed_full_url.netloc == domain and full_url not in visited_urls:
                    urls_to_visit.append(full_url)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")

    return all_text

def main():
    """Main function to ingest website data."""
    # 1. Configuration
    start_url = "https://min.io/docs/minio/kubernetes/upstream/index.html"  # <<< IMPORTANT: CHANGE THIS
    domain = "min.io"           # <<< IMPORTANT: AND THIS
    max_pages = 10                     # Limit the number of pages to scrape
    chunk_size = 1000
    chunk_overlap = 200
    embedding_model = "llama3"
    persist_directory = "chroma_db"
    ollama_base_url = "http://localhost:11434"

    # 2. Scrape Website Content
    print(f"Starting web scrape at {start_url} within domain {domain}...")
    document_text = scrape_website(start_url, domain, max_pages)
    if not document_text:
        print("No content scraped. Exiting.")
        return

    # 3. Split the document into chunks
    print("Splitting document into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    docs = text_splitter.split_text(document_text)

    # 4. Create embeddings
    print(f"Creating embeddings with '{embedding_model}'...")
    embeddings = OllamaEmbeddings(model=embedding_model, base_url=ollama_base_url)

    # 5. Create and persist the vector store
    print(f"Creating and persisting vector store to '{persist_directory}'...")
    db = Chroma.from_texts(
        texts=docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print("Ingestion complete!")

if __name__ == "__main__":
    main()
