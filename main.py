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

    # clean data 
    for i in range(len(TEXTLIST)):
        if TEXTLIST[i][-1] == "\n":
            TEXTLIST[i] = TEXTLIST[i][:-1] 
        if '"' in TEXTLIST[i]:
            TEXTLIST[i] = TEXTLIST[i].split('"')
        else:
            TEXTLIST[i] = TEXTLIST[i].split(",")
        for j in range(len(TEXTLIST[i])):
            if TEXTLIST[i][j].isnumeric():
                TEXTLIST[i][j] = int(TEXTLIST[i][j])
            if TEXTLIST[i][j] == "NA" or TEXTLIST[i][j] == "":
                TEXTLIST[i][j] = None
    return TEXTLIST

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
        print(CONTENT)
        setup(CONTENT)
# PROCESSING # 

# OUPUTS # 