"""
ORGANIZADOR DE PASTAS
Organiza automaticamente uma pasta por tipo de arquivo.

USO:
  python organizador.py                        → organiza Downloads
  python organizador.py --pasta /caminho       → organiza outra pasta
  python organizador.py --simular              → só mostra, não move

INSTALAR:
  Nada — usa só bibliotecas padrão do Python.
"""

import shutil
import argparse
from pathlib import Path
from collections import defaultdict


CATEGORIAS = {
    "Imagens":       [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic"],
    "Vídeos":        [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".webm"],
    "Áudio":         [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Documentos":    [".pdf", ".doc", ".docx", ".txt", ".odt", ".md"],
    "Planilhas":     [".xls", ".xlsx", ".csv", ".ods"],
    "Apresentações": [".ppt", ".pptx", ".key"],
    "Código":        [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".cs", ".json", ".sql"],
    "Compactados":   [".zip", ".rar", ".tar", ".gz", ".7z"],
}

# Lookup reverso: ".jpg" → "Imagens", ".py" → "Código" etc.
MAPA = {ext: cat for cat, exts in CATEGORIAS.items() for ext in exts}


def organizar(pasta, simular=False):
    pasta = Path(pasta)

    if not pasta.exists():
        print(f"  ❌ Pasta não encontrada: {pasta}")
        return

    print(f"\n  {'[SIMULAÇÃO] ' if simular else ''}Organizando: {pasta}\n")

    movidos = defaultdict(list)

    for arquivo in sorted(pasta.iterdir()):
        # Ignora subpastas e arquivos ocultos
        if arquivo.is_dir() or arquivo.name.startswith("."):
            continue

        categoria = MAPA.get(arquivo.suffix.lower(), "Outros")
        destino   = pasta / categoria / arquivo.name

        # Se já existe um arquivo com esse nome, adiciona número ao final
        contador = 2
        while destino.exists():
            destino = pasta / categoria / f"{arquivo.stem}_{contador}{arquivo.suffix}"
            contador += 1

        print(f"  {'→' if simular else '✅'}  {arquivo.name:<40} → {categoria}/")

        if not simular:
            (pasta / categoria).mkdir(exist_ok=True)
            shutil.move(str(arquivo), str(destino))

        movidos[categoria].append(arquivo.name)

    # Resumo
    total = sum(len(v) for v in movidos.values())
    print(f"\n  {'─'*48}")
    for cat, arquivos in sorted(movidos.items()):
        print(f"  📁 {cat}: {len(arquivos)} arquivo(s)")
    print(f"  Total: {total} arquivo(s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organiza uma pasta por tipo de arquivo.")
    parser.add_argument("--pasta",   default=None, help="Pasta a organizar (padrão: Downloads)")
    parser.add_argument("--simular", action="store_true", help="Mostra o que faria sem mover nada")
    args = parser.parse_args()

    pasta = args.pasta or str(Path.home() / "Downloads")
    organizar(pasta, simular=args.simular)
