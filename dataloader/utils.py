# dataloader/utils.py

import time
from functools import wraps

def timer(func):
    """
    Decorator to measure and print the time taken by a function.

    This is useful for performance tracking, especially for 
    functions that involve file I/O, data processing, or network requests.

    :param func: The function being wrapped.
    :return: The wrapped function with execution time logging.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start time tracking
        result = func(*args, **kwargs)  # Execute the function
        elapsed = time.time() - start_time  # Calculate elapsed time
        print(f"Function '{func.__name__}' took {elapsed:.2f}s to complete.")
        return result
    return wrapper


def download_file(url, dest_path):
    """
    Downloads a file from a given URL and saves it to the specified destination.

    Uses a streaming approach to handle large files efficiently without consuming
    excessive memory. The function raises an exception if the request fails.

    :param url: The URL of the file to be downloaded.
    :param dest_path: The local path where the downloaded file should be saved.
    """
    import requests  # Imported here to avoid unnecessary dependency if unused

    try:
        # Stream download to efficiently handle large files
        with requests.get(url, stream=True) as r:
            r.raise_for_status()  # Raise an error if the request fails
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):  # Read in chunks
                    if chunk: 
                        f.write(chunk)  # Write each chunk to the file
        print(f"Downloaded file successfully to {dest_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")


def cache_data(func):
    """
    Simple caching decorator to avoid recomputing expensive function calls.

    This decorator uses `functools.lru_cache` to cache results for functions
    that return the same output for the same input.

    **Limitations:**
      - Only works for functions with hashable arguments.
      - Not suitable for functions that return large datasets, as it stores results in memory.

    :param func: The function to be cached.
    :return: The wrapped function with caching enabled.
    """
    from functools import lru_cache

    # Wrap the function with an LRU (Least Recently Used) cache
    cached_func = lru_cache(maxsize=None)(func)

    def wrapper(*args, **kwargs):
        return cached_func(*args, **kwargs)

    return wrapper
