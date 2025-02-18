# dataloader/dataloader.py

import os
import sys
import random
import glob
from collections import namedtuple

from .preprocessors import default_preprocess, normalize, augment
from .utils import download_file, timer

# NamedTuple to store dataset samples (features and labels)
DataSample = namedtuple('DataSample', ['features', 'label'])

class DataLoader:
    """
    A flexible DataLoader that:
      - Opens binary files (e.g., MNIST .idx, CIFAR-10 batches) in 'rb' mode.
      - Opens text files (e.g., CSV or small text datasets) in 'r' mode.
      - Applies a preprocessing function (customizable).
      - Ensures at least batch_size samples are available.
      - Implements an iterator protocol for batch-wise data retrieval.
    """

    # URLs for datasets that can be downloaded automatically if not found locally.
    DATASET_URLS = {
        'CIFAR-10': 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz',
        'CIFAR-100': 'https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz',
        'sample_text': 'https://raw.githubusercontent.com/selva86/datasets/master/newsgroups.json',
        'unstructured': 'https://example.com/unstructured_data.zip'
        # MNIST is expected to be stored locally in `.idx` format.
    }

    @timer  # Logs the execution time of the function
    def __init__(self, dataset_name='MNIST', batch_size=32, shuffle=True, **kwargs):
        """
        Initializes the DataLoader and loads the dataset.

        :param dataset_name: Name of the dataset (e.g., 'MNIST', 'CIFAR-10', 'CSV filename').
        :param batch_size: Number of samples per batch.
        :param shuffle: Whether to shuffle data before each iteration.
        :param kwargs: Additional options (e.g., preprocess_func, normalize, augment).
        """
        self.dataset_name = dataset_name
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.kwargs = kwargs

        self.data = []  # Stores the dataset samples
        self.index = 0  # Keeps track of batch index during iteration

        self.load_data()  # Load data when the object is initialized

    @timer
    def load_data(self):
        """
        Loads the dataset from a local directory. If the dataset is recognized but not found locally,
        it will attempt to download it.
        """
        dataset_path = os.path.join("datasets", self.dataset_name)

        # If dataset is known (e.g., CIFAR-10) but not found, attempt to download it
        if self.dataset_name in self.DATASET_URLS and not os.path.isdir(dataset_path):
            os.makedirs(dataset_path, exist_ok=True)
            self.download_dataset(dataset_path)

        # Read local data from dataset folder
        raw_samples = list(self.read_data(dataset_path))
        self.data = self.preprocess_data(raw_samples)

        # Ensure at least batch_size samples are available (by duplicating if needed)
        if len(self.data) < self.batch_size and len(self.data) > 0:
            multiplier = (self.batch_size // len(self.data)) + 1
            self.data = (self.data * multiplier)[:self.batch_size]

        if not self.data:
            print(f"Warning: No data loaded for '{self.dataset_name}'. Batches will be empty.")

    @timer
    def download_dataset(self, dataset_path):
        """
        Downloads the dataset if a URL is provided in DATASET_URLS.

        :param dataset_path: The path where the dataset should be stored.
        """
        url = self.DATASET_URLS.get(self.dataset_name)
        if url is None:
            print(f"No download URL for dataset {self.dataset_name}.")
            return

        print(f"Downloading {self.dataset_name} from {url} ...")
        filename = os.path.join(dataset_path, os.path.basename(url))
        try:
            download_file(url, filename)
            print(f"Downloaded {filename}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    def read_data(self, dataset_path):
        """
        Reads and yields dataset samples from the specified path.
        Identifies binary files vs. text files and reads them accordingly.

        :param dataset_path: The path to the dataset directory or file.
        :return: Generator yielding DataSample instances.
        """
        if os.path.isdir(dataset_path):
            # Read all files in the folder
            file_paths = glob.glob(os.path.join(dataset_path, '*'))
            for fp in file_paths:
                yield from self._read_file(fp)
        elif os.path.isfile(dataset_path):
            yield from self._read_file(dataset_path)
        else:
            print(f"Could not find dataset at {dataset_path}.")

    def _read_file(self, fp):
        """
        Reads a file and determines whether to open it as binary or text.

        :param fp: File path.
        :return: Yields DataSample objects.
        """
        # Identify binary files by their extensions or known filename patterns
        is_binary = False
        if fp.endswith('.idx3-ubyte') or fp.endswith('.idx1-ubyte'):
            is_binary = True
        elif any(token in fp for token in ['data_batch', 'test_batch', 'batches.meta']):
            is_binary = True
        elif fp.endswith('.csv'):
            is_binary = False  # CSV files are text

        mode = 'rb' if is_binary else 'r'  # Binary vs text mode
        encoding = None if is_binary else 'utf-8'  # Only text files need encoding

        try:
            with open(fp, mode, encoding=encoding) as f:
                content = f.read()
                yield DataSample(features=content, label=None)
        except Exception as e:
            print(f"Error reading file {fp}: {e}")

    def preprocess_data(self, samples):
        """
        Applies a preprocessing function to each sample. If the function raises a TypeError
        when passed a dict, it falls back to calling it with sample['features'].

        :param samples: List of DataSample instances.
        :return: Processed dataset.
        """
        preprocess_func = self.kwargs.get('preprocess_func', default_preprocess)
        do_normalize = self.kwargs.get('normalize', False)
        do_augment = self.kwargs.get('augment', False)

        processed = []
        for sample in samples:
            sample_dict = {'features': sample.features, 'label': sample.label}
            try:
                result = preprocess_func(sample_dict)
            except TypeError:
                # Fallback: apply preprocess only to features
                processed_feature = preprocess_func(sample_dict.get('features'))
                result = {'features': processed_feature, 'label': sample_dict.get('label')}

            # Optionally normalize
            if do_normalize:
                try:
                    result = normalize(result)
                except TypeError:
                    processed_feature = normalize(result.get('features'))
                    result = {'features': processed_feature, 'label': result.get('label')}

            # Optionally augment
            if do_augment:
                try:
                    result = augment(result)
                except TypeError:
                    processed_feature = augment(result.get('features'))
                    result = {'features': processed_feature, 'label': result.get('label')}

            processed.append(DataSample(features=result.get('features'), label=result.get('label')))
        return processed

    def __iter__(self):
        """
        Resets the index and shuffles data if required before iteration.

        :return: Iterator object.
        """
        self.index = 0
        if self.shuffle:
            random.shuffle(self.data)
        return self

    def __next__(self):
        """
        Returns the next batch of data.

        :return: A batch of DataSample instances.
        :raises StopIteration: When no more data is left.
        """
        if self.index < len(self.data):
            batch = self.data[self.index : self.index + self.batch_size]
            self.index += self.batch_size
            return batch
        else:
            raise StopIteration
