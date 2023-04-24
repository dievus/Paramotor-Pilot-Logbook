import tkinter as tk
import sqlite3
from tkinter import ttk
import csv
import tkinter.filedialog as fd

connection = sqlite3.connect('flight_data.db')
cursor = connection.cursor()

# create flight_data table if it does not already exist
cursor.execute('''CREATE TABLE IF NOT EXISTS flight_data
                (id INTEGER PRIMARY KEY,
                date TEXT,
                full_stop_landings INTEGER,
                touch_and_go INTEGER,
                distance_flown INTEGER,
                duration_of_flight INTEGER,
                airport TEXT,
                notes TEXT)''')


def add_flight_data():
    # get data from user input
    date = date_var.get()
    full_stop = int(full_stop_var.get())
    touch_go = int(touch_go_var.get())
    distance = float(distance_var.get())
    duration = float(duration_var.get())
    airport_info = airport_info_var.get()
    notes = notes_var.get()

    # insert data into table
    cursor.execute('''INSERT INTO flight_data(date, full_stop_landings, touch_and_go, distance_flown, duration_of_flight, airport, notes)
                    VALUES(?,?,?,?,?,?,?)''', (date, full_stop, touch_go, distance, duration, airport_info, notes))
    connection.commit()

    # clear user input fields
    date_var.set('')
    full_stop_var.set('')
    touch_go_var.set('')
    distance_var.set('')
    duration_var.set('')
    airport_info_var.set('')
    notes_var.set('')

    # update table display
    display_data()


def display_data():
    # delete previous table display
    for widget in data_frame.winfo_children():
        widget.destroy()

    # create new table display
    cursor.execute('''SELECT * FROM flight_data ORDER BY id DESC LIMIT 5''')
    data = cursor.fetchall()

    # create table headers
    headers = ['Flight Number', 'Date', 'Number of Flights', "Touch and Go's",
               'Distance Flown (Miles)', 'Duration of Flight (Minutes)', 'Airport (Optional)', 'Notes']
    for i in range(len(headers)):
        header_label = ttk.Label(data_frame, text=headers[i])
        header_label.grid(row=0, column=i, padx=5, pady=5)

    # create table rows
    for i in range(len(data)):
        for j in range(len(data[i])):
            data_label = ttk.Label(data_frame, text=data[i][j])
            data_label.grid(row=i+1, column=j, padx=5, pady=5)

    # create footer with sums
    full_stop_landings_sum = cursor.execute(
        '''SELECT SUM(full_stop_landings) FROM flight_data''').fetchone()[0]
    touch_and_go_sum = cursor.execute(
        '''SELECT SUM(touch_and_go) FROM flight_data''').fetchone()[0]
    distance_flown_sum = cursor.execute(
        '''SELECT SUM(distance_flown) FROM flight_data''').fetchone()[0]
    duration_of_flight_sum = cursor.execute(
        '''SELECT SUM(duration_of_flight) FROM flight_data''').fetchone()[0]
    if full_stop_landings_sum is None:
        full_stop_landings_sum = 0
    else:
        full_stop_landings_sum = (
            int(full_stop_landings_sum) + int(touch_and_go_sum))
    if duration_of_flight_sum is None:
        duration_of_flight_sum = 0
    else:
        duration_of_flight_sum = round(duration_of_flight_sum / 60, 2)
    if distance_flown_sum is None:
        distance_flown_sum = 0
    else:
        distance_flown_sum = round(distance_flown_sum, 2)
    footer_label = ttk.Label(
        text=f'Total Flights: {full_stop_landings_sum} | Total Distance Flown: {distance_flown_sum} miles | Total Duration of Flight: {duration_of_flight_sum} hrs', anchor='w')
    footer_label.grid(row=len(data)+1, column=0, columnspan=7, padx=5, pady=5)


def close_app():
    connection.close()
    root.quit()


# create tkinter window
root = tk.Tk()
root.title('Paramotor Pilot Logbook')

# create data entry form
data_entry_frame = ttk.LabelFrame(root, text='Enter Flight Data')
data_entry_frame.grid(row=0, column=0, padx=10, pady=10)

date_label = ttk.Label(data_entry_frame, text='Date (DD/MM/YYYY):')
date_label.grid(row=0, column=0, padx=5, pady=5)
date_var = tk.StringVar()
date_entry = ttk.Entry(data_entry_frame, textvariable=date_var)
date_entry.grid(row=0, column=1, padx=5, pady=5)

full_stop_label = ttk.Label(
    data_entry_frame, text='Number of Full Stop Landings:')
full_stop_label.grid(row=1, column=0, padx=5, pady=5)
full_stop_var = tk.IntVar()
full_stop_entry = ttk.Entry(data_entry_frame, textvariable=full_stop_var)
full_stop_entry.grid(row=1, column=1, padx=5, pady=5)

touch_go_label = ttk.Label(
    data_entry_frame, text="Number of Touch and Go's:")
touch_go_label.grid(row=2, column=0, padx=5, pady=5)
touch_go_var = tk.IntVar()
touch_go_entry = ttk.Entry(data_entry_frame, textvariable=touch_go_var)
touch_go_entry.grid(row=2, column=1, padx=5, pady=5)

distance_label = ttk.Label(data_entry_frame, text='Distance Flown (miles):')
distance_label.grid(row=3, column=0, padx=5, pady=5)
distance_var = tk.IntVar()
distance_entry = ttk.Entry(data_entry_frame, textvariable=distance_var)
distance_entry.grid(row=3, column=1, padx=5, pady=5)

duration_label = ttk.Label(
    data_entry_frame, text='Duration of Flight (minutes):')
duration_label.grid(row=4, column=0, padx=5, pady=5)
duration_var = tk.IntVar()
duration_entry = ttk.Entry(data_entry_frame, textvariable=duration_var)
duration_entry.grid(row=4, column=1, padx=5, pady=5)

airport_info_label = ttk.Label(data_entry_frame, text='Airport (Optional):')
airport_info_label.grid(row=5, column=0, padx=5, pady=5)
airport_info_var = tk.StringVar()
airport_info_entry = ttk.Entry(data_entry_frame, textvariable=airport_info_var)
airport_info_entry.grid(row=5, column=1, padx=5, pady=5)

notes_label = ttk.Label(data_entry_frame, text='Notes:')
notes_label.grid(row=6, column=0, padx=5, pady=5)
notes_var = tk.StringVar()
notes_entry = ttk.Entry(data_entry_frame, textvariable=notes_var)
notes_entry.grid(row=6, column=1, padx=5, pady=5)

submit_btn = ttk.Button(data_entry_frame, text='Submit',
                        command=add_flight_data)
submit_btn.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# create table display frame
data_frame = ttk.LabelFrame(root, text='Logbook - Five Most Recent Flights')
data_frame.grid(row=1, column=0, padx=10, pady=10)

# display flight data in table
display_data()

# create menu bar with exit option
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Exit', command=close_app)
menu_bar.add_cascade(label='File', menu=file_menu)
root.config(menu=menu_bar)


def save_flight_log():
    cursor.execute('''SELECT * FROM flight_data''')
    data = cursor.fetchall()
    header = ['Flight Number', 'Date', 'Full Stop Landings', "Touch and Go's",
              'Distance Flown', 'Duration of Flight (Minutes)', 'Airport (Optional)', 'Notes']
    file_types = [('All Files', '*.*'),
                  ('CSV (Comma Separated Value)', '.csv')]
    file_path = fd.asksaveasfilename(
        filetypes=file_types, defaultextension=file_types)
    try:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for row in data:
                writer.writerow(row)
    except FileNotFoundError:
        pass


# Create menu bar with exit and save as csv options
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Save Flight Log', command=save_flight_log)
file_menu.add_command(label='Exit', command=close_app)
menu_bar.add_cascade(label='File', menu=file_menu)
root.config(menu=menu_bar)


def show_about_popup():
    about_window = tk.Toplevel(root)
    about_window.title('About')
    about_window.iconbitmap('parachute.ico')
    about_window.resizable(False, False)
    about_window.geometry('400x300')
    about_text = tk.Label(
        about_window, text='''Paramotor Pilot Logbook
        Version 1.0
        
        Created by Joe Helle
        USPPA Member No. 10524
        
        Report issues to 
        https://github.com/dievus/Paramotor-Pilot-Logbook.
        
        Paramotor Pilot Logbook is provided as-is with no 
        warranty or guarantee. The software is provided 
        under protection of Apache License 2.0, which 
        requires users to preserve copyright and license
        notices with use, modification, patent, and
        other changes.
        ''', justify='center')
    about_text.pack(padx=10, pady=10)


def show_help_popup():
    help_window = tk.Toplevel(root)
    help_window.title('Help')
    help_window.iconbitmap('parachute.ico')
    help_window.geometry('400x300')
    help_window.resizable(False, False)
    help_text = tk.Label(
        help_window, text='''
        This is the help section for the Paramotor Pilot Logbook.\n\n
        To make a flight log entry, enter the information for your
        flight as required in the "Enter Flight Data" section.\n\n
        Flight logs are saved in a file called a 'SQLite3 database.'
        The five most recent flights are shown in the interface. 
        
        Additional flights are stored in the SQLite3 database.
        To export your file as a .CSV file, click on File -> Save Flight Log,
        and then specify the name and location to save the file to. 
        
        Report issues to 
        https://github.com/dievus/Paramotor-Pilot-Logbook.
        
        ''')
    help_text.pack(padx=10, pady=10)


menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Save Flight Log', command=save_flight_log)
file_menu.add_command(label='Exit', command=close_app)
menu_bar.add_cascade(label='File', menu=file_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label='About', command=show_about_popup)
help_menu.add_command(label='Help', command=show_help_popup)
menu_bar.add_cascade(label='Help', menu=help_menu)

root.config(menu=menu_bar)
root.resizable(False, False)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.minsize(400, 400)
root.maxsize(1200, 800)
root.iconbitmap("parachute.ico")
root.mainloop()
