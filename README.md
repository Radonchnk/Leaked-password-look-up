# Leaked-Password-Lookup

I made my best attempt to create the most memory- and time-efficient lookup table for leaked passwords that you can find on the internet.
Inspired by RockYou2024 (https://github.com/exploit-development/RockYou2024)
This tool is designed for people to check if their password was leaked. If you use it in any malicious way, you are a bad person.
### Installation

Pull the git repo and execute Main.py.
### Usage

There are two folders:
"RawData" and "SortedData."
To add lists of passwords to the dataset, you need to put a txt file with passwords in the "RawData" folder and execute the program:
![image](https://github.com/user-attachments/assets/a86123d9-ea9c-40bf-a803-673418a494ee)
The file will be sorted, compressed, and stored in the "SortedData" folder.
![image](https://github.com/user-attachments/assets/ef504dd1-86fe-4721-b591-7055a7bb276a)

To look up passwords, you need to run the program, select the search option, and write the password:
![image](https://github.com/user-attachments/assets/295c469e-fa91-4a36-bba9-e924226726c8)
### Additional Info

It took roughly 24 hours for my computer to sort and save 160GB of RockYou2024.
Lookup time is roughly constant and stays around 1.5 seconds per file. I have achieved this by using a double binary search. 
The first search is to find which chunk of the text file the password is in, and the second search is to look through the file itself.

This tool comes with pre-sorted rockyou.txt (14kk passwords, 2009 edition)

This project is in the early alpha stage with no error checking and no user-friendly interface.
I may update this project in the future for personal use.
If anyone feels like upgrading it further, feel free!
