class DataStorage:

    def __init__(self, file_path):
        self.file_path = file_path

    def write_to_file(self, data, codes, quantization_level):
        f = open(self.file_path, "w")
        f.write(data + "\n")
        codes_line = ""
        for i in codes.keys():
            codes_line += str(i) + " " + str(codes[i]) + " "
        f.write(codes_line[:-1] + "\n")
        f.write(str(quantization_level) + "\n")
        f.close()

    def read_from_file(self):
        f = open(self.file_path, "r")
        data = f.readline().strip()
        codes = {}
        split_codes = f.readline().strip().split(" ")
        for i in range(len(split_codes) // 2):
            codes[split_codes[2 * i]] = split_codes[2 * i + 1]
        quantization_level = int(f.readline().strip())
        ans = {"data": data, "codes": codes, "quantization_level": quantization_level}
        return ans
