from groq import Groq
import os
from pypdf import PdfReader

def read_document(filepath):
    if filepath.endswith(".pdf"):
        reader = PdfReader(filepath)
        pages = []
        for i, page in enumerate(reader.pages):
            if i >= 5:
                break
            text = page.extract_text()
            if text and text.strip():
                pages.append({
                    "page_number": i + 1,
                    "content": text[:1000]
                })
        return pages
    else:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            return [{"page_number": 1, "content": content[:5000]}]

def ask_ai(question, pages):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    document_text = ""
    for page in pages:
        document_text += f"\n[Page {page['page_number']}]\n{page['content']}\n"

    document_text = document_text[:5000]
    
    prompt = f"""You are a documentation research assistant.
Answer the user's question based on the document below.
Always mention the page number where you found the answer.
If the answer is not in the document, say "I could not find that in the document."

Document:
{document_text}

Question: {question}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
