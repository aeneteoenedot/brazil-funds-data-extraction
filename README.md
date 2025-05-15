# CVM Investment Funds Extract Downloader

This Python script automates the download, cleanup, and loading of the **daily extract of Brazilian investment funds ("Extrato Diários")** from the official [CVM (Comissão de Valores Mobiliários)](https://www.gov.br/cvm/pt-br) website.

It is designed to streamline data ingestion for analysts, researchers, or commercial teams interested in exploring and analyzing fund data for regulatory, financial, or strategic purposes.

---

## Features

- 📥 **Download Automation**  
  Downloads the latest `extrato_fi.csv` file from the CVM open data portal.

- 🧹 **Local Cleanup**  
  Deletes previously downloaded CSV files to ensure only the latest data is stored locally.

- 🔍 **Smart File Parsing**  
  Automatically detects CSV file encoding and separator using common Brazilian formats.

- 📊 **Immediate Data Access**  
  Loads the dataset into a pandas DataFrame and displays a preview of the data.

---

## Functions Overview

- `read_csv_interpreter(file_path)`  
  Attempts to read a CSV file using multiple separator and encoding combinations. Returns the most suitable format for parsing Brazilian financial data.

- `delete_old_files(file_path)`  
  Removes all `.csv` files from the specified directory to prevent outdated data usage.

- `cvm_dwnld_and_save(file_path, url_list)`  
  Downloads the daily extract from the CVM website and saves it locally. Automatically clears old files before saving.

- `main()`  
  Coordinates the download, file cleanup, format detection, and initial data loading. Prints the first few rows of the resulting DataFrame.

---

## Usage

1. Clone or download this repository.
2. Ensure you have the required dependencies:
   ```bash
   pip install pandas requests
