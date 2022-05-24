import sys
from FileWriter import FileWriter


def conv_text(text_filename):
    text_file = open(text_filename, "r")
    data = text_file.read()
    number_of_characters = len(data)
    print('Number of characters in text file :', number_of_characters)
    file_writer = FileWriter(text_filename, data)

    file_writer.write_header()
    file_writer.write_body()
    file_writer.write_end_of_file()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Correct usage: \"CalcConvText.py [filename]\"')
    elif sys.argv[1][-4:] != '.txt':
        print(f'File to convert must be a text file')
    else:
        filename = sys.argv[1]
        try:
            conv_text(filename)
        except FileNotFoundError:
            print(f'File {filename} not found')
    print()
