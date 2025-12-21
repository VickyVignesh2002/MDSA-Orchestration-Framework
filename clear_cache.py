"""Clear Python cache files"""
import pathlib
import shutil

# Remove all __pycache__ directories
for p in pathlib.Path('.').rglob('__pycache__'):
    if p.is_dir():
        shutil.rmtree(p)
        print(f"Removed: {p}")

# Remove all .pyc and .pyo files
for p in pathlib.Path('.').rglob('*.py[co]'):
    if p.is_file():
        p.unlink()
        print(f"Removed: {p}")

print("\n✓ Cache cleared successfully!")
