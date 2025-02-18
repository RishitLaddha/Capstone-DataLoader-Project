# main.py

import sys
from dataloader import DataLoader

def main():
    """
    Main function to initialize and run the DataLoader.

    - Accepts command-line arguments to specify the dataset and batch size.
    - Supports optional flags for normalization and augmentation.
    - Iterates over the dataset in batches and prints sample information.

    Command-line usage:
        python main.py <dataset_name> <batch_size> [--normalize] [--augment]

    Example:
        python main.py CIFAR-10 64 --normalize --augment
    """

    # Parse command-line arguments
    dataset_name = sys.argv[1] if len(sys.argv) > 1 else 'MNIST'  # Default: MNIST
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 32  # Default batch size: 32

    # Check for optional flags in arguments
    normalize_flag = '--normalize' in sys.argv  # Enable normalization if flag is present
    augment_flag = '--augment' in sys.argv  # Enable augmentation if flag is present

    # Initialize DataLoader with optional preprocessing options
    data_loader = DataLoader(
        dataset_name=dataset_name,
        batch_size=batch_size,
        normalize=normalize_flag,
        augment=augment_flag
    )

    # Iterate over data in batches
    for batch_idx, batch in enumerate(data_loader):
        print(f"\nProcessing batch #{batch_idx + 1}, size {len(batch)}")
        for sample in batch:
            # Each sample is a namedtuple DataSample(features, label)
            print(f"Features: {sample.features[:50]}...")  # Print first 50 characters for preview
            print(f"Label: {sample.label}")
        print("-" * 40)  # Separator for batch output

if __name__ == '__main__':
    main()  # Run the main function if the script is executed directly
