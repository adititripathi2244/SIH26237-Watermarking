import torch
import torch.nn as nn
from torchvision import models


class WatermarkCNN(nn.Module):
    """
    CNN-based detector for identifying whether an image/document
    contains our forensic watermark.

    Output:
        0 -> No watermark
        1 -> Watermark detected
    """

    def __init__(self, pretrained=False):
        super().__init__()

        # ResNet18 gives us a strong CNN backbone.
        self.model = models.resnet18(weights=None)

        # Our input images are RGB.
        # ResNet18 normally expects 3-channel RGB images.

        # Replace the original 1000-class ImageNet classifier
        # with a binary classifier.
        input_features = self.model.fc.in_features

        self.model.fc = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(input_features, 1)
        )

    def forward(self, x):
        """
        Forward pass.

        Returns one raw value (logit) for each image.
        During training we will use BCEWithLogitsLoss.
        """
        return self.model(x)


def create_model():
    """
    Create and return a WatermarkCNN model.
    """
    model = WatermarkCNN(pretrained=False)
    return model


if __name__ == "__main__":
    print("Testing WatermarkCNN...")

    # Create model
    model = create_model()

    # Put model in evaluation mode
    model.eval()

    # Create a fake batch:
    # 2 RGB images, 224x224 pixels
    test_input = torch.randn(2, 3, 224, 224)

    # Run the images through the CNN
    with torch.no_grad():
        output = model(test_input)

    print("Input shape :", test_input.shape)
    print("Output shape:", output.shape)
    print("Model test  : PASS")
