import os
import shutil

def cleanup():
    """Clean up Python cache files and directories"""
    patterns = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.DS_Store',
        '*.egg-info',
        '*.egg',
        '.pytest_cache',
        '.coverage',
        'htmlcov'
    ]

    total_removed = 0
    for root, dirs, files in os.walk('.'):
        for pattern in patterns:
            # For directories
            if pattern in dirs and not pattern.startswith('*.'):
                path = os.path.join(root, pattern)
                print(f"Removing directory: {path}")
                shutil.rmtree(path)
                total_removed += 1
                
            # For files
            if pattern.startswith('*.'):
                ext = pattern[2:]
                for file in files:
                    if file.endswith(ext) or file == '.DS_Store':
                        path = os.path.join(root, file)
                        print(f"Removing file: {path}")
                        os.remove(path)
                        total_removed += 1

    print(f"\nCleanup complete! Removed {total_removed} items.")

if __name__ == "__main__":
    cleanup()