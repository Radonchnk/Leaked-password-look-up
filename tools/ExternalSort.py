import os
import time

from tools.CustomHeap import MinHeap



def split_large_file(starting_file, temp_dir, max_line=10000000):
    """
    Split the large file into smaller sorted files.

    :param starting_file: input file to be split
    :param temp_dir: temporary directory
    :param max_line: number of lines to put in each smaller file (ram usage)
    :return: a list with all temporary file paths
    """
    temp_file_list = []
    line_holder = []
    cpt = 0

    with open(starting_file, 'r', encoding="utf-8", errors="ignore") as f_in:
        for line in f_in:
            line_holder.append(line)
            cpt += 1
            # lines appended until limit of lines per file is reached

            if cpt % max_line == 0:
                # check if limit of lines per file is reached
                cpt = 0
                line_holder.sort()
                temp_file_name = f'temp_{len(temp_file_list)}.txt'
                temp_file_path = os.path.join(temp_dir, temp_file_name)
                with open(temp_file_path, 'w', encoding="utf-8") as temp_file:
                    temp_file.writelines(line_holder)
                line_holder = []
                temp_file_list.append(temp_file_path)

        # This line is used for case when all file is read but there is not enough lines to trigger first if
        if line_holder:
            line_holder.sort()
            temp_file_name = f'temp_{len(temp_file_list)}.txt'
            temp_file_path = os.path.join(temp_dir,temp_file_name)
            with open(temp_file_path, 'w', encoding="utf-8") as temp_file:
                temp_file.writelines(line_holder)
            temp_file_list.append(temp_file_path)

    print("Temp file num:", len(temp_file_list))
    return temp_file_list


def merged(temp_file_list, out_file):
    """
    Merge the sorted temporary files into a single sorted output file.

    :param temp_file_list: a list with all temporary file paths
    :param out_file: the output file
    :param col: the column where to perform the sort
    :return: path to output file
    """
    my_heap = MinHeap()
    file_pointers = [open(temp_file, 'r', encoding="utf-8") for temp_file in temp_file_list]

    for file_pointer in file_pointers:
        line = file_pointer.readline()
        if line:
            my_heap.insert([line, file_pointer])

    with open(out_file, "w", encoding="utf-8") as out:
        while not my_heap.is_empty():
            minimal = my_heap.extract_min()
            out.write(minimal[0])
            file_pointer = minimal[1]
            line = file_pointer.readline()
            if line:
                my_heap.insert([line, file_pointer])
            else:
                file_pointer.close()
                os.remove(file_pointer.name)

    return out_file


def SortFile(big_file, outfile, tmp_dir=None, max_line=10000000):
    if not tmp_dir:
        tmp_dir = os.getcwd()

    temp_dir = os.path.join(tmp_dir, 'temp_sort')
    os.makedirs(temp_dir, exist_ok=True)

    print("""
    ==============
    Splitting File
    ==============""")
    start_time = time.time()

    temp_file_list = split_large_file(big_file, temp_dir, max_line)
    end_time = time.time()
    print("Time taken:", end_time-start_time)
    print("""
    ====================
    Splitting successful
    ====================""")

    os.remove(big_file)
    # Remove original unsorted file

    print("""
    =============
    Merging Files
    ==============""")
    start_time = time.time()

    merged(temp_file_list=temp_file_list, out_file=outfile)
    end_time = time.time()
    print("Time taken:", end_time-start_time)
    print("""
    ================
    Merge successful
    ================""")

    # Clean up temporary directory
    for temp_file in temp_file_list:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    os.rmdir(temp_dir)