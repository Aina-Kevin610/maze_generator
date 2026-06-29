MAIN = a_maze_ing.py
CONFIG = config.txt


run:
	python3 $(MAIN) $(CONFIG)

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

fclean: clean
	rm -f maze.txt

.PHONY: install run debug lint lint-strict build clean fclean re