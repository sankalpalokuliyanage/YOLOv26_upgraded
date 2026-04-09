from ultralytics import YOLO
import torch

def train_my_model():
    # 1. Check for GPU
    device = '0' if torch.cuda.is_available() else 'cpu'
    print(f"Training will run on: {device}")

    # 2. Load the model
    model = YOLO('yolo26n.pt')

    # 3. Start Training
    model.train(
        data='data.yaml', 
        epochs=50, 
        imgsz=640, 
        device=device,
        workers=20  # You can adjust this based on your CPU
    )

    print(model.val())

if __name__ == '__main__':
    # This block is CRITICAL on Windows to prevent the RuntimeError
    train_my_model()