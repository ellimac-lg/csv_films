#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 16:14:32 2025

@author: clg
"""


# keys of a film dict
DESCRIPTORS = ["Titre", "Réalisateur", "Genre", "Année", "Note", "Studio"]
# unique field
KEY_FIELD = "Titre"
# fields that are integers
INT_FIELDS = ['Année']
# fields that floats
FLOAT_FIELDS = ['Note']

# all loaded films: title -> film dict
films_by_title = {}

# indices
# one index per descriptor
# descriptor -> description value -> list of title
films_by = {}


def read_films (file_name):
    "CSV reading and decoding, returns a list of film dicts"
    fd = open(file_name)
    films = []
    first_line= True
    header = []
    for line in fd:
        values = line.strip().split(";")
        if first_line : # header line
            header = values
            first_line = False
        else: # regular lines
            # building the film dict
            film = {}
            for item in zip (header,values):
                field = item[0].strip()
                value = item[1].strip()
                if field in INT_FIELDS:
                    film[field] = int(value)
                elif field in FLOAT_FIELDS:
                    film[field] = float(value.replace(',', '.'))
                else:
                    film[field] = value
            films.append(film)
    fd.close()
    return films

def by_descriptor(films_by_title, descriptor):
    "builds an index for a given descriptor"
    films_by_descriptor = {}
    for film in films_by_title.values():
        value = film[descriptor]
        if value not in films_by_descriptor:
            films_by_descriptor[value] = []
        films_by_descriptor[value].append(film[KEY_FIELD])
    return dict(sorted(films_by_descriptor.items()))


def load_films(filenames):
    "reads CSV files, store films in films_by_title and builds the indices films_by"
    global films_by_title
    global films_by
    
    # reading files
    films = []
    for filename in filenames:
        films += read_films(filename)
        
    # building films_by_title
    films_by_title = {}
    for film in films:
        films_by_title[film[KEY_FIELD]] = film
    films_by_title = dict(sorted(films_by_title.items()))
    
    # building indices for every descriptor (except title)
    films_by = {}
    for descriptor in DESCRIPTORS:
        if descriptor != KEY_FIELD:
            films_by[descriptor] = by_descriptor(films_by_title, descriptor)

#%%

#load_films(["films1.csv", "films2.csv"])

#import json
#with open("films_by_title.json", 'w') as fd:
#    json.dump(films_by_title, fd)
 
#with open("films_by.json", 'w') as fd:
#    json.dump(films_by, fd)
    
#%%
    
def search_by(descriptor, value):
    "search in indices with exact match, returns a list of film dicts"
    global films_by_title
    global films_by
    if value not in films_by[descriptor]:
        return []
    films = []
    for title in films_by[descriptor][value]:
        films.append(films_by_title[title])
    return films

def search_compare(descriptor, value, greater=True):
    "search in indices with >= or <= comparison, returns a list of films dicts"
    global films_by_title
    global films_by
    if (descriptor not in INT_FIELDS) and (descriptor not in FLOAT_FIELDS):
        raise ValueError(f"pas de recherche compartive possible sur le champs {descriptor}")
    titles = []
    films_by_descriptor = films_by[descriptor]
    for key in films_by_descriptor:
        if (greater and (key >= value)) or (not greater and (key <= value)):
            titles += films_by_descriptor[key] 
    # converting titles to film dicts
    films = []
    for title in titles:
        films.append(films_by_title[title])
    return films


def search_contains(descriptor, value):
    "search in indices with match of partial string"
    searched_val = value.casefold() 
    if descriptor == KEY_FIELD: # for title we look into films_by_title keys
        results = []
        for title in films_by_title:
            if searched_val in title.casefold():
                results.append(films_by_title[title])
        return results
    else: # for other descriptors we look at the corresponding index key
        films_by_descriptor = films_by[descriptor]
        titles = []
        for key in films_by[descriptor]: 
            if searched_val in key.casefold(): # partial string match
                titles += films_by_descriptor[key] 
        # converting titles to film dicts
        films = []
        for title in titles:
            films.append(films_by_title[title])
        return films
        

#%%
#import pprint
#pprint.pprint(films_by)

#%%

#for film in search_by(films_by_title, films_by, 'Note', 9):
#    print(film)
    
#%%

#for film in search_compare(films_by_title, films_by, 'Note', 9, True):
#    print(film)
