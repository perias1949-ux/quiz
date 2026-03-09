from readability import Document
from bs4 import BeautifulSoup

def clean_html_to_text(html_content: str) -> dict:
    """Extra main article content using readability and clean it using BS4."""
    doc = Document(html_content)
    title = doc.title()
    summary_html = doc.summary()
    
    soup = BeautifulSoup(summary_html, "html.parser")
    
    # Remove navigation menus, ads, scripts that might somehow remain
    for element in soup(["script", "style", "nav", "footer", "aside"]):
        element.decompose()
        
    text = soup.get_text(separator="\n")
    
    # Clean up excess whitespace/newlines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned_text = "\n".join(lines)
    
    return {
        "title": title,
        "content": cleaned_text
    }
