import csv


class SaveData():
    def __init__(self, filename):
        self.file = open(filename, 'w')
        self.writer = csv.writer(self.file)

    def write_data(self, *data):
        self.writer.writerows(data)
