import os
import google.generativeai as genai
from ebooklib import epub

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Erreur : La clé GEMINI_API_KEY est absente des secrets GitHub.")

print("Démarrage du système Ouroboros Publisher OS...")

# Configuration du SDK Google Gemini
genai.configure(api_key=api_key)

# Détection dynamique du modèle actif sur le compte
print("Recherche automatique du modèle Gemini disponible...")
available_models = []
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
except Exception as e:
    print(f"Avertissement lors de la liste des modèles : {e}")

selected_model_name = None
preferred_order = [
    "models/gemini-2.5-flash",
    "models/gemini-2.0-flash",
    "models/gemini-1.5-flash-002",
    "models/gemini-1.5-flash-001",
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro",
    "models/gemini-flash-latest"
]

for pref in preferred_order:
    if pref in available_models:
        selected_model_name = pref
        break

if not selected_model_name and available_models:
    selected_model_name = available_models[0]

if not selected_model_name:
    selected_model_name = "gemini-2.0-flash"

print(f" Modèle sélectionné avec succès : {selected_model_name}")
model = genai.GenerativeModel(selected_model_name)

# Génération du contenu textuel Best-Seller
prompt_text = (
    "Tu es un auteur et éditeur de best-sellers. "
    "Rédige le contenu captivant du Tome 1 de la saga Afro-Fantasy 'AKHANO — Le Tisseur du Destin'. "
    "Auteur : FABIO LAROUS (Le Tisseur). "
    "Ambiance : Dark Fantasy, scarifications cyan, fils d'or bioluminescents, sensualité mystique (18+), héritage afro-caraïbéen. "
    "Style immersif, riche et visuel digne d'un grand roman best-seller."
)

response = model.generate_content(prompt_text)
generated_text = response.text if response.text else "Contenu en cours de tissage..."

# Construction de l'EPUB Best-Seller Professionnel
book = epub.EpubBook()
book.set_identifier("akhano-tome-1-bestseller")
book.set_title("AKHANO — Tome 1 : Le Tisseur du Destin")
book.set_language("fr")
book.add_author("FABIO LAROUS (Le Tisseur)")

# Styles CSS professionnels
style = '''
@page { margin: 5% 5%; }
body { font-family: 'Georgia', serif; line-height: 1.8; color: #1a1a1a; margin: 0; padding: 0; }
h1 { font-family: 'Cinzel', 'Times New Roman', serif; text-align: center; font-size: 2em; margin-top: 2em; margin-bottom: 1em; text-transform: uppercase; letter-spacing: 2px; color: #111; }
h2 { font-family: 'Georgia', serif; text-align: center; font-size: 1.4em; margin-top: 1.5em; color: #333; font-style: italic; }
p { text-indent: 1.5em; margin-bottom: 0.5em; text-align: justify; }
.no-indent { text-indent: 0; }
.center { text-align: center; text-indent: 0; }
.title-page { text-align: center; margin-top: 25%; }
.author-name { font-size: 1.5em; font-weight: bold; letter-spacing: 3px; margin-top: 2em; text-transform: uppercase; }
.copyright-page { font-size: 0.85em; text-align: center; margin-top: 30%; color: #555; text-indent: 0; }
.dedication { font-style: italic; text-align: center; margin-top: 35%; text-indent: 0; }
.back-cover { padding: 8%; background-color: #f9f9f9; border-left: 4px solid #111; font-style: italic; }
'''

nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
book.add_item(nav_css)

# 1. Page de titre
p_title = epub.EpubHtml(title="Titre", file_name="title.xhtml", lang="fr")
p_title.content = '''
<div class="title-page">
    <h1>AKHANO</h1>
    <h2>Tome 1 : Le Tisseur du Destin</h2>
    <br/><br/>
    <p class="author-name">FABIO LAROUS<br/><small>(Le Tisseur)</small></p>
</div>
'''
p_title.add_item(nav_css)

# 2. Copyright
p_copyright = epub.EpubHtml(title="Copyright", file_name="copyright.xhtml", lang="fr")
p_copyright.content = '''
<div class="copyright-page">
    <p class="no-indent"><strong>AKHANO — Tome 1 : Le Tisseur du Destin</strong></p>
    <p class="no-indent">© 2026 FABIO LAROUS (Le Tisseur). Tous droits réservés.</p>
    <p class="no-indent">Aucune partie de ce livre ne peut être reproduite ou transmise sans l'autorisation écrite de l'auteur.</p>
    <p class="no-indent">Édition Ouroboros Publisher OS</p>
</div>
'''
p_copyright.add_item(nav_css)

# 3. Dédicace
p_dedication = epub.EpubHtml(title="Dédicace", file_name="dedication.xhtml", lang="fr")
p_dedication.content = '''
<div class="dedication">
    <p class="no-indent"><em>À toutes les âmes qui tissent la lumière à travers les ombres du destin.</em></p>
</div>
'''
p_dedication.add_item(nav_css)

# 4. Remerciements
p_thanks = epub.EpubHtml(title="Remerciements", file_name="remerciements.xhtml", lang="fr")
p_thanks.content = '''
<h1>Remerciements</h1>
<p>Mes remerciements les plus profonds s'adressent à mes lecteurs passionnés, à mes proches et à tous ceux qui soutiennent l'univers de la saga AKHANO. Ce livre existe grâce à votre énergie et à votre foi inébranlable dans la puissance du récit.</p>
'''
p_thanks.add_item(nav_css)

# 5. Prologue / Chapitres
formatted_paragraphs = "".join([f"<p>{p.strip()}</p>" for p in generated_text.split("\n") if p.strip()])
p_content = epub.EpubHtml(title="Récit Principal", file_name="content.xhtml", lang="fr")
p_content.content = f"<h1>AKHANO — Récit Principal</h1>{formatted_paragraphs}"
p_content.add_item(nav_css)

# 6. Quatrième de couverture
p_back = epub.EpubHtml(title="Quatrième de couverture", file_name="back_cover.xhtml", lang="fr")
p_back.content = '''
<h1>Quatrième de Couverture</h1>
<div class="back-cover">
    <p class="no-indent">Quand les fils d'or bioluminescents s'éveillent sous la chair et que les scarifications cyan révèlent la mémoire des anciens, le destin bascule.</p>
    <p class="no-indent">Plongez dans l'univers mystique et envoûtant d'AKHANO, un chef-d'œuvre Afro-Fantasy sculpté par la plume vibrante de FABIO LAROUS (Le Tisseur).</p>
</div>
'''
p_back.add_item(nav_css)

# 7. À propos de l'auteur
p_author = epub.EpubHtml(title="À propos de l'auteur", file_name="author.xhtml", lang="fr")
p_author.content = '''
<h1>À Propos de l'Auteur</h1>
<p class="no-indent"><strong>FABIO LAROUS (Le Tisseur)</strong> est un auteur indépendant et créateur d'univers immersifs à la croisée de la dark fantasy, du folklore afro-caraïbéen et des récits initiatiques majeurs. À travers la saga AKHANO et le système Ouroboros OS, il façonne des œuvres littéraires conçues avec la rigueur d'un best-seller international.</p>
'''
p_author.add_item(nav_css)

# Assemblage des parties
sections = [p_title, p_copyright, p_dedication, p_thanks, p_content, p_back, p_author]
for s in sections:
    book.add_item(s)

book.toc = tuple(sections)
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
book.spine = ['nav'] + sections

# Écriture du fichier EPUB final
epub.write_epub("Akhano_Tome1_BestSeller.epub", book, {})

# Génération du Kit Marketing complet
with open("KIT_MARKETING.md", "w", encoding="utf-8") as f:
    f.write("# Kit Marketing Best-Seller — AKHANO Tome 1\n\n")
    f.write("**Auteur :** FABIO LAROUS (Le Tisseur)\n\n")
    f.write("## 1. Accroches TikTok / Reels (Hooks Viral)\n")
    f.write("- *Hook 1 :* 'Si tes scarifications commençaient à luire en bleu sous la nuit, quel fil du destin tisserais-tu ?'\n")
    f.write("- *Hook 2 :* 'L'Afro-Fantasy n'a jamais été aussi sombre et envoûtante... Découvre AKHANO.'\n\n")
    f.write("## 2. Pitch Réseaux & Newsletter\n")
    f.write("Découvrez le premier tome captivant d'AKHANO par FABIO LAROUS (Le Tisseur). Une plongée magistrale au cœur d'un univers où la magie se tisse dans la chair et le sang.\n")

print(" Génération terminée avec succès ! EPUB et Kit Marketing créés.")
