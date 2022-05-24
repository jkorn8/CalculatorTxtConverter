START_OF_FILE_CODE = 0x2A2A54493833462A1A0A00
COMMENT_CODE = 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000

DATA_SECTION_CONST = 0x0D00
VAR_ID = 0x15
VAR_FLAG = 0x0080

TWO_BYTES_SIZE = 2 ** 16

class FileWriter:
    def __init__(self, text_filename, chars):
        self.chars = chars
        self.full_filename = text_filename
        self.filename = text_filename[:-4]
        self.calc_filename = self.filename + '.8xv'
        self.num_chars = len(chars)

    def write_header(self):
        bytes_of_data_section = self.num_chars + 47
        bytes_of_var_data = self.num_chars + 30
        bytes_of_var = self.num_chars + 28

        with open(self.calc_filename, "wb") as calc_file:
            # Header
            calc_file.write(START_OF_FILE_CODE.to_bytes(11, 'big'))
            calc_file.write(COMMENT_CODE.to_bytes(42, 'big'))
            calc_file.write(bytes_of_data_section.to_bytes(2, 'little'))        # Variable

            # Data Section
            calc_file.write(DATA_SECTION_CONST.to_bytes(2, 'big'))
            calc_file.write(bytes_of_var_data.to_bytes(2, 'little'))            # Variable
            calc_file.write(VAR_ID.to_bytes(1, 'big'))

            for i in range(0, 8):
                if i < len(self.filename):
                    calc_file.write(bytes(self.filename[i], 'utf-8'))
                else:
                    calc_file.write(b'\x00')

            calc_file.write(VAR_FLAG.to_bytes(2, 'big'))
            calc_file.write(bytes_of_var_data.to_bytes(2, 'little'))            # Variable
            calc_file.write(bytes_of_var.to_bytes(2, 'little'))                 # Variable

    def write_body(self):
        with open(self.calc_filename, "ab") as calc_file:
            calc_file.write(b'\x4D\x41\x54\x45\x4F')
            for i in range(0, 20):
                if i < len(self.full_filename):
                    calc_file.write(bytes(self.full_filename[i], 'utf-8'))
                else:
                    calc_file.write(b'\x0D')
            for char in self.chars:
                if char == '\n':
                    calc_file.write(b'\x0D')
                else:
                    calc_file.write(bytes(char, 'utf-8'))
            calc_file.write(b'\xFF\x0D\x00')

    def write_end_of_file(self):
        checksum = self.calculate_checksum()
        with open(self.calc_filename, "ab") as calc_file:
            calc_file.write(checksum.to_bytes(2, 'little'))
        print(f'Checksum calculated: {hex(checksum)}\n--------------')
        print(f'{self.full_filename} copied to file: {self.calc_filename}')

    def calculate_checksum(self):
        checksum = 0
        with open(self.calc_filename, 'rb') as calc_file:
            byte = calc_file.read(55)                           # Read from the start of the data section
            while byte:
                byte = calc_file.read(1)
                checksum = checksum + int.from_bytes(byte, "big")
        if checksum > TWO_BYTES_SIZE:
            checksum = checksum % TWO_BYTES_SIZE
        return checksum
