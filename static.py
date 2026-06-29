import os
import sys
from typing import Any, Tuple, List, Set

N = 1 << 0
E = 1 << 1
S = 1 << 2
W = 1 << 3

WALL_COLORS = [
    0x00FF00FF,
    0xFFFFFFFF,
    0x00FFFFFF,
    0xFFFF00FF,
    0xFF00FFFF,
]


class DrawingMazeMLX:
    """
    Gère le rendu graphique statique à l'aide d'assets XPM et les interactions 
    d'un labyrinthe parsé depuis un fichier. (Aucune animation)
    """
    def __init__(self, filename: str = "maze.txt") -> None:
        self.filename = filename
        
        # Charger et parser les données initiales du fichier fini
        self.grid, self.entry, self.exit_, self.path = self.parse(filename)
        self.path_set: Set[Tuple[int, int]] = set(self.path)
        
        self.height = len(self.grid)
        self.width = len(self.grid[0])

        # Taille fixe basée sur la dimension de tes assets générés (32x32 pixels)
        self.cell_size_w = 32
        self.cell_size_h = 32
        self.w_win = self.width * self.cell_size_w
        self.h_win = self.height * self.cell_size_h

        # Initialisation MiniLibX
        from mlx import Mlx
        self.m = Mlx()
        self.mlx = self.m.mlx_init()
        if not self.mlx:
            sys.exit(1)

        self.win = self.m.mlx_new_window(self.mlx, self.w_win, self.h_win, "A-MAZE-ING ! (MLX Statique)")
        if not self.win:
            sys.exit(1)

        # Image buffer principale
        self.img = self.m.mlx_new_image(self.mlx, self.w_win, self.h_win)
        if not self.img:
            sys.exit(1)

        (self.data, self.bpp, self.size_line, _) = self.m.mlx_get_data_addr(self.img)

        # Chargement UNIQUE des 16 assets (0.xpm à 15.xpm) au démarrage
        self.tiles: dict[int, Any] = {}
        for i in range(16):
            asset_path = f"assets/{i}.xpm"
            if os.path.exists(asset_path):
                img_ptr, _, _ = self.m.mlx_xpm_file_to_image(self.mlx, asset_path)
                self.tiles[i] = img_ptr
            else:
                print(f"[!] Attention : L'asset {asset_path} est manquant.")
                self.tiles[i] = None

        # États pour les interactions clavier
        self.show_path = True
        self.wall_color_idx = 0
        self.wall_color = WALL_COLORS[self.wall_color_idx]
        self.bg_color = 0x111111FF  # Fond sombre gris/noir

        # Couleurs des overlays (Départ, Arrivée, Chemin)
        self.entry_color = 0x00FF0088  # Vert translucide
        self.exit_color = 0xFF000088   # Rouge translucide
        self.path_color = 0x00FFFF88   # Cyan translucide

        # Enregistrement du Hook clavier standard (Pas de loop_hook d'animation)
        self.m.mlx_hook(self.win, 2, 1, self.handle_keys, [self])
        
        # Premier et unique dessin immédiat
        self.draw_maze()

    def parse(self, filename: str) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int], List[Tuple[int, int]]]:
        with open(filename, "r") as f:
            lines = f.read().splitlines()

        grid_lines: List[str] = []
        rest: List[str] = []
        sep = None
        
        for line in lines:
            if line == "" and sep is None:
                sep = 0
            elif sep is None:
                grid_lines.append(line)
            elif line:
                rest.append(line)

        grid = [[int(c, 16) for c in row] for row in grid_lines]
        ex, ey = map(int, rest[0].split(","))
        xx, xy = map(int, rest[1].split(","))

        path: List[Tuple[int, int]] = []
        if len(rest) >= 3:
            x, y = ex, ey
            for ch in rest[2]:
                path.append((x, y))
                if ch == "N": y -= 1
                elif ch == "S": y += 1
                elif ch == "E": x += 1
                elif ch == "W": x -= 1
            path.append((x, y))

        return grid, (ex, ey), (xx, xy), path

    def my_put_pixel(self, x: int, y: int, color: int) -> None:
        """ Place un pixel dans le buffer d'image principal """
        if x < 0 or y < 0 or x >= self.w_win or y >= self.h_win:
            return

        offset = (y * self.size_line) + (x * (self.bpp // 8))
        
        blue = (color >> 24) & 0xFF
        green = (color >> 16) & 0xFF
        red = (color >> 8) & 0xFF

        self.data[offset] = blue
        self.data[offset + 1] = green
        self.data[offset + 2] = red
        self.data[offset + 3] = 0xFF

    def clear_image(self) -> None:
        """ Nettoie le fond du buffer de l'image """
        for y in range(self.h_win):
            for x in range(self.w_win):
                self.my_put_pixel(x, y, self.bg_color)

    def fill_cell(self, cx: int, cy: int, color: int) -> None:
        """ Superpose une couleur unie sur le sol de la cellule """
        px = cx * self.cell_size_w
        py = cy * self.cell_size_h
        # On remplit l'intérieur en laissant une marge pour les murs de 2px
        for y in range(py + 2, py + self.cell_size_h - 2):
            for x in range(px + 2, px + self.cell_size_w - 2):
                self.my_put_pixel(x, y, color)

    def draw_maze(self) -> None:
        """ Rendu instantané du labyrinthe entier """
        self.clear_image()
        
        # 1. On applique le fond noir/gris de base sur la fenêtre
        self.m.mlx_put_image_to_window(self.mlx, self.win, self.img, 0, 0)

        # 2. On dessine chaque bloc d'asset de mur (.xpm) de façon statique
        for y in range(self.height):
            for x in range(self.width):
                cell_value = self.grid[y][x]
                px = x * self.cell_size_w
                py = y * self.cell_size_h

                tile_ptr = self.tiles.get(cell_value)
                if tile_ptr:
                    self.m.mlx_put_image_to_window(self.mlx, self.win, tile_ptr, px, py)

        # 3. Superposition immédiate des couleurs spéciales (Entrée, Sortie, Chemin)
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == self.entry:
                    self.fill_cell(x, y, self.entry_color)
                elif (x, y) == self.exit_:
                    self.fill_cell(x, y, self.exit_color)
                elif self.show_path and (x, y) in self.path_set:
                    self.fill_cell(x, y, self.path_color)

        # 4. On pousse le résultat final stabilisé à l'écran
        self.m.mlx_put_image_to_window(self.mlx, self.win, self.img, 0, 0)

    def handle_keys(self, keycode: int, params: list[Any]) -> int:
        _ = params

        # Touche ESPACE -> Change l'état de couleur (optionnel avec les assets)
        if keycode == 32:
            self.wall_color_idx = (self.wall_color_idx + 1) % len(WALL_COLORS)
            self.wall_color = WALL_COLORS[self.wall_color_idx]
            self.draw_maze()

        # Touche 'P' -> Afficher / Masquer instantanément le chemin de résolution
        elif keycode == 112:
            self.show_path = not self.show_path
            self.draw_maze()

        # Touche ENTRÉE -> Re-parse le fichier mis à jour (Génération synchrone terminée)
        elif keycode in (13, 65293):
            try:
                self.grid, self.entry, self.exit_, self.path = self.parse(self.filename)
                self.path_set = set(self.path)
                self.draw_maze()
            except FileNotFoundError:
                print("Erreur : Fichier maze.txt introuvable lors de la lecture.")

        # Touche ÉCHAP -> Quitte proprement l'application
        elif keycode in (27, 65307):
            self.m.mlx_destroy_window(self.mlx, self.win)
            self.m.mlx_loop_exit(self.mlx)
            sys.exit(0)

        return 0

    def run(self) -> None:
        """ Lance la boucle d'événements MLX standard """
        self.m.mlx_loop(self.mlx)


if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else "maze.txt"
    app = DrawingMazeMLX(target_file)
    app.run()