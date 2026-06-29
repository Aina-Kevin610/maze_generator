import os

# Créer le dossier pour tes textures
os.makedirs("assets", exist_ok=True)

# Masques de bits du sujet
N, E, S, W = 1, 2, 4, 8

# Dimensions des textures (en pixels)
SIZE = 32

for cell in range(16):
    lines = []
    for y in range(SIZE):
        row = ""
        for x in range(SIZE):
            # Détection des bordures pour tracer les murs selon les bits activés
            is_wall = (
                (y < 2 and (cell & N)) or          # Mur Nord (2px de large)
                (x >= SIZE - 2 and (cell & E)) or  # Mur Est
                (y >= SIZE - 2 and (cell & S)) or  # Mur Sud
                (x < 2 and (cell & W))             # Mur Ouest
            )
            row += "X" if is_wall else " "
        lines.append(f'"{row}"')

    # Génération de l'en-tête XPM textuelle classique
    xpm_content = [
        "/* XPM */",
        f"static char *tile_{cell}[] = {{",
        f'"{SIZE} {SIZE} 2 1",',
        '"  c #0F0F0F",',  # Couleur du sol (Gris très sombre)
        '"X c #00FF00",',  # Couleur des murs (Vert MLX fluo)
        ",\n".join(lines),
        "};"
    ]

    # Écriture directe du fichier .xpm en mode texte brut
    with open(f"assets/{cell}.xpm", "w") as f:
        f.write("\n".join(xpm_content))

print("Succès : Les 16 fichiers .xpm sont prêts dans le dossier './assets/' !")