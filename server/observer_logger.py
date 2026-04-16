import gzip

class Observer:
    def __init__(self, output_file):
        # self.player_names = player_names
        self.output_file_name = output_file
        self.output_file = gzip.open(output_file, "wb")

    def write(self, data:str, end='\n'):
        data += end
        self.output_file.write(data.encode('UTF-8'))
        self.output_file.flush()

    def close(self):
        self.output_file.close()
        # f = gzip.open(self.output_file_name + '.gz', "w")

if __name__ == '__main__':
    import os
    print('\n\n[ UNIT TEST BEGIN ]')
    print('[ TESTING READING ]\n')
    read_test_file = input('Enter file to read-test: ')
    if os.path.exists(read_test_file):
        content = '[ Failed to read ]'
        with gzip.open(read_test_file, 'rb') as f:
            content = f.readlines()
        print(f'[ FILE CONTENT START ]\n\n{'\n'.join([i.decode('UTF-8') for i in content])}\n\n[ FILE CONTENT END ]')

    print('\n\n[ TESTING WRITING ]\n\n')
    write_test_file = input('Enter output file (empty for same as read-test): ')
    if not write_test_file:
        write_test_file = read_test_file
    o = Observer([], write_test_file)
    i = input('Enter file content (enter to exit): ')
    while i:
        o.write_turn(i)
        i = input('| ')
    o.close()