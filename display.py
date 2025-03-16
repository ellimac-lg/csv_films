#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 14:23:11 2025

@author: glg
"""

import csv_films
from tkinter import Tk, ttk, StringVar, Canvas, END, VERTICAL

HEADER = csv_films.DESCRIPTORS
CELL_SIZES = [50, 30, 10, 5, 5, 30]
FILM_HEIGHT = 500



def upload_films(*args):
    "upload films from files and display them"
    print(f"upload_films file1: {file1.get()} file2: {file2.get()}")
    filenames = []
    if file1.get() != "":
        filenames.append(file1.get())
    if file2.get() != "":
        filenames.append(file2.get())
    csv_films.load_films(filenames)
    criteria_change()

def display_films(*args):
    "search for films and display them"

    print(f"display_films with criteria: {criteria_var.get()} cmp: {cmp_var.get()} value: {value_var.get()} ")

    # rebuild content of film canvas
    global film_canvas
    if criteria_var.get() in csv_films.INT_FIELDS:
        val = int(value_var.get())
    elif criteria_var.get() in csv_films.FLOAT_FIELDS:
        val = float(value_var.get())
    else: 
        val = val = value_var.get()
    if (criteria_var.get() == "")  or (val == ""):
        films = csv_films.films_by_title.values()
    elif cmp_var.get() == "contient":
        films = csv_films.search_contains(criteria_var.get(), val)
    elif cmp_var.get() in ["=", ">=", "<="]:
        if cmp_var.get() == "=":    
            films = csv_films.search_by(criteria_var.get(), val)
        else:
            cmp_op = True if cmp_var.get() == ">=" else False
            films = csv_films.search_compare(criteria_var.get(), val, cmp_op)
    film_frame = ttk.Frame(film_canvas)
    film_frame.grid(column=0, row=0, sticky="NEWS")
    film_frame.bind("<Configure>", lambda e: film_canvas.configure(scrollregion=film_canvas.bbox("all")))
    for i, film in enumerate(films):
        for j, descriptor in enumerate(HEADER):
            val = film[descriptor]
            entry = ttk.Entry(film_frame, width=CELL_SIZES[j])
            entry.grid(column=j, row=i)
            entry.insert(END, val)

    film_canvas.delete("all")
    film_canvas.create_window((0, 0), window=film_frame, anchor="nw")


    
def criteria_change(*args):
    "when the criteria is modified we change the other search menus'options"
    if criteria_var.get() == "":
        value['values'] = ("",)
        value.current(0)
        cmp['values'] = ("",)
        cmp.current(0)
    elif (criteria_var.get() in csv_films.INT_FIELDS) or (criteria_var.get() in csv_films.FLOAT_FIELDS):
        cmp['values'] = ("=", ">=", "<=")
        cmp.current(0)
        value['values'] = ("",)
        value.current(0)
    else:
        if criteria_var.get() == "Titre":
            cmp['values'] = ("contient", "=")
            cmp.current(0)            
            value['values'] = ("",)
            value.current(0)
        else:
            cmp['values'] = ("=", "contient")
            cmp.current(0)            
            possible_values = csv_films.films_by[criteria_var.get()].keys()
            value['values'] = [""] + list(possible_values)
            value.current(0)
        
    display_films()
    
    


# create main window
root = Tk()
root.title("Recherche de films")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# create the main frame
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky="NEWS")

# file 1
ttk.Label(mainframe, text="fichier 1").grid(column=0, row=0, sticky="W")
file1 = StringVar()
file1_entry = ttk.Entry(mainframe, width=7, textvariable=file1)
file1_entry.grid(column=0, row=1, sticky="WE")
file1_entry.bind('<Return>', upload_films)
file1_entry.insert(END, "films1.csv")

# file 2
ttk.Label(mainframe, text="fichier 2").grid(column=1, row=0, sticky="W")
file2 = StringVar()
file2_entry = ttk.Entry(mainframe, width=7, textvariable=file2)
file2_entry.grid(column=1, row=1, sticky="WE")
file1_entry.bind('<Return>', upload_films)
file2_entry.insert(END, "films2.csv")

# Upload button
upload_button = ttk.Button(mainframe, text="Upload", command=upload_films)
upload_button.grid(column=2, row=1, sticky="W")
upload_button.bind('<Return>', upload_films)

# criteria
ttk.Label(mainframe, text="Critère").grid(column=0, row=2, sticky="W")
criteria_var = StringVar()
criteria = ttk.Combobox(mainframe, textvariable=criteria_var)
criteria.grid(column=0, row=3, sticky="WE")
criteria.bind('<<ComboboxSelected>>', criteria_change)
criteria.state(["readonly"])
criteria['values'] = ('', *HEADER)
criteria.current(0)

# comparison
ttk.Label(mainframe, text="").grid(column=1, row=2, sticky="W")
cmp_var = StringVar()
cmp = ttk.Combobox(mainframe, textvariable=cmp_var)
cmp.grid(column=1, row=3, sticky="WE")
cmp.bind('<<ComboboxSelected>>', display_films)
cmp.state(["readonly"])
cmp['values'] = ('',) # to do : get values from loaded files
cmp.current(0)

# value
ttk.Label(mainframe, text="Valeur").grid(column=2, row=2, sticky="W")
value_var = StringVar()
value = ttk.Combobox(mainframe, textvariable=value_var)
value.bind('<<ComboboxSelected>>', display_films)
value.grid(column=2, row=3, sticky="WE")
value.bind('<Return>', display_films)

# adding padding to all previous widgets
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

# create the sub frame to put the header and the film frame
table_frame = ttk.Frame(mainframe)
table_frame.grid(column=0, row=4, columnspan=len(HEADER),  sticky="WE")

# create the header
for j, val in enumerate(HEADER):
    entry = ttk.Entry(table_frame, width=CELL_SIZES[j])
    entry.grid(column=j, row=0, sticky="WE")
    entry.insert(END, val)

# create empty scrollable canvas (to be filled with films in display_films)
film_canvas = Canvas(table_frame, height=FILM_HEIGHT)
film_canvas.grid(column=0, row=1, columnspan=len(HEADER),  sticky="WE")

# scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL)
scrollbar.grid(column=len(HEADER), row=1, sticky="NS")
scrollbar['command'] = film_canvas.yview
film_canvas['yscrollcommand'] = scrollbar.set

# focus on one element
upload_button.focus()

# launch the main loop
root.mainloop()

