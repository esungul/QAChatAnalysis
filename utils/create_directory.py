import os

# Define the base directory
base_dir = 'qa_analysis_tool'

# Create the base directory
os.makedirs(base_dir, exist_ok=True)

# Create subdirectories
os.makedirs(os.path.join(base_dir, 'utils'), exist_ok=True)
os.makedirs(os.path.join(base_dir, 'analyzers'), exist_ok=True)

# Create empty files
open(os.path.join(base_dir, 'app.py'), 'w').close()
open(os.path.join(base_dir, 'config.py'), 'w').close()
open(os.path.join(base_dir, 'requirements.txt'), 'w').close()
open(os.path.join(base_dir, 'README.md'), 'w').close()
open(os.path.join(base_dir, '.gitignore'), 'w').close()

open(os.path.join(base_dir, 'utils', '__init__.py'), 'w').close()
open(os.path.join(base_dir, 'utils', 'parsers.py'), 'w').close()
open(os.path.join(base_dir, 'utils', 'detectors.py'), 'w').close()

open(os.path.join(base_dir, 'analyzers', '__init__.py'), 'w').close()
open(os.path.join(base_dir, 'analyzers', 'prompt_builder.py'), 'w').close()
open(os.path.join(base_dir, 'analyzers', 'analyzer.py'), 'w').close()

print("Directory structure created successfully.")