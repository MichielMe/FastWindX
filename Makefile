build:
	python -m build --sdist --wheel ./
	echo "Build complete."

remove-package:
	rm -r build/ dist/ *.egg-info/ *.dist-info/ *.cache
	echo "Package removed."

clean-up:
	# Remove cache files
	find . -type f -name '*.cache' -exec rm -f {} +

	# Remove .dist-info directories
	find . -type d -name '*.dist-info' -exec rm -rf {} +

	# Remove .egg-info directories
	find . -type d -name '*.egg-info' -exec rm -rf {} +

	echo "Cleanup complete."

