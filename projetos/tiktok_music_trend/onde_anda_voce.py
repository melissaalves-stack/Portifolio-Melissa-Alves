import time
import sys
import os

# ─── CORES ANSI ──────────────────────────────────────────────────────────────
AMARELO = "\033[93m"
CIANO   = "\033[96m"
VERDE   = "\033[92m"
BRANCO  = "\033[97m"
RESET   = "\033[0m"

# ─── DIGITAÇÃO LETRA POR LETRA ───────────────────────────────────────────────
def digitar(texto, velocidade=0.055, cor=BRANCO):
    print(cor, end="")
    for letra in texto:
        print(letra, end="")
        sys.stdout.flush()
        time.sleep(velocidade)
    print(RESET)

# ─── MOTOR DE SINCRONIZAÇÃO ───────────────────────────────────────────────────
def rodar_sincronizado(eventos):
    inicio = time.time()
    for (momento, texto, velocidade, cor) in eventos:
        agora  = time.time()
        espera = momento - (agora - inicio)
        if espera > 0:
            time.sleep(espera)
        if texto is None:
            print()
        else:
            digitar(texto, velocidade=velocidade, cor=cor)

# ─── ROTEIRO ──────────────────────────────────────────────────────────────────
eventos = [

    # ── ESTROFE 1 ─────────────────────────────────────────────────────────────
    (17.0,  "E por falar em saudade",            0.060, CIANO  ),
    (21.0,  "onde anda você?",                   0.090, AMARELO),
    (23.0,  "Onde andam os seus olhos",          0.060, CIANO  ),
    (25.0,  "que a gente não vê?",               0.080, AMARELO),
    (27.0,  "Onde anda esse corpo",              0.065, VERDE  ),
    (30.0,  "que me deixou morto",               0.065, VERDE  ),
    (32.0,  "de tanto prazer?",                  0.090, AMARELO),

    (32.0,  None, 0, BRANCO),

    # ── ESTROFE 2 ─────────────────────────────────────────────────────────────
    (35.0,  "E por falar em beleza",             0.060, CIANO  ),
    (38.0,  "onde anda a canção",                0.075, CIANO  ),
    (40.0,  "que se ouvia na noite",             0.060, VERDE  ),
    (43.0,  "dos bares de então?",               0.080, VERDE  ),
    (45.0,  "Onde a gente ficava",               0.065, CIANO  ),
    (47.0,  "onde a gente se amava",             0.065, CIANO  ),
    (49.0,  "em total solidão...",               0.100, AMARELO),

    (49.0,  None, 0, BRANCO),

    # ── PONTE ─────────────────────────────────────────────────────────────────
    (54.0,  "Hoje eu saio na noite vazia",       0.050, VERDE  ),
    (58.0,  "numa boemia sem razão de ser",      0.050, VERDE  ),
    (60.0,  "Na rotina dos bares",               0.065, CIANO  ),
    (62.0,  "que apesar dos pesares",            0.065, CIANO  ),
    (66.0,  "me trazem você...",                 0.095, AMARELO),

    (66.0,  None, 0, BRANCO),

    # ── REFRÃO ────────────────────────────────────────────────────────────────
    (70.0,  "E por falar em paixão",             0.065, CIANO  ),
    (73.0,  "em razão de viver",                 0.075, CIANO  ),
    (75.0,  "você bem que podia me aparecer",    0.045, VERDE  ),
    (77.0,  "nesses mesmos lugares",             0.065, VERDE  ),
    (82.0,  "na noite, nos bares",               0.075, CIANO  ),
    (85,  "onde anda você?",                   0.110, AMARELO),

]

# ─── EXECUTA ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")

    print(AMARELO + "\n  ♪  Onde Anda Você  ♪")
    print("     Toquinho & Vinícius de Moraes\n" + RESET)
    print(VERDE + "  Deixa o vídeo pausado em 0:00...")
    print(CIANO + "  Aperte ENTER e dê play ao mesmo tempo.\n" + RESET)
    input()

    os.system("cls" if os.name == "nt" else "clear")
    print()

    rodar_sincronizado(eventos)

    print()
    print(AMARELO + "  ♪  fim  ♪\n" + RESET)