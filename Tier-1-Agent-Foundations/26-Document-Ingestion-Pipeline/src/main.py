from dataclasses import dataclass
from typing import List, Dict, Optional
import re

@dataclass
class Document:
    page_content: str
    metadata: Dict

class SimpleTextLoader:
    """Simulates loading text files."""
    def load(self, file_path: str) -> List[Document]:
        print(f"📂 Loading: {file_path}")
        # In real life: open(file_path).read()
        # Mocking content for demo
        content = (
            "Title: The History of AI\n"
            "Page 1 of 5\n"
            "Artificial Intelligence is a field of computer science.\n"
            "It began in the 1950s.\n\n"
            "Chapter 1: Beginnings\n"
            "Alan Turing proposed the Turing Test.\n"
            "This test checks for intelligence.\n"
        )
        return [Document(page_content=content, metadata={"source": file_path})]

class RecursiveCharacterTextSplitter:
    """
    Splits text recursively by trying different separators.
    """
    def __init__(self, chunk_size: int = 50, chunk_overlap: int = 10):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", ".", " "]

    def split_documents(self, documents: List[Document]) -> List[Document]:
        chunks = []
        for doc in documents:
            text = doc.page_content
            # Very simplified splitting logic for demo
            # Real impl uses recursion
            splits = self._simple_split(text)
            
            for i, split in enumerate(splits):
                meta = doc.metadata.copy()
                meta["chunk_index"] = i
                chunks.append(Document(page_content=split, metadata=meta))
        return chunks

    def _simple_split(self, text: str) -> List[str]:
        # Split by newline for simplicity in this pattern demo
        # A real implementation is 100 lines of recursion
        clean_text = re.sub(r'Page \d+ of \d+', '', text) # Simple cleaning
        return [s.strip() for s in clean_text.split('\n') if s.strip()]

class IngestionPipeline:
    def __init__(self):
        self.loader = SimpleTextLoader()
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=50)

    def run(self, file_path: str) -> List[Document]:
        raw_docs = self.loader.load(file_path)
        chunks = self.splitter.split_documents(raw_docs)
        print(f"✅ Processed {len(chunks)} chunks.")
        return chunks

# --- Example Usage ---

if __name__ == "__main__":
    pipeline = IngestionPipeline()
    
    final_chunks = pipeline.run("history_of_ai.pdf")
    
    print("\n--- Output Chunks ---")
    for doc in final_chunks:
        print(f"[{doc.metadata['chunk_index']}] {doc.page_content}")
