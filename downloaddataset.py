import os
from huggingface_hub import snapshot_download
from pathlib import Path

def download_dataset():
    # 1. Define paths
    BASE_DIR = Path(__file__).resolve().parent
    target_dir = BASE_DIR / "datasets" / "cat-dog-yolo"
    repo_id = "sankalpa1998/cat-dog-yolo-dataset"

    print(f"Target directory: {target_dir}")
    
    # 2. Check if dataset already exists and is not empty
    if target_dir.exists() and any(target_dir.iterdir()):
        print(f"Dataset already exists at '{target_dir}'. Skipping download.")
        print(f"Folder contents: {os.listdir(target_dir)}")
        return

    # 3. Start Download if it doesn't exist
    try:
        print(f"Downloading dataset '{repo_id}' from Hugging Face...")
        
        snapshot_download(
            repo_id=repo_id,
            repo_type="dataset",
            local_dir=str(target_dir),
            local_dir_use_symlinks=False  # Ensures actual files are downloaded
        )
        
        print("\nSuccess! Dataset downloaded and organized.")
        print(f"Location: {target_dir}")
        
        # Verify Download
        if os.path.exists(target_dir):
            contents = os.listdir(target_dir)
            print(f"Folder contents: {contents}")

    except Exception as e:
        print(f"\nAn error occurred during download: {e}")

if __name__ == "__main__":
    download_dataset()