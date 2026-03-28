from groq import Groq
import os
from pypdf import PdfReader

def read_document(filepath):
    if filepath.endswith(".pdf"):
        reader = PdfReader(filepath)
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append({
                    "page_number": i + 1,
                    "content": text
                })
        return pages
    else:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            return [{"page_number": 1, "content": content}]

def ask_ai(question, pages):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    document_text = ""
    for page in pages:
        document_text += f"\n[Page {page['page_number']}]\n{page['content']}\n"
        document_text = document_text[:8000]
    
    prompt = f"""You are a documentation research assistant.
Answer the user's question based on the document below.

Your response must follow this exact format:

 Found on Page: [mention exact page number]

 Exact Content:
[copy the exact relevant text from that page]

 Summary:
[explain the answer in simple words]

If the answer spans multiple pages mention all page numbers.
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
