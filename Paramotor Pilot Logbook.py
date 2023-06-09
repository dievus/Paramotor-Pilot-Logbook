import tkinter as tk
import sqlite3
from tkinter import ttk
import os.path
import os
import csv
import tkinter.filedialog as fd
from tkinter import messagebox
import webbrowser
from PIL import Image, ImageTk

# create connection to database
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

# function to add flight data to database
def open_record_window(tree):
    selected_item = tree.item(tree.focus())
    record_values = selected_item['values']

    # Create a new window
    record_window = tk.Toplevel(root)
    record_window.title('Flight Record Details')
    record_window.iconbitmap('icons\\parachute.ico')

    # Create a menu bar
    menu_bar = tk.Menu(record_window)
    record_window.config(menu=menu_bar)

    # Create the "File" menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Window", menu=file_menu)

    # Add the "Close" option to the "File" menu
    file_menu.add_command(label="Close", command=record_window.destroy)

    # Display record details in the new window
    record_label = ttk.LabelFrame(record_window, text='Flight Record Details')
    record_label.pack(padx=0, pady=10)

    # record_info = ttk.Label(record_label, text=f'Date: {record_values[1]}\n'
    #                                              f'Number of Flights: {record_values[2]}\n'
    #                                              f"Touch and Go's: {record_values[3]}\n"
    #                                              f'Distance Flown (Miles): {record_values[4]}\n'
    #                                              f'Duration of Flight (Minutes): {record_values[5]}\n'
    #                                              f'Airport: {record_values[6]}')
    # record_info.configure(justify='center')
    # record_info.pack()
    date_label = ttk.Label(record_label, text="Date:")
    date_label.grid(row=0, column=0)
    date = ttk.Label(record_label, text=f'{record_values[1]}')
    date.grid(row=0, column=1)
    flight_label = ttk.Label(record_label, text="Number of Flights:")
    flight_label.grid(row=1, column=0)
    flight = ttk.Label(record_label, text=f'{record_values[2]}')
    flight.grid(row=1, column=1, padx=10)
    touch_label = ttk.Label(record_label, text="Touch and Go's:")
    touch_label.grid(row=2, column=0)
    touch = ttk.Label(record_label, text=f'{record_values[3]}')
    touch.grid(row=2, column=1, padx=10)
    distance_label = ttk.Label(record_label, text="Distance Flown (Miles):")
    distance_label.grid(row=3, column=0)
    distance = ttk.Label(record_label, text=f'{record_values[4]}')
    distance.grid(row=3, column=1, padx=10)
    duration_label = ttk.Label(record_label, text="Duration of Flight (Minutes):")
    duration_label.grid(row=4, column=0)
    duration = ttk.Label(record_label, text=f'{record_values[5]}')
    duration.grid(row=4, column=1, padx=10)
    airport_label = ttk.Label(record_label, text="Airport:")
    airport_label.grid(row=5, column=0)
    airport = ttk.Label(record_label, text=f'{record_values[6]}')
    airport.grid(row=5, column=1, padx=10)

    # Create a labeled frame for flight data
    data_frame = ttk.LabelFrame(record_window, text='Flight Notes')
    data_frame.pack(padx=10, pady=10)

    # Create a text widget inside the labeled frame to display the notes
    notes_text = tk.Text(data_frame, wrap='word', width=80)
    notes_text.insert(tk.END, record_values[7])
    notes_text.configure(state='disabled')
    notes_text.pack(fill='both', expand=True)

def add_flight_data():
    try:
        # get data from user input
        date = date_var.get()
        try:
            full_stop = int(full_stop_var.get())
        except tk.TclError:
            messagebox.showerror(
                'Input Error', 'Please enter a value for total number of full stop landings. If none, enter a zero (0).\n\nPlease try again.')
        try:
            touch_go = int(touch_go_var.get())
        except tk.TclError:
            messagebox.showerror(
                'Input Error', "Please enter a value for total number of Touch and Go's. If none, enter a zero (0).\n\nPlease try again.")
        try:
            distance = float(distance_var.get())
        except tk.TclError:
            messagebox.showerror(
                'Input Error', "Please enter the total distance flown.\n\nPlease try again.")
        try:
            duration = float(duration_var.get())
        except tk.TclError:
            messagebox.showerror(
                'Input Error', "Please enter the total flight duration.\n\nPlease try again.")
        airport_info = airport_info_var.get()
        notes = notes_var.get()
        date = ''.join(e for e in date if e.isnumeric()
                       or e.isspace() or e in ['/'])
        airport_info = ''.join(e for e in airport_info if e.isalnum(
        ) or e.isspace() or e in ['!', '#', ',', '.', '?'])
        notes = ''.join(e for e in notes if e.isalnum()
                        or e.isspace() or e in ['!', '#', ',', '.', '?'])
        # insert data into table
        if not date:
            messagebox.showerror(
                'Date Missing Error', 'Please enter a date and try again.')
        else:
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
    except UnboundLocalError:
        pass
    except tk.TclError:
        messagebox.showerror(
            'Data Input Error', 'You are either missing values, or used illegal characters. If the value is 0, enter 0.\n\nTry again.')

# function to undo the latest entry in the log


def undo_last_entry():
    response_box = messagebox.askokcancel(
        "Delete Record", "Do you really want to delete the record(s)? This cannot be reversed.")
    if response_box:
        cursor.execute(
            '''DELETE FROM flight_data WHERE id = (SELECT MAX(id) FROM flight_data)''')
        connection.commit()
        display_data()
    else:
        pass


def display_data():
    # delete previous tree display
    for widget in data_frame.winfo_children():
        widget.destroy()

    # create new tree display
    tree = ttk.Treeview(data_frame, columns=(
        1, 2, 3, 4, 5, 6, 7, 8), show="headings", height=16)
    tree.grid(row=1, column=0, columnspan=8, padx=5, pady=5)

    # define tree headings
    tree.heading(1, text="Entry", anchor=tk.CENTER)
    tree.heading(2, text="Date", anchor=tk.CENTER)
    tree.heading(3, text="Number of Flights", anchor=tk.CENTER)
    tree.heading(4, text="Touch and Go's", anchor=tk.CENTER)
    tree.heading(5, text="Distance Flown (Miles)", anchor=tk.CENTER)
    tree.heading(6, text="Duration of Flight (Minutes)", anchor=tk.CENTER)
    tree.heading(7, text="Airport (Optional)", anchor=tk.CENTER)
    tree.heading(8, text="Notes", anchor=tk.CENTER)
    tree.bind('<Double-1>', lambda event: open_record_window(tree))

    # set column width
    tree.column(1, width=100, anchor=tk.CENTER)
    tree.column(2, width=75, anchor=tk.CENTER)
    tree.column(3, width=105, anchor=tk.CENTER)
    tree.column(4, width=100, anchor=tk.CENTER)
    tree.column(5, width=150, anchor=tk.CENTER)
    tree.column(6, width=175, anchor=tk.CENTER)
    tree.column(7, width=150, anchor=tk.CENTER)
    tree.column(8, width=500, anchor=tk.CENTER)

    # create tree rows
    cursor.execute('''SELECT * FROM flight_data ORDER BY id DESC''')
    data = cursor.fetchall()
    if data:
        for row in data:
            tree.insert("", tk.END, values=row, tags=('center',))
    else:
        tree.insert("", tk.END, values=[
                    "No data to display."]*8, tags=('center',))

    # set column alignment to center
    for column in range(8):
        tree.column(column, anchor=tk.CENTER)

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
        data_frame, text=f'Total Flights: {full_stop_landings_sum} | Total Distance Flown: {distance_flown_sum} miles | Total Duration of Flight: {duration_of_flight_sum} hrs')
    footer_label.grid(row=3, column=0, columnspan=8, padx=5, pady=5)

    # set row alignment to center
    tree.tag_configure('center', anchor=tk.CENTER)
    # create a function to delete rows

    def delete_row():
        response_box = messagebox.askokcancel(
            "Delete Record", "Do you really want to delete the record(s)? This cannot be reversed.")
        if response_box:
            selection = tree.selection()
            for item in selection:
                # get id of the row to be deleted
                row_id = tree.item(item)['values'][0]
                # remove row from tree view
                tree.delete(item)
                # delete row from database
                cursor.execute(
                    '''DELETE FROM flight_data WHERE id = ?''', (row_id,))
                connection.commit()
            display_data()
        else:
            pass

    # add delete button
    delete_button = ttk.Button(
        data_frame, text='Delete Record', command=delete_row)
    delete_button.grid(row=2, columnspan=8, pady=5, padx=5)

# function to close the database connection and exit the application


def close_app():
    connection.close()
    root.quit()


# create tkinter window
root = tk.Tk()
root.title('Paramotor Pilot Logbook')

# create data entry form
data_entry_frame = ttk.LabelFrame(root, text='Enter Flight Data')
data_entry_frame.grid(row=0, columnspan=2, padx=10, pady=10)

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
data_frame = ttk.LabelFrame(root, text='Flight Data')
data_frame.grid(row=1, column=0, padx=10, pady=10)

# display flight data in table
display_data()

# Save flight log as .csv file


def save_flight_log():
    cursor.execute('''SELECT * FROM flight_data''')
    data = cursor.fetchall()
    files = [('All Files', '*.*'),
             ('Comma Separated Value (CSV, .csv)', '*.csv')]
    header = ['Flight Number', 'Date', 'Full Stop Landings', "Touch and Go's",
              'Distance Flown', 'Duration of Flight (Minutes)', 'Airport (Optional)', 'Notes']
    file_path = fd.asksaveasfilename(filetypes=files, defaultextension=files)
    try:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for row in data:
                writer.writerow(row)
        path = file_path
        check_file = os.path.isfile(path)
        if check_file:
            messagebox.showinfo('File Saved', f"File saved as {file_path}.")
        else:
            messagebox.showerror(
                'File Save Error', f"An error occurred when saving {file_path}.")
    except FileNotFoundError:
        pass


# Import flight log from .csv file


def import_flight_log():
    files = [('Comma Separated Value (CSV, .csv)', '*.csv')]
    file_path = fd.askopenfilename(filetypes=files, defaultextension=files)
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cursor.execute('''INSERT INTO flight_data(date, full_stop_landings, touch_and_go, distance_flown, duration_of_flight, airport, notes)
                    VALUES(?,?,?,?,?,?,?)''', (row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        connection.commit()
    display_data()
# Show About popup


def show_about_popup():
    about_window = tk.Toplevel(root)
    about_window.title('About')
    about_window.iconbitmap('icons\\parachute.ico')
    about_window.resizable(False, False)
    about_window.geometry('350x275')
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
    about_text.grid(row=0, columnspan=6, padx=5, pady=5)


def show_help_popup():
    help_window = tk.Toplevel(root)
    help_window.title('Help')
    help_window.iconbitmap('icons\\parachute.ico')
    help_window.geometry('390x750')
    help_window.resizable(False, False)
    help_text_header = tk.Label(
        help_window, text='''
Paramotor Pilot Logbook Help Manual''', font=('Helvetica', 10, 'bold'))
    help_text_header.grid(row=0, columnspan=6, padx=5, pady=5)

    help_text = tk.Label(
        help_window, text='''
Making Flight Log Entries
----------------------------------------------------------------------
To make a flight log entry, enter the information for your flight 
as required in the "Enter Flight Data" section.

Paramotor Pilot Logbook logs an individual flight as one that has one
takeoff and one landing. A touch-and-go is logged as one takeoff and
one landing. For flights with a takeoff and one more more touch and
go's, the flight will add the amount of takeoffs and landings to the
total amount of touch and go's.

Removing Flight Log Entries
----------------------------------------------------------------------
There are two ways to remove an entry currently.Selecting the entry or
entries in the table, and clicking the Delete Record button will 
delete records. Alternatively, you can click the Edit menu -> 
"Remove Latest Entry" option in the menu. 

Flight Log Data
----------------------------------------------------------------------        
Flight logs are saved in a file called a 'SQLite3 database.' The ten 
most recent flights are shown in the interface. Additional flights are 
stored in the SQLite3 database.

Importing Log Data
----------------------------------------------------------------------
A boilerplate .CSV file is provided in the downloaded files that can
be used for uploading existing log data in bulk. Simply add your log
information, save, and then select File -> Import Log Data from the
interface, and select the .CSV file previously saved.        

Exporting Log Data
----------------------------------------------------------------------
To export your file as a .CSV file, click on File -> Save Flight Log,
and then specify the name and location to save the file to. 

Reporting Issues in Application
----------------------------------------------------------------------
This is a free and open source project, and is developed as a 
side-project. As such, some issues are simply impossible to discover 
during development and the developer's individual use.

Should you discover any issues, please file an issue on Github at
https://github.com/dievus/Paramotor-Pilot-Logbook.
        ''')
    # help_text.pack(padx=10, pady=10)
    help_text.grid(row=1, columnspan=6, padx=5, pady=5)


def ko_fi_sponsor_popup():
    ko_fi_window = tk.Toplevel(root)
    ko_fi_window.title('Sponsor This Project')
    ko_fi_window.iconbitmap('icons\\parachute.ico')
    ko_fi_window.resizable(False, False)
    ko_fi_window.geometry('380x425')
    qr_image = Image.open("images\\qr-code.png")
    qr_image = qr_image.resize((200, 200), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(qr_image)
    ko_fi_text = tk.Label(
        ko_fi_window, text='''
Sponsor my work through a Ko-Fi Donation
----------------------------------------------------------------------
While this project is provided free-of-charge, it does take time to 
develop and maintain. Should you wish to help sponsor the project, 
you can do so by scanning the QR code above, visiting the following 
link or by clicking the button below.
        
https://ko-fi.com/themayor
        
Thank you for your consideration!
        ''', image=photo, compound='top')
    ko_fi_text.image = photo
    ko_fi_text.grid(row=0, column=0, padx=5, pady=5)
    ko_fi_button = tk.Button(
        ko_fi_window, text='Sponsor This Project', command=sponsor_call_ko_fi, bd=1, justify='center')
    ko_fi_button.grid(row=1, columnspan=7)


# submit_btn.grid(row=7, column=0, columnspan=2, padx=5, pady=5)


def sponsor_call_ko_fi():
    webbrowser.open('https://ko-fi.com/themayor')



menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Save Flight Log', command=save_flight_log)
file_menu.add_command(label='Import Flight Log', command=import_flight_log)
file_menu.add_command(label='Exit', command=close_app)
menu_bar.add_cascade(label='File', menu=file_menu)
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label='Remove Latest Entry', command=undo_last_entry)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
sponsor_menu = tk.Menu(menu_bar, tearoff=0)
sponsor_menu.add_command(label='Sponsor This Project',
                         command=ko_fi_sponsor_popup)
menu_bar.add_cascade(label='Sponsor', menu=sponsor_menu)
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label='About', command=show_about_popup)
help_menu.add_command(label='Help', command=show_help_popup)
menu_bar.add_cascade(label='Help', menu=help_menu)

root.config(menu=menu_bar)
root.resizable(True, True)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.minsize(1200, 400)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.maxsize(width, height)
root.iconbitmap("icons\\parachute.ico")
root.mainloop()
