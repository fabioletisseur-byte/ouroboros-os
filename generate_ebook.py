from pathlib import Path
from html import escape
import requests
from ebooklib import epub

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

TITLE = "AKHANO — Tome 1 : Le Tisseur du Destin"
AUTHOR = "FABIO LAROUS (Le Tisseur)"


def generate_text(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "num_ctx": 4096
            }
        },
        timeout=900
    )
    response.raise_for_status()
    data = response.json()
    return data.get("response", "").strip()


def paragraphs_to_html(text: str) -> str:
    paragraphs = []

    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if paragraph:
            paragraphs.append(f"<p>{escape(paragraph)}</p>")

    return "\n".join(paragraphs)


def create_epub(generated_text: str) -> None:
    book = epub.EpubBook()

    book.set_identifier("akhano-tome-1")
    book.set_title(TITLE)
    book.set_language("fr")
    book.add_author(AUTHOR)

    style = """
    body {
        font-family: Georgia, serif;
        line-height: 1.6;
        margin: 5%;
        color: #1a1a1a;
    }

    h1 {
        text-align: center;
        margin-top: 2em;
        margin-bottom: 1em;
    }

    h2 {
        text-align: center;
        font-style: italic;
    }

    p {
        text-align: justify;
        text-indent: 1.4em;
        margin-bottom: 0.7em;
    }

    .center {
        text-align: center;
        text-indent: 0;
    }
    """

    css = epub.EpubItem(
        uid="style",
        file_name="style/style.css",
        media_type="text/css",
        content=style.encode("utf-8")
    )

    book.add_item(css)

    title_page = epub.EpubHtml(
        title="Titre",
        file_name="title.xhtml",
        lang="fr"
    )

    title_page.content = f"""
    <html>
    <head><title>{escape(TITLE)}</title></head>
    <body>
        <h1>{escape(TITLE)}</h1>
        <p class="center">{escape(AUTHOR)}</p>
    </body>
    </html>
    """

    title_page.add_item(css)

    content_page = epub.EpubHtml(
        title="Récit principal",
        file_name="content.xhtml",
        lang="fr"
    )

    content_page.content = f"""
    <html>
    <head><title>Récit principal</title></head>
    <body>
        <h1>Récit principal</h1>
        {paragraphs_to_html(generated_text)}
    </body>
    </html>
    """

    content_page.add_item(css)

    back_page = epub.EpubHtml(
        title="Quatrième de couverture",
        file_name="back.xhtml",
        lang="fr"
    )

    back_page.content = """
    <html>
    <head><title>Quatrième de couverture</title></head>
    <body>
        <h1>Quatrième de couverture</h1>
        <p>
        Quand les fils d’or bioluminescents s’éveillent sous la chair,
        les scarifications cyan révèlent la mémoire des anciens.
        </p>
    </body>
    </html>
    """

    back_page.add_item(css)

    sections = [title_page, content_page, back_page]

    for section in sections:
        book.add_item(section)

    book.toc = tuple(sections)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav"] + sections

    epub.write_epub("Akhano_Tome1_Ollama.epub", book, {})


def main() -> None:
    print("Démarrage d’Ouroboros en mode local...")
    print(f"Modèle Ollama utilisé : {MODEL}")

    prompt = """
Tu es un auteur de dark fantasy afro-futuriste.

Écris un extrait original du Tome 1 d’AKHANO — Le Tisseur du Destin,
en français.

Contraintes :
- 1 000 à 1 500 mots ;
- narration immersive ;
- pas de commentaire sur ton rôle d’IA ;
- pas de résumé ni d’explication ;
- personnages, décor et conflit clairement présents ;
- style sombre, poétique et visuel.
"""

    generated_text = generate_text(prompt)

    if not generated_text:
        raise RuntimeError("Ollama a renvoyé un texte vide.")

    Path("generated_text.txt").write_text(
        generated_text,
        encoding="utf-8"
    )

    create_epub(generated_text)

    Path("KIT_MARKETING.md").write_text(
        f"""# Kit marketing — {TITLE}

**Auteur :** {AUTHOR}

## Description courte

Un récit de dark fantasy afro-futuriste où les fils du destin
s’éveillent dans la chair et la mémoire.

## Accroches

- Et si ton destin brillait sous ta peau ?
- Les anciens ont laissé des fils. Quelqu’un doit les suivre.
- AKHANO : le premier fil d’une saga mystique.
""",
        encoding="utf-8"
    )

    print("EPUB créé : Akhano_Tome1_Ollama.epub")
    print("Texte créé : generated_text.txt")
    print("Marketing créé : KIT_MARKETING.md")


if __name__ == "__main__":
    main()
