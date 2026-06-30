PYTHON     = python3
VENV       = .venv
ACTIVATE   = $(VENV)/bin/activate
PIP        = $(VENV)/bin/pip
EXEC       = $(VENV)/bin/python
MAIN       = a_maze_ing.py
SRC        = a_maze_ing.py \
             render/ascii.py \
             render/window_render.py \
             render/__init__.py \
             mazegen/parsing.py \
             mazegen/mazegen.py \
             mazegen/__init__.py \
             mazegen/pattern.py \
             mazegen/algo/prim.py \
             mazegen/algo/hunt_and_kill.py \
             mazegen/algo/algo_utils.py \
             mazegen/algo/__init__.py
FILENAME   = "config.txt"
PACKAGE    = package/mlx-2.2-py3-none-any.whl

run: install
	$(EXEC) $(MAIN) $(FILENAME)

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy
	$(PIP) install $(PACKAGE)

debug: install
	$(EXEC) -m pdb $(MAIN)

lint: install
	$(EXEC) -m flake8 $(SRC)
	$(EXEC) -m mypy --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs $(SRC)

build: install
	$(PIP) install build
	$(EXEC) -m build --wheel

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

fclean: clean
	rm -rf $(VENV)
	rm -rf dist
	rm -rf build
	rm -f maze.txt
	rm -rf mazegen.egg-info

re: fclean install

.PHONY: install run debug lint lint-strict build clean fclean re
