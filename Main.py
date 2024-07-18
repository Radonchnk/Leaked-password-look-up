import os
import time

from tools.ExternalSort import SortFile
from tools.SplitFile import storeFile
from tools.BinarySearch import findPassword

def storeFiles():
    unsortedDataFolder = "RawData"
    sortedDataFolder = "SortedData"

    filesInDirectory = os.listdir(unsortedDataFolder)

    if len(filesInDirectory) >= 1:
        print(f"\nFiles to process: {len(filesInDirectory)}")
    else:
        print("\nNo files to process")

    for file in filesInDirectory:
        filePath = os.path.join(unsortedDataFolder, file)
        outputFile = "TempSortedData.txt"
        # Value max_line=10000000 roughly makes files of 100 mb
        SortFile(big_file=filePath, outfile=outputFile, max_line=10000000)
        print("""
    - Entire file is sorted
    - Preparing file for binary sort""")

        storeFile(file_path="TempSortedData.txt", destination_folder=sortedDataFolder, file_name=file)

def searchPassword(password):
    is_found = 0
    stat_time = time.time()

    sortedDataFolder = "SortedData"

    passwordSets = os.listdir(sortedDataFolder)

    for passwordSet in passwordSets:

        path_to_leak = os.path.join(sortedDataFolder, passwordSet)

        result = findPassword(password=password, folder_path=path_to_leak)

        if result:
            is_found = 1
            print("""
    ==================
    Password was found
    ==================
            """)
            print("Dataset name:", passwordSet)
            print("Nearby standing passwords:")
            [print(x) for x in result]

    if not is_found:
        print("Password was not found in any of datasets!")

    end_time = time.time()

    print("Time taken:", end_time-stat_time)
    print("Files searched:", len(passwordSets))


print("""
    ====================
    Password Leak Lookup
    ====================""")

while True:

    user_input = input("\nSelect action: 1 - add files to dataset, 2 - search for password: ")
    if user_input == "1":
        storeFiles()
    elif user_input == "2":
        password = input("Enter password to lookup: ")
        searchPassword(password=password)