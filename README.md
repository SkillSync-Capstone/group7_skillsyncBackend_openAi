# group7_capstone_backend

## Overview
This repository contains the backend code for our capstone project. It is developed using Python 3.11.

## Prerequisites
Ensure that you have Python 3.11 installed on your system to run this project.

## Setup

### Creating a Virtual Environment
Before installing the required packages, it's recommended to create a virtual environment to avoid conflicts with other packages and versions:

- **For Windows:**
  ```bash
  python -m venv myenv

  myenv\Scripts\activate

- **For  macOS and Linux:**
  ```bash
    python -m venv myenv
    
    source myenv/bin/activate

### Installing Dependencies
    pip install -r requirements.txt

### Running the Application
    python app.py

### Deactivating the Virtual Environment

Before installing the required packages, it's recommended to create a virtual environment to avoid conflicts with other packages and versions:

- **For Windows:**
  ```bash
    myenv\Scripts\deactivate

- **For  macOS and Linux:**
  ```bash
   deactivate

### Additional Python Commands
- **To find which Python is being used:**
  ```bash
    which python

- **To list Python site-packages:**
     ```bash
    python -m site
- **To check for the 'chromadb' package and its location:**
     ```bash
        pip list | grep chromadb
        python -c "import chromadb; print(chromadb.__file__)"

