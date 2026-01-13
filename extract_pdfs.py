import pypdf
import os

files = [
    "IMPACT DE l' IA POUR TERAVOO -2.pdf",
    "Ma Vision Plateforme B2B Commerce Agricole-5.pdf",
    "PLAN DE DÉVELOPPEMENT DU MVP Final – TeraVoo.pdf",
    "Présentation Officielle du Projet – TeraVoo-2.pdf",
    "Réponses TeraVoo aux Problématiques Terrain-1.pdf",
    "TeraVoo – AI Product & Technical Vision.pdf"
]

output_file = "extracted_pdfs.txt"

print(f"Extracting text from {len(files)} files...")

with open(output_file, "w", encoding="utf-8") as out:
    for f in files:
        print(f"Processing {f}...")
        out.write(f"\n\n========================================\nFILE: {f}\n========================================\n\n")
        try:
            if not os.path.exists(f):
                out.write(f"ERROR: File not found: {f}\n")
                continue
                
            reader = pypdf.PdfReader(f)
            number_of_pages = len(reader.pages)
            out.write(f"Pages: {number_of_pages}\n\n")
            
            for i, page in enumerate(reader.pages):
                out.write(f"--- Page {i+1} ---\n")
                text = page.extract_text()
                if text:
                    out.write(text)
                else:
                    out.write("[No text extracted]")
                out.write("\n\n")
        except Exception as e:
            out.write(f"ERROR reading {f}: {e}\n")
            print(f"Error on {f}: {e}")
            
print("Done.")
