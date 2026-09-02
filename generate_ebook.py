import os
import requests
from ebooklib import epub

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Erreur : La clé GEMINI_API_KEY est absente des secrets GitHub.")

print("Démarrage de la génération d'AKHANO...")

# Appel à l'API Gemini
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
prompt_text = (
    "Rédige le Chapitre 1 du roman Afro-Fantasy 'AKHANO'. "
    "Ambiance dark fantasy, scarifications cyan, fils d'or bioluminescents, "
    "sensualité mystique (18+). Style immersif et visuel."
)

payload = {
    "contents": [{"parts": [{"text": prompt_text}]}]
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

try:
    generated_text = data['candidates'][0]['content']['parts'][0]['text']
except Exception as e:
    print(f"Erreur réponse API : {data}")
    raise e

# Construction du fichier EPUB
book = epub.EpubBook()
book.set_identifier("akhano-tome-1")
book.set_title("AKHANO — Tome 1 : Le Tisseur du Destin")
book.set_language("fr")
book.add_author("Fabio LAROUS (Le Tisseur)")

c1 = epub.EpubHtml(title="Chapitre 1", file_name="chap_1.xhtml", lang="fr")
formatted_html = "".join([f"<p>{paragraph}</p>" for paragraph in generated_text.split("\n") if paragraph.strip()])
c1.content = f"<h1>Chapitre 1 — L'Éveil des Fils</h1>{formatted_html}"

book.add_item(c1)
book.toc = (epub.Link("chap_1.xhtml", "Chapitre 1", "chap1"),)
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

style = 'body { font-family: Georgia, serif; line-height: 1.6; }'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
book.add_item(nav_css)
book.spine = ['nav', c1]

epub.write_epub("Akhano_Tome1_BestSeller.epub", book, {})

# Génération du Kit Marketing
with open("KIT_MARKETING.md", "w", encoding="utf-8") as f:
    f.write("# Kit Marketing — AKHANO Tome 1\n\n")
    f.write("## Hook TikTok\n'Quand les fils d'or s'éveillent, le destin se tisse dans l'ombre...'\n\n")
    f.write("## Pitch Newsletter\nDécouvrez le premier tome de la saga Afro-Fantasy d'AKHANO.\n")

print("Génération réussie : EPUB et Kit Marketing créés !")
