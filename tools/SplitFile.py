import os
import json
import tarfile
import io
import time

def createMetadataFile(metadata, metadata_folder_path):
    metadata_file_path = os.path.join(metadata_folder_path, "metadata.json")

    # Create a list to hold the dictionaries
    data_to_store = []

    # Process each sublist in the array
    for item in metadata:
        # Ensure the item has exactly three elements
        if len(item) == 3:
            # Create a dictionary with the appropriate keys and values
            entry = {
                "file_name": item[0],
                "first_word": item[1],
                "last_word": item[2]
            }
            # Append the dictionary to the list
            data_to_store.append(entry)

    # Write the list of dictionaries to the JSON file
    with open(metadata_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_to_store, json_file, ensure_ascii=False, indent=4)


def splitAndStore(file_path, file_folder, lines_per_file=10000000):
    """
    Splits the input file into chunks and stores them as tar.gz archives in memory.

    :param file_path: Path to the input file to be split.
    :param file_folder: Folder where the output tar.gz files will be stored.
    :param lines_per_file: Number of lines per split file.
    :return: List of metadata about the created tar.gz files.
    """

    line_holder = []
    chunk_file_list = []
    cpt = 0

    with open(file=file_path, encoding="utf-8") as f:
        for line in f:
            line_holder.append(line)
            cpt += 1

            if cpt % lines_per_file == 0:
                cpt = 0
                temp_file_name = f'chunk_{len(chunk_file_list)}.txt'

                # Create in-memory bytes stream
                temp_file = io.BytesIO()
                # Write lines to the in-memory bytes stream
                temp_file.write(''.join(line_holder).encode('utf-8'))
                temp_file.seek(0)

                # Store the in-memory bytes stream in a tar.gz archive
                tar_file_name = f'chunk_{len(chunk_file_list)}.tar.gz'
                tar_chunk_file_path = os.path.join(file_folder, tar_file_name)

                with tarfile.open(tar_chunk_file_path, 'w:gz') as tar:
                    # Add the in-memory bytes stream to the tar.gz archive
                    tarinfo = tarfile.TarInfo(name=temp_file_name)
                    tarinfo.size = temp_file.getbuffer().nbytes
                    tar.addfile(tarinfo, fileobj=temp_file)

                temp_file.close()

                # First and last lines are needed for metadata to do further finding
                first_line = line_holder[0]
                last_line = line_holder[-1]
                line_holder = []
                chunk_file_list.append([tar_file_name, first_line, last_line])

        if line_holder:
            temp_file_name = f'chunk_{len(chunk_file_list)}.txt'

            # Create in-memory bytes stream
            temp_file = io.BytesIO()
            # Write lines to the in-memory bytes stream
            temp_file.write(''.join(line_holder).encode('utf-8'))
            temp_file.seek(0)

            # Store the in-memory bytes stream in a tar.gz archive
            tar_file_name = f'chunk_{len(chunk_file_list)}.tar.gz'
            tar_chunk_file_path = os.path.join(file_folder, tar_file_name)

            with tarfile.open(tar_chunk_file_path, 'w:gz') as tar:
                # Add the in-memory bytes stream to the tar.gz archive
                tarinfo = tarfile.TarInfo(name=temp_file_name)
                tarinfo.size = temp_file.getbuffer().nbytes
                tar.addfile(tarinfo, fileobj=temp_file)

            temp_file.close()

            # First and last lines are needed for metadata to do further finding
            first_line = line_holder[0]
            last_line = line_holder[-1]
            line_holder = []
            chunk_file_list.append([tar_file_name, first_line, last_line])

    return chunk_file_list

def storeFile(file_path, destination_folder, file_name):

    os.makedirs(destination_folder, exist_ok=True)

    file_folder = os.path.join(destination_folder, file_name)

    os.makedirs(file_folder, exist_ok=True)
    # Creates dir for chunks of original file to be in

    print("""
    ===============================
    Splitting and Compressing Files
    ===============================""")
    start_time = time.time()

    metadata = splitAndStore(file_path=file_path, file_folder=file_folder)
    end_time = time.time()
    print("Time taken:", end_time-start_time)
    print("""
    ======================
    Compression successful
    ======================""")

    os.remove(file_path)

    createMetadataFile(metadata=metadata, metadata_folder_path=file_folder)
    print("""
    =====================================
    Metadata file is successfully created
    =====================================""")