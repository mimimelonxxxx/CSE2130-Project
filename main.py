"""
title: Large Mammal Population Calculator
author: Michelle Jiang
date-created: 2022-11-25
"""

# Most of the time will be spent manipulating the data
# Must manipulate the data with code, not editing the txt file
# for add new year data, should have user be able to input data for every column in the database 
# only need to query the database and add new columns, don't need to edit data 
# commas exist in comments so you need to edit the data before splitting by commas 
# don't actually need to normalize 

### VARIABLES ### 
import sqlite3
import pathlib
DATABASEFILE = "large mammal population.db"

FIRSTRUN = True 
if (pathlib.Path.cwd() / DATABASEFILE).exists():
    FIRSTRUN = False

CONNECTION = sqlite3.connect(DATABASEFILE)
CURSOR = CONNECTION.cursor()
### FUNCTIONS ### 

# INPUTS # 

def checkInt(VALUE, MAXVALUE):
    """
    checks if the value is a valid integer
    """
    try:
        int(VALUE)
        if VALUE > MAXVALUE:
            print("Please input a valid number! ")
    except ValueError:
        print("Please input a valid number! ")

def extractFile(FILENAME) -> list:
    """
    extract file content and puts it into the database 
    :param FILENAME: str
    :return: list
    """

    # get file content
    FILE = open(FILENAME)
    TEXTLIST = FILE.readlines()
    FILE = FILE.close()

    NEWLIST = []
    # clean data 
    for i in range(len(TEXTLIST)):
        if TEXTLIST[i][-1] == "\n":
            TEXTLIST[i] = TEXTLIST[i][:-1] 
        if '"' in TEXTLIST[i+1]:
            TEXTLIST[i] = TEXTLIST[i].split('"') # split at the quotation so there are 3 nodes
            TEXTLIST[i][0] = TEXTLIST[i][0].split(",") # split the first node at commas so its a 2d array
            NEWLIST.append(TEXTLIST[i][0]) # add the first node into the empty array
            print(NEWLIST[i+1])
            NEWLIST[i].pop(-1)  
            NEWLIST[i].append(TEXTLIST[i][1]) # man fuck this 
            TEXTLIST[i][2] = TEXTLIST[i][2].split(",")
            NEWLIST[i].append(TEXTLIST[i][2][1])
            print(NEWLIST[i])
        else:
            TEXTLIST[i] = TEXTLIST[i].split(",")
            NEWLIST.append(TEXTLIST[i])
        for j in range(len(NEWLIST[i])):
            if NEWLIST[i][j].isnumeric():
                NEWLIST[i][j] = int(NEWLIST[i][j])
            if NEWLIST[i][j] == "NA" or NEWLIST[i][j] == "":
                NEWLIST[i][j] = None
    return NEWLIST

def startScreen() -> None:
    """
    displays starting text
    :return: None
    """
    print("Welcome to Elk Island National Park Large Mammal population database! ")

def menu() -> int:
    """
    user selects options 
    :return: int
    """
    print("""
Please choose an option:
    1. Search Population Growth
    2. Add new year data
    3. <New Function!>
    4. Exit
    """)
    CHOICE = input("> ")
    CHOICE = checkInt(CHOICE, 4)
    return CHOICE

# PROCESSING # 

def setup(CONTENT) -> None:
    """
    creates the database file on first run 
    :param CONTENT: list
    :return: None
    """
    global CURSOR, CONNECTION

    CURSOR.execute("""
        CREATE TABLE
            large_mammals (
                area_of_park TEXT NOT NULL,
                population_year INTEGER NOT NULL,
                survey_year INTEGER,
                survey_month INTEGER,
                survey_day INTEGER,
                species_name TEXT NOT NULL,
                unknown_age_and_sex INTEGER,
                adult_male_count INTEGER,
                adult_female_count INTEGER,
                adult_unknown_count INTEGER,
                yearling_count INTEGER,
                calf_count INTEGER,
                survey_total INTEGER,
                sightability_correction_factor INTEGER,
                additional_captive_count INTEGER,
                animals_removed_prior_to_survey INTEGER,
                fall_population_estimate INTEGER,
                survey_comment TEXT,
                estimate_method TEXT,
                PRIMARY KEY (area_of_park, population_year, species_name)
        );
    """) # composite key from area_of_park and population_year and species_name

    for i in range(len(CONTENT)):
        CURSOR.execute("""
            INSERT INTO
                large_mammals
            VALUES (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
            );
        """, CONTENT[i])

    CONNECTION.commit()

# OUTPUTS #

### MAIN PROGRAM CODE ###
if __name__ == "__main__":
# INPUTS #
    if FIRSTRUN:
        CONTENT = extractFile("Elk_Island_NP_Grassland_Forest_Ungulate_Population_1906-2017_data_reg.csv")
        setup(CONTENT)
    startScreen()
    CHOICE = menu()
# PROCESSING # 

# OUPUTS # 