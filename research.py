from groq import Groq
import os
from pypdf import PdfReader

def read_document(filepath):
    if filepath.endswith(".pdf"):
        reader = PdfReader(filepath)
        pages = []
        for i, page in enumerate(reader.pages):
            if i >= 3:
                break
            text = page.extract_text()
            if text and text.strip():
                pages.append({
                    "page_number": i + 1,
                    "content": text[:500]
                })
        return pages
    else:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            return [{"page_number": 1, "content": content[:2000]}]

def ask_ai(question, pages):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    document_text = ""
    for page in pages:
        document_text += f"\n[Page {page['page_number']}]\n{page['content']}\n"

    document_text = document_text[:2000]
    
    prompt = f"""Answer this question based only on this document:

Document:
{document_text}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content
