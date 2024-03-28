import json
import os
import tqdm


class AddSn:

    def __init__(self, path, keys_per_file, num_key_files):
        self.path = path
        self.keys_per_file = keys_per_file
        self.num_key_files = num_key_files

    def add_sn(self):
        file_list = [file for file in os.listdir(self.path) if "_temp_" in file]
        data = []

        for file in file_list:
            with open(self.path + file, 'r') as infile:
                data += (json.load(infile))

        data_list = []
        i = 0
        j = 0
        for key in tqdm.tqdm(data):
            if i >= self.keys_per_file:
                with open(self.path + str(j).zfill(len(str(self.num_key_files - 1))) + '_key.json', 'w') as outfile:
                    json.dump(data_list, outfile)
                    # print(f"Saved {outfile}")
                i = 0
                j = j + 1
                data_list = []

            sn = str(j).zfill(len(str(self.num_key_files-1))) + '_' + str(i).zfill(len(str(self.keys_per_file-1)))
            data_list.append((sn, key['pin_list'], key['lugs'], key['letter_check']))
            i = i + 1

        filename = self.path + str(j).zfill(len(str(self.num_key_files - 1))) + '_key.json'
        with open(filename, 'w') as outfile:
            json.dump(data_list, outfile)
            # print(f"Saved {outfile}")
