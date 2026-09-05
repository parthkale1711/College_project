import os
import shutil

# Files to delete
DELETE_FILES = [
    'features.py',
    'predict.py',
    'fake_news_model.pkl',
    'fake_news_rf.pkl',
    'tfidf_vectorizer.pkl',
    'train_model22.py',
    'quick_metadata_fix.py',
    'cleanup_files.py',
    'IndFakeNewsDetector.ipynb',
    'Real_News1.txt',
    'Real_News2.txt',
    'Real_News3.txt',
    'Real_News4.txt',
    'index.html'
]

# Directories to delete
DELETE_DIRS = [
    '__pycache__',
    '.ipynb_checkpoints'
]

# Files to move to 'datasets' folder
MOVE_TO_DATASETS = [
    'IFND.csv',
    'fake_or_real_news.csv',
    'Whatsapp_fake_news_India.csv'
]

def cleanup():
    print("Starting cleanup...")

    # Create datasets folder
    if not os.path.exists('datasets'):
        os.makedirs('datasets')
        print("Created 'datasets' folder")

    # Delete files
    for file in DELETE_FILES:
        if os.path.exists(file):
            os.remove(file)
            print(f"Deleted: {file}")

    # Delete directories
    for dir in DELETE_DIRS:
        if os.path.exists(dir):
            shutil.rmtree(dir)
            print(f"Deleted directory: {dir}")

    # Move datasets
    for file in MOVE_TO_DATASETS:
        if os.path.exists(file):
            shutil.move(file, f'datasets/{file}')
            print(f"Moved to datasets/: {file}")

    # Rename app22.py to app.py
    if os.path.exists('app22.py') and not os.path.exists('app.py'):
        os.rename('app22.py', 'app.py')
        print("Renamed: app22.py → app.py")

    print("\nCleanup complete!")

if __name__ == '__main__':
    cleanup()
