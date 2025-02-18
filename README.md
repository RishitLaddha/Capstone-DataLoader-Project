# Session15-Capstone DataLoader Project

![GitHub Actions](https://github.com/RishitLaddha/session15-Capstone/actions/workflows/python-ci.yml/badge.svg)

Welcome to the Session15-Capstone DataLoader project! This project demonstrates a flexible, modular Python-based DataLoader that can load, preprocess, and manage various types of datasets including images, text, CSV files, and unstructured data. The project is designed with simplicity and extensibility in mind so that even non-technical users can appreciate its design, while technical users can dive deep into its functionality.

## Overview

At its core, the project provides a DataLoader class that abstracts away the complexity of reading different file formats. Whether your dataset is stored locally or needs to be downloaded, the DataLoader can handle it. The DataLoader automatically checks for the existence of datasets in a local folder and, if they are missing, it can download them from provided URLs. The project also includes support for basic preprocessing steps such as normalization and data augmentation. This means that raw data is transformed into a format that is easier for downstream tasks like training machine learning models.

## Project Structure

The project follows a clean, modular structure:

```
project_root/
├── dataloader/
│   ├── __init__.py
│   ├── dataloader.py
│   ├── preprocessors.py
│   └── utils.py
├── datasets/
│   └── (Your datasets will be stored here)
├── tests/
│   └── test_dataloader.py
├── main.py
└── requirements.txt
```

- **dataloader/**: Contains the main logic of the DataLoader. The `dataloader.py` file defines the DataLoader class, `preprocessors.py` includes functions for data cleaning and transformation, and `utils.py` provides helper functions like timing decorators and file download utilities.
- **datasets/**: This folder is where all datasets are stored. It supports multiple formats—images, text files, CSV files, etc.
- **tests/**: Contains unit tests that verify the functionality of the DataLoader and its related components.
- **main.py**: Acts as the entry point for running the DataLoader, parsing command-line arguments, and iterating over data batches.
- **requirements.txt**: Lists the external Python packages needed (such as `requests` for downloading files).

## Key Features

### 1. Flexible Data Loading

The DataLoader is built to work with various types of datasets:

- **Image Datasets**: For example, CIFAR-10 and CIFAR-100 are typically provided in archive formats. Although the current implementation reads the raw binary files, the project is structured so that you can later add extraction and parsing logic.
- **Text Datasets**: Small text datasets are supported by reading files in UTF-8 mode. This makes it simple to work with plain text data.
- **CSV Files**: The DataLoader can handle CSV files, reading the rows and treating each as a data sample. This is particularly useful for structured data.
- **Unstructured Data**: For folders containing files of various formats, the DataLoader scans all files and loads them as raw samples.

The approach used is to automatically check if the dataset exists locally. If not, and if a download URL is provided, it downloads the dataset into the proper folder. This makes it very convenient for users who may not want to manually handle file downloads.

### 2. Preprocessing and Normalization

Preprocessing is a crucial step in data science and machine learning. This project includes several preprocessing functions that help prepare data for further processing:

- **Default Preprocessing**: The `default_preprocess` function cleans up text by removing unnecessary whitespace. It acts as a baseline processor.
- **Normalization**: The `normalize` function is designed to scale numerical values into the [0, 1] range. This is important because many machine learning algorithms perform better when data is normalized. For example, if your data contains pixel values (ranging from 0 to 255), normalization scales these values down so that they are more consistent with other features.
- **Augmentation**: The `augment` function provides simple augmentation capabilities. For text, it can convert text to uppercase. For numerical data, it can add a small constant. For binary data, the function duplicates the bytes as a placeholder for more advanced operations. This function can be extended later with more complex augmentations like image flipping, rotation, or noise injection.

### 3. Modularity and Extensibility

The project is structured in a modular way:
- **Separation of Concerns**: The code is divided into modules, each responsible for a specific part of the functionality. This makes the code easier to maintain and extend.
- **Extensible Preprocessing**: By using keyword arguments (`**kwargs`) in the DataLoader, you can pass custom preprocessing functions. This means you can plug in your own logic for data cleaning and transformation without modifying the core code.
- **Utility Functions**: Common functionalities such as downloading files and timing function execution are abstracted into the `utils.py` module. This helps keep the core logic clean and focused.

### 4. Batch Processing and Iteration

The DataLoader implements Python’s iterator protocol. This means you can loop over your dataset in batches, making it efficient to process large datasets:
- **Iterator Protocol**: The DataLoader resets the batch index and shuffles the data if required, providing a new batch of samples with every iteration.
- **Batch Replication**: If the number of available samples is less than the specified batch size, the DataLoader replicates samples to ensure that every batch has the desired number of items. This feature ensures that downstream processing (like model training) always receives a batch of consistent size.

### 5. Command-Line Integration

The project includes a `main.py` script that allows you to run the DataLoader from the command line:
- **Command-Line Arguments**: Users can specify the dataset name, batch size, and optional flags for normalization and augmentation. This makes the project user-friendly and adaptable to different scenarios.
- **Example Usage**: For instance, running `python main.py CIFAR-10 64 --normalize --augment` will load the CIFAR-10 dataset, apply normalization and augmentation, and process data in batches of 64.

### 6. Testing

Robust testing is essential for any project. The tests in this project verify:
- DataLoader initialization and file downloading.
- Flexible method parameters by passing custom preprocessing functions.
- Proper normalization of numerical data.
- Usage of lambda functions, closures, decorators, and custom iterators.
- That the project is modular and that files can be imported correctly.
- Command-line arguments are parsed and handled without error.

These tests ensure that the DataLoader works as expected and is robust enough for a variety of use cases.

## Example Workflow

Imagine you are working on a machine learning project and you need to load a dataset of images and text. You place your dataset files into the appropriate folder inside the `datasets/` directory. Next, you run the DataLoader using the command line:
  
```bash
python main.py MNIST 32 --normalize --augment
```

This command tells the DataLoader to use the MNIST dataset, process data in batches of 32, and apply both normalization and augmentation. The DataLoader checks for the dataset, downloads it if necessary, applies the preprocessing functions, and then iterates over the data in batches. As each batch is processed, the DataLoader prints out sample information, giving you a quick preview of what has been loaded.

## Final Thoughts

This DataLoader project addresses common data loading challenges, from file downloading and preprocessing to batch processing and iteration. 

Whether you are a beginner or an experienced developer, this project offers a solid foundation for your data loading needs. We invite you to explore the code, run the tests, and integrate this DataLoader into your projects. Your contributions and improvements are welcome as you adapt the project to fit your specific requirements.

Thank you for checking out the Session15-Capstone DataLoader project. 

-----
