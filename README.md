# 📦 Capstone DataLoader Project – Your All-in-One Data Helper

[![Python CI](https://github.com/RishitLaddha/session15-Capstone/actions/workflows/test.yml/badge.svg)](https://github.com/RishitLaddha/session15-Capstone/actions/workflows/test.yml)

<img width="1223" alt="Screenshot 2025-02-18 at 16 02 35" src="https://github.com/user-attachments/assets/22c55a20-84ac-4414-829e-c558cbb134f8" />


Welcome to the **Capstone DataLoader Project**!
This is a Python tool I built to make working with datasets super easy. Whether it’s **images, text, CSV files, or even messy unstructured data**, this DataLoader can handle it all.

The idea is simple:

* **For beginners** → easy to use and understand.
* **For advanced users** → flexible enough to extend and customize.

Think of it as your **Swiss Army knife for loading and preparing data**.

---

## 🔎 Overview

At the heart of this project is a **DataLoader class** that takes care of all the boring stuff when it comes to data:

* Reads different file formats
* Downloads datasets if they’re missing
* Cleans and preprocesses the data so it’s ready for use

This means you don’t have to worry about setup every time—you can just focus on your project or machine learning model.

---

## 🗂️ Project Structure

Here’s how everything is organized:

```
project_root/
├── dataloader/
│   ├── __init__.py
│   ├── dataloader.py       # main DataLoader class
│   ├── preprocessors.py    # functions to clean/transform data
│   └── utils.py            # helper tools like downloads + timers
├── datasets/               # your datasets live here
├── tests/                  # unit tests
│   └── test_dataloader.py
├── main.py                 # entry point (run from command line)
└── requirements.txt        # needed Python packages
```

---

## 🌟 Key Features

### 1. Flexible Data Loading

* **Images** → works with CIFAR-10/100 and can be extended for more
* **Text** → reads simple text datasets in UTF-8
* **CSV files** → loads structured data row by row
* **Unstructured data** → scans folders and picks up all files

👉 Bonus: If the dataset isn’t already in your `datasets/` folder, the DataLoader can **download it automatically** if you give it a link.

---

### 2. Preprocessing & Normalization

Raw data is rarely ready-to-use. This DataLoader includes:

* **Default preprocessing** → cleans up text by removing extra spaces
* **Normalization** → scales numbers (like pixel values) into a nice `[0,1]` range
* **Augmentation** → basic tricks like uppercase text, adding constants to numbers, or duplicating binary data (can easily be extended for image flips, noise, etc.)

---

### 3. Modular & Easy to Extend

The code is designed to stay clean and flexible:

* Separate files for different jobs (loader, preprocessors, utils)
* You can pass your own **custom preprocessing functions**
* Helper utilities like downloaders and timers keep the core simple

---

### 4. Batch Processing

Built-in **batch support** so you can:

* Loop over data in fixed batch sizes
* Shuffle data between epochs
* Always get full batches (even if dataset size doesn’t divide evenly)

This makes it perfect for machine learning workflows.

---

### 5. Command-Line Ready

Run the DataLoader straight from the terminal:

```bash
python main.py CIFAR-10 64 --normalize --augment
```

This will:

* Load CIFAR-10
* Apply normalization + augmentation
* Process data in batches of 64

---

### 6. Testing Built-In

The project has **unit tests** to make sure everything works:

* Data loading + downloads
* Normalization + preprocessing
* Iterator behavior
* Command-line arguments

So you can trust it won’t break when you add new features.

---

## ⚡ Example Workflow

Say you’re working with the **MNIST dataset**. Just run:

```bash
python main.py MNIST 32 --normalize --augment
```

What happens:

1. The DataLoader checks if MNIST is downloaded (downloads if missing).
2. Cleans + normalizes + augments the data.
3. Loads it in batches of 32.
4. Prints a preview so you know what’s going on.

Easy, right?

---

## 💡 Why This Project?

When doing ML projects, I found myself repeating the same steps—downloading datasets, normalizing them, writing loaders. So I built this project to:

* Save time
* Keep things clean and modular
* Make it beginner-friendly but still powerful

---


## 🔮 Limitations & Future Plans

Like any project, this one’s still a work in progress. Right now, the DataLoader:

* Handles common formats (images, text, CSV, unstructured files) but not huge archives like `.zip` or `.tar` out of the box.
* Has only very simple augmentation (uppercase text, add constants, duplicate bytes). No fancy stuff like image flips, rotations, or noise yet.
* Normalization is basic — it works, but could be extended for dataset-specific needs.

**What I plan to add next:**

* Smarter augmentation for images (flips, rotations, brightness changes).
* Support for compressed datasets so you don’t have to manually extract them.
* More preprocessing functions that can be plugged in easily.
* Better logging/visualization so you can see what’s happening under the hood.

---

## 🚀 Final Thoughts

The **Capstone DataLoader** solves the everyday problems of handling datasets—loading, cleaning, and batching.

* Beginners can use it out of the box.
* Experienced devs can extend it for complex workflows.

Feel free to explore, run tests, and use this as a foundation in your own projects.

Thanks for checking it out! 🎉

---
