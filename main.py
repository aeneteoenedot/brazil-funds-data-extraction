import pandas as pd
"""
This script downloads the daily extract of Brazilian investment funds ("Extrato diários") from the CVM website, saves it locally, and reads the CSV file while automatically detecting its separator and encoding. The script provides utility functions for:
Functions:
----------
- read_csv_interpreter(file_path):
    Determines the separator and encoding of a CSV file by attempting to read it with common Brazilian data formats. Returns the detected separator and encoding.
- delete_old_files(file_path):
    Deletes all CSV files in the specified directory to ensure only the latest data is present.
- cvm_dwnld_and_save(file_path, url_list):
    Downloads the CSV file from the provided CVM URL and saves it to the specified directory, removing any old CSV files beforehand.
- main():
    Orchestrates the download, file cleanup, separator/encoding detection, and initial data loading. Prints the first few rows of the loaded DataFrame for inspection.
Usage:
------
Run the script to download the latest "extrato_fi.csv" from the CVM, clean up old files, and display the head of the DataFrame. The script is designed for general data analysis and commercial insights on Brazilian investment funds.
Note:
-----
- The script is robust to unknown file formats by attempting multiple separator and encoding combinations.
- It is safe to run multiple times; each run ensures only the latest data is present in the target directory.
"""
import requests
import os

def read_csv_interpreter(file_path):
    # The purpose of this function is to be complimentary to panda's own functionality of reading csv files
    # Since the particularities of the the file are not know, this function will be used to check the separator and encoding
    # The function will return the separator and encoding used in the file for better understanding of the data 
    separators = [';','/','|','\t',','] # These are the most common separators for Brazilian data
    encodings = ['utf-8', 'latin1', 'iso-8859-1'] # These encodings are the most common ones for Brazilian data
    for encoding in encodings:
        for sep in separators:
            try:
                df = pd.read_csv(file_path, sep=sep, encoding=encoding, nrows=2)
                if not df.empty:
                    return sep, encoding
            except Exception:
                continue
    raise ValueError("Unable to determine the separator and encoding of the file.")


def delete_old_files(file_path):
    for file in os.listdir(file_path):
        if file.endswith('.csv'):
            os.remove(os.path.join(file_path, file))

def cvm_dwnld_and_save(file_path, url_list):
    #This function will download the file from CVM website and save it locally
    # The file will be saved in the path defined by the user
    try:
        response = requests.get(url_list)
    except Exception as e:
        print(f"Error fetching data from CVM: Error - {e}")
        return None
    if response.status_code == 200:
        # Delete any lingering file within the folder to reinforce consistency
        delete_old_files(file_path)
        # Save the file locally
        with open(os.path.join(file_path, 'extrato_fi.csv'), 'wb') as file:
            file.write(response.content)
    else:
        print("Failed to download the file. Status code:", response.status_code)
        return None
    return 1

def main():
    # Define file path
    file_path = './'
    # For the purpose of this script, only "Extrato diários" will be downloaded, "Extrato diários" are available in the following URL:
    url_list = 'https://dados.cvm.gov.br/dados/FI/DOC/EXTRATO/DADOS/extrato_fi.csv'
    if cvm_dwnld_and_save(file_path, url_list) is None:
        print("Failed to download the file, exiting...")
        return
    sep, encoding = read_csv_interpreter(os.path.join(file_path, 'extrato_fi.csv'))
    # Read the file using the separator and encoding obtained from the read_csv_interpreter function
    df = pd.read_csv(os.path.join(file_path, 'extrato_fi.csv'), sep=sep, encoding=encoding)
    # Check if the file is empty
    if df.empty:
        print("The file is empty, exiting...")
        return
    print(df.head())
    # From this point onward, the user can choose to manipulate the data as they see fit
    # An interesting analysis here would be to normalize the data and build a KNN model to suggest best-fit funds for the user
    # The user can also choose to save the data in a different container, such as a AWS S3 bucket or a SQL database for easier access and manipulation

if __name__ == '__main__':
    # This script's purpose will be to perform a basic task of downloading the brazilian funds data from CVM website so it can be used for general data purposes and commercial insights.
    # The script can be run on-demand and there should represent no issue being ran multiple times.
    # The expected speed should be O(n) where n is the number of lines contained within the downloaded file.
    # The number of lines contained within the file is expected to be variable as new funds get registered and old ones get closed.
    main()