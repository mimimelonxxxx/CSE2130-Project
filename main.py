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
        TEXTLIST[i] = TEXTLIST[i].split(",")
        # if TEXTLIST[i] ends with " then join with the column before it
        for j in range(len(TEXTLIST[i])):
            if TEXTLIST[i][j].isnumeric():
                TEXTLIST[i][j] = int(TEXTLIST[i][j])
            if TEXTLIST[i][j] == "NA" or TEXTLIST[i][j] == "":
                TEXTLIST[i][j] = 0
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
                area_of_park TEXT,
                population_year,
                survey_year,
                survey_month,
                survey_day,
                species_name,
                unknown_age_and_sex,
                adult_male_count,
                adult_female_count,
                adult_unknown_count,
                yearling_count,
                calf_count,
                survey_total,
                sightability_correction_factor,
                additional_captive_count,
                animals_removed_prior_to_survey,
                fall_population_estimate,
                survey_comment,
                estimate_method
        );
    """) # composite key from area_of_part and population_year and species_name

    for i in range(len(CONTENT)):
        CURSOR.execute("""
            INSERT INTO
                large_mammals
            VALUES (
                    area_of_park = ?,
                    population_year = ?,
                    survey_year = ?,
                    survey_month = ?,
                    survey_day = ?,
                    species_name = ?,
                    unknown_age_and_sex = ?,
                    adult_male_count = ?,
                    adult_female_count = ?,
                    adult_unknown_count = ?,
                    yearling_count = ?,
                    calf_count = ?,
                    survey_total = ?,
                    sightability_correction_factor = ?,
                    additional_captive_count = ?,
                    animals_removed_prior_to_survey = ?,
                    fall_population_estimate = ?,
                    survey_comment = ?,
                    estimate_method = ?
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