import csv

csv_writer: csv.writer


class DumpDatabase:

    def step(self, *data):
        row = [data]
        csv_writer.writerows(row)

    def finalize(self):
        return ""
