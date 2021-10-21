import csv
import sqlite3
import tkinter.filedialog
from tkinter import Tk

import DumpDatabase


def show_file_opener_dialog():
    tk = Tk()
    tk.withdraw()
    return tkinter.filedialog.Open(tk,
                                   title="Choose the file to convert",
                                   filetypes=[('SQL DB file', '.db')],
                                   defaultextension="db").show()


def show_save_as_dialog():
    tk = Tk()
    tk.withdraw()
    title = "Choose the name of the directory to store the converted files"
    return tkinter.filedialog.Directory(tk, title=title).show()


def process_file(db_path, save_folder_path):
    conn = sqlite3.connect(db_path)
    sqlite3.enable_callback_tracebacks(True)
    conn.create_aggregate('dump', -1, DumpDatabase.DumpDatabase)
    data = conn.cursor().execute("SELECT tbl_name FROM main.sqlite_master "
                                 "WHERE type='table' "
                                 "AND tbl_name != 'sqlite_sequence'").fetchall()
    for row in data:
        table_name = row[0]
        path_to_csv = f'{save_folder_path}/{table_name}.csv'
        print('Working on', path_to_csv)
        with open(path_to_csv, mode='w', encoding='utf-8', newline='') as writer:
            DumpDatabase.csv_writer = csv.writer(writer)
            cursor = conn.execute(f'SELECT * FROM {table_name} LIMIT 1;')
            column_tuples = list(cursor.description)
            columns = []
            for column_tuple in column_tuples:
                columns.append(column_tuple[0])
            columns_string = ', '.join(columns)
            conn.execute(f"SELECT dump({columns_string}) FROM {table_name}")
            print('Done', path_to_csv)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    process_file(show_file_opener_dialog(), show_save_as_dialog())
