import json
import os.path
import io
import tarfile


def binary_search(arr, target):
    """
    Perform binary search on a sorted array to find the target value.

    :param arr: Sorted list of elements to search.
    :param target: The value to search for.
    :return: The index of the target in the array if found, otherwise -1.
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        # Check if target is present at mid
        if arr[mid] == target:
            return mid
        # If target is greater, ignore left half
        elif arr[mid] < target:
            left = mid + 1
        # If target is smaller, ignore right half
        else:
            right = mid - 1

    # Target is not present in the array
    return -1


def get_elements_around_index(lines, index):
    """
    Retrieves a slice of elements from the 'lines' list around the specified 'index'.

    :param lines: The list of lines.
    :param index: The index around which to retrieve elements.
    :return: List of elements around the index. Empty list if index is out of bounds.
    """
    if index < 0 or index >= len(lines):
        # Index is out of bounds
        return []

    start_index = max(0, index - 2)
    end_index = min(len(lines), index + 3)

    return lines[start_index:end_index]

def read_from_tar(tar_path, file_name):
    """
    Reads data from a specified file within a tar or tar.gz archive and returns it as an array of lines.

    :param tar_path: Path to the tar or tar.gz archive.
    :param file_name: Name of the file within the archive to be read.
    :return: Array of lines read from the specified file.
    """
    lines = []

    # Open the tar archive
    with tarfile.open(tar_path, 'r:*') as tar:
        # Extract the file object from the archive
        file_obj = tar.extractfile(file_name)
        if file_obj is not None:
            # Read the file content and decode it to a string
            content = file_obj.read().decode('utf-8')
            # Split the content into lines
            lines = content.splitlines()

    return lines

def load_json(file_path):
    """
    Loads data from a JSON file and returns it.

    :param file_path: Path to the JSON file.
    :return: Data loaded from the JSON file.
    """

    metadata = []

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for file in data:
        metadata.append([
            file["file_name"],
            file["first_word"],
            file["last_word"]
        ])

    return metadata

def findPassword(folder_path, password):

    metadata_file = os.path.join(folder_path, "metadata.json")

    metadata = load_json(metadata_file)

    # check if password somewhere in range of leaked data
    first_password = metadata[0][1]  # get first line from dataset
    last_password = metadata[-1][2]  # get last line from dataset

    if password < first_password or password > last_password:
        return "Password is not in a dataset"

    left = 0
    right =  len(metadata) - 1

    while left <= right:
        mid = left + (right - left) // 2

        # If target is greater, ignore the left half
        if metadata[mid][2] < password:
            left = mid + 1
        # If target is smaller, ignore the right half
        elif password < metadata[mid][1]:
            right = mid - 1
        else:
            tar_file_name = metadata[mid][0]

            tar_path = os.path.join(folder_path, tar_file_name)

            text_file_name = tar_file_name[:-7] + ".txt"
            lines = read_from_tar(tar_path=tar_path, file_name=text_file_name)

            index = binary_search(arr=lines, target=password)

            if index != -1:
                return get_elements_around_index(lines, index)
            else:
                return False

    return False
    print(metadata)
