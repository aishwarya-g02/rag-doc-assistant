from dotenv import load_dotenv
import os
from app.research import ask_ai, read_document

load_dotenv()

document_path = "data/research.pdf"
document_text = read_document(document_path)

print("=== RAG Documentation Research Assistant ===")
print(f"Document loaded: {document_path}")
print("Type 'quit' to exit\n")

while True:
    question = input("Ask a question about the document: ")
    if question.lower() == "quit":
        print("Goodbye!")
        break
    print("\nAI Response:", ask_ai(question, document_text))
    print("-" * 50)