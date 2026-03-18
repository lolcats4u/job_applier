import csv

class File():
    def __init__(self, file_name):
        self.file_name = file_name
        self.contents = self.read_file(self.file_name)

    def read_file(self):
        with open( self.file_name , "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            self.contents = list(csv_reader)
    
    def write_row(self,row):
        with open(self.file_name, "w", encoding="utf-8") as file:
            csv_writer = csv.DictWriter.writerow(row)

