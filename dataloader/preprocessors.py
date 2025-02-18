# dataloader/preprocessors.py

def default_preprocess(sample):
    """
    Default preprocessing function.

    If the input `sample` is a dictionary containing 'features' and 'label', this function:
      - Strips any leading/trailing whitespace from the 'features' value if it is a string.
      - Leaves the 'label' unchanged.
    Otherwise, it returns the sample unchanged.

    :param sample: The input sample to preprocess (expected to be a dict).
    :return: A dictionary with preprocessed 'features' and 'label', or the original sample if not a dict.
    """
    if not isinstance(sample, dict):
        return sample

    # Extract 'features' and 'label' from the sample
    features = sample.get('features')
    label = sample.get('label')

    # If the features are text, remove any extra whitespace
    if isinstance(features, str):
        features = features.strip()

    return {'features': features, 'label': label}


def normalize(sample):
    """
    Normalizes numeric data to the range [0, 1].

    This function supports:
      - A single numeric value (int or float): Divides it by 255.0.
      - A list of numeric values: Applies the same division element-wise.
      - Binary data (bytes): Converts each byte into a float in [0, 1] by dividing by 255.0.
      - A dictionary: Applies normalization to the value under the 'features' key, leaving the 'label' unchanged.

    :param sample: The input sample, which can be a number, a list of numbers, bytes, or a dict containing 'features'.
    :return: The normalized value or a dictionary with normalized 'features'.
    """
    # Normalize a single numeric value
    if isinstance(sample, (int, float)):
        return sample / 255.0

    # If sample is a dictionary, process the 'features' value accordingly
    if isinstance(sample, dict):
        features = sample.get('features')
        label = sample.get('label')

        # Normalize a single numeric feature
        if isinstance(features, (int, float)):
            features = features / 255.0
        # Normalize a list of numeric features element-wise
        elif isinstance(features, list) and all(isinstance(x, (int, float)) for x in features):
            features = [x / 255.0 for x in features]
        # Normalize binary data: convert each byte to a float in the range [0, 1]
        elif isinstance(features, bytes):
            features = [b / 255.0 for b in features]
        return {'features': features, 'label': label}

    # If sample is of an unhandled type, return it unchanged
    return sample


def augment(sample):
    """
    Applies simple augmentation to the input sample.

    The augmentation rules are:
      - For numeric data (int or float): Adds 1 to the value.
      - For a list of numeric data: Adds 1 to each element.
      - For text data (str): Converts the text to uppercase.
      - For binary data (bytes): Duplicates the byte sequence as a simple augmentation example.
      - For dictionaries: Applies augmentation to the 'features' value while keeping 'label' unchanged.

    :param sample: The input sample to augment, which may be a number, a list, a string, bytes, or a dict.
    :return: The augmented sample.
    """
    # Augment a single numeric value by adding 1
    if isinstance(sample, (int, float)):
        return sample + 1

    # If sample is a dictionary, process its 'features'
    if isinstance(sample, dict):
        features = sample.get('features')
        label = sample.get('label')

        # For text, convert to uppercase
        if isinstance(features, str):
            features = features.upper()
        # For a list of numbers, add 1 to each element
        elif isinstance(features, list) and all(isinstance(x, (int, float)) for x in features):
            features = [x + 1 for x in features]
        # For binary data, duplicate the bytes (simple augmentation example)
        elif isinstance(features, bytes):
            features = features * 2
        return {'features': features, 'label': label}

    # If sample type is not recognized, return it unchanged
    return sample
