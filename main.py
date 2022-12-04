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

def checkInt(VALUE, MINVALUE=0, MAXVALUE=5000):
    """
    checks if the value is a valid integer
    """
    try:
        VALUE = int(VALUE)
        if VALUE > MAXVALUE or VALUE < MINVALUE:
            print("Please input a valid number within the range! ")
            NEWVALUE = input("> ")
            return checkInt(NEWVALUE, MINVALUE, MAXVALUE)
        return VALUE
    except ValueError:
        print("Please input a valid number! ")
        NEWVALUE = input("> ")
        return checkInt(NEWVALUE, MINVALUE, MAXVALUE)
    
def checkValue(VALUE, CORRECTVALUE1="", CORRECTVALUE2="", CORRECTVALUE3="", CORRECTVALUE4=""):
    """
    checks if a string has the correct value 
    :param VALUE: str
    :param CORRECTVALUE1: str
    :param CORRECTVALUE2: str
    :param CORRECTVALUE3: str
    :return: str
    """
    if VALUE is not CORRECTVALUE1 or VALUE is not CORRECTVALUE2 or VALUE is not CORRECTVALUE3 or VALUE is not CORRECTVALUE4:
        print("Please input a correct value into the database! ")
        NEWVALUE = input("> ")
        return checkValue(NEWVALUE, CORRECTVALUE1, CORRECTVALUE2, CORRECTVALUE3)
    else:
        return VALUE


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
        if '"' in TEXTLIST[i]: # search for a quotation mark 
            TEXTLIST[i] = TEXTLIST[i].split('"') # split at the quotation so there are 3 nodes
            NEWLIST.append(TEXTLIST[i][0]) # add the first node into the empty array
            NEWLIST[i] = NEWLIST[i].split(",") # split the first node at commas so its a 2d array
            NEWLIST[i].pop(-1) # from the list that has the first 
            NEWLIST[i].append(TEXTLIST[i][1]) # add the second node (the quotations) 
            TEXTLIST[i][2] = TEXTLIST[i][2].split(",")
            NEWLIST[i].append(TEXTLIST[i][2][1])
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
    CHOICE = checkInt(CHOICE, 1, 4)
    return CHOICE

def getTimespan() -> int:
    """
    user inputs start and end years 
    :return: STARTYEAR int, ENDYEAR int
    """
    global CURSOR
    MINVALUE = CURSOR.execute("""
    SELECT
        population_year
    FROM
        large_mammals
    ORDER BY
        population_year ASC;
    """).fetchone()
    MAXVALUE = CURSOR.execute("""
    SELECT
        population_year
    FROM
        large_mammals
    ORDER BY
        population_year DESC;
    """).fetchall()
    STARTYEAR = input("What is the starting year? ")
    STARTYEAR = checkInt(STARTYEAR, MINVALUE[0], MAXVALUE[1][0])
    ENDYEAR = input("What is the end year? ")
    ENDYEAR = checkInt(ENDYEAR, MINVALUE[0], MAXVALUE[1][0])
    return STARTYEAR, ENDYEAR

def getSpecies() -> int:
    """
    user selects species of animal
    :return: int
    """
    SPECIES = input("What species are you searching for, Bison (1), Elk (2), Moose (3), Deer (4) or All (5)? ")
    SPECIES = checkInt(SPECIES, 1, 5)
    return SPECIES

def addNewData():
    """
    user adds new year data to the database 
    :return: None
    """
    global CURSOR, CONNECTION
    AREA = input("Area of park: ")
    AREA = checkValue(AREA, "North", "South") # need to make it not "" or null
    POPULATIONYEAR = input("Population year: ")
    POPULATIONYEAR = checkInt(POPULATIONYEAR, 1000)
    SURVEYYEAR = input("Survey year: ")
    SURVEYYEAR = checkInt(SURVEYYEAR, 1000) # need to also allow for null
    SURVEYMONTH = input("Survey month: ")
    SURVEYMONTH = checkInt(SURVEYMONTH, 1, 12) # need to also allow for null
    SURVEYDAY = input("Survey day: ")
    SURVEYDAY = checkInt(SURVEYDAY, 1, 31) # need to also allow for null
    SPECIESNAME = input("Species name: ")
    SPECIESNAME = checkValue(SPECIESNAME, "Elk", "Bison", "Deer", "Moose") # need to make it not "" or null
    UNKNOWNAGESEX = input("Unknown age and sex count: ")
    UNKNOWNAGESEX = checkInt(UNKNOWNAGESEX, 0) # need to also allow for null
    ADULTMALE = input("Adult male count: ")
    ADULTMALE = checkInt(ADULTMALE, 0) # need to also allow for null
    ADULTFEMALE = input("Adult female count: ")
    ADULTFEMALE = checkInt(ADULTFEMALE, 0) # need to also allow for null
    ADULTUNKNOWN = input("Adult unknown count: ")
    ADULTUNKNOWN = checkInt(ADULTUNKNOWN, 0) # need to also allow for null
    YEARLING = input("Yearling count: ")
    YEARLING = checkInt(YEARLING, 0) # need to also allow for null
    CALF = input("Calf count: ")
    CALF = checkInt(CALF, 0) # need to also allow for null
    SURVEYTOTAL = input("Survey total: ")
    SURVEYTOTAL = checkInt(SURVEYTOTAL, 0) # need to also allow for null
    SIGHTABILITY = input("Sightability correction factor: ")
    SIGHTABILITY = checkInt(SIGHTABILITY, 0) # need to also allow for null
    CAPTIVE = input("Additional captive count: ")
    CAPTIVE = checkInt(CAPTIVE, 0) # need to also allow for null
    ANIMALSREMOVED = input("Animals removed prior to survey: ")
    ANIMALSREMOVED = checkInt(ANIMALSREMOVED, 0)
    POPULATIONESTIMATE = input("Fall population estimate: ")
    POPULATIONESTIMATE = checkInt(POPULATIONESTIMATE, 0)
    SURVEYCOMMENT = input("Survey comment: ") # this one can be anything
    ESTIMATEMETHOD = input("Estimate method: ")
    ESTIMATEMETHOD = checkValue(ESTIMATEMETHOD, "Ground", "Aerial") # need to make it not "" or null
    NEWDATA = [AREA, POPULATIONYEAR, SURVEYYEAR, SURVEYMONTH, SURVEYDAY, SPECIESNAME, UNKNOWNAGESEX, ADULTMALE, ADULTFEMALE, ADULTUNKNOWN, YEARLING, CALF, SURVEYTOTAL, SIGHTABILITY, CAPTIVE, ANIMALSREMOVED, POPULATIONESTIMATE, SURVEYCOMMENT, ESTIMATEMETHOD]

    # insert into database 
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
    """, NEWDATA)

    CONNECTION.commit()

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

def searchYear(YEAR, SPECIES) -> int:
    """
    searches the database for the total population of the species during that year
    :param STARTYEAR: int
    :param SPECIES: int 
    :return: int
    """
    global CURSOR
    # need to add north & south populations together 
    BISON = 0 
    ELK = 0 
    MOOSE = 0
    DEER = 0 
    DEERLIST = CURSOR.execute(f"""
            SELECT
                fall_population_estimate
            FROM
                large_mammals
            WHERE
                population_year = {YEAR}
            AND
                (species_name = "deer" 
            OR
                species_name = "Deer");
        """).fetchall()
    for i in range(len(DEERLIST)): # add north to south
        for j in range(len(DEERLIST[i])):
            DEER = DEERLIST[i][j] + DEER
    BISONLIST = CURSOR.execute(f"""
            SELECT
                fall_population_estimate
            FROM
                large_mammals
            WHERE
                population_year = {YEAR}
            AND
                (species_name = "bison" 
            OR
                species_name = "Bison");
        """).fetchall()
    for i in range(len(BISONLIST)):
        for j in range(len(BISONLIST[i])):
            BISON = BISONLIST[i][j] + BISON
    ELKLIST = CURSOR.execute(f"""
            SELECT
                fall_population_estimate
            FROM
                large_mammals
            WHERE
                population_year = {YEAR}
            AND
                (species_name = "elk" 
            OR
                species_name = "Elk");
        """).fetchall()
    for i in range(len(ELKLIST)):
        for j in range(len(ELKLIST[i])):
            ELK = ELKLIST[i][j] + ELK
    MOOSELIST = CURSOR.execute(f"""
            SELECT
                fall_population_estimate
            FROM
                large_mammals
            WHERE
                population_year = {YEAR}
            AND
                (species_name = "moose" 
            OR
                species_name = "Moose");
        """).fetchall()
    for i in range(len(MOOSELIST)):
        for j in range(len(MOOSELIST[i])):
            MOOSE = MOOSELIST[i][j] + MOOSE
    if SPECIES == 1: # bison
        return BISON
    elif SPECIES == 2: # elk 
        return ELK
    elif SPECIES == 3: # moose 
        return MOOSE
    elif SPECIES == 4: # deer 
        return DEER
    elif SPECIES == 5: # all 
        ALL = BISON + ELK + MOOSE + DEER
        return ALL

def calculateGrowth(STARTPOPULATION, ENDPOPULATION, STARTYEAR, ENDYEAR) -> int:
    """
    calculate population growth 
    :param STARTPOPULATION: int
    :param ENDPOPULATION: int
    :param STARTYEAR: int 
    :param ENDYEAR: int
    :return: int
    """
    POPULATION = ENDPOPULATION - STARTPOPULATION
    TIME = ENDYEAR - STARTYEAR
    GROWTH = POPULATION / TIME
    return GROWTH

# OUTPUTS #

def displayGrowth(GROWTH, STARTYEAR, ENDYEAR, SPECIES) -> None:
    """
    prints out the population growth per year
    :param GROWTH: int
    :return: None
    """
    if SPECIES == 1: 
        ANIMAL = "bison"
    elif SPECIES == 2: 
        ANIMAL = "elk"
    elif SPECIES == 3: 
        ANIMAL = "moose"
    elif SPECIES == 4:
        ANIMAL == "deer"
    
    if SPECIES < 5:
        print(f"The growth rate of {ANIMAL.title()} between {STARTYEAR} and {ENDYEAR} is {round(GROWTH, 2)} {ANIMAL.title()}/year. ")
    elif SPECIES == 5:
        print(f"The growth rate of all animals between {STARTYEAR} and {ENDYEAR} is {round(GROWTH, 2)} animals/year. ")
    return

### MAIN PROGRAM CODE ###
if __name__ == "__main__":
# INPUTS #
    if FIRSTRUN:
        CONTENT = extractFile("Elk_Island_NP_Grassland_Forest_Ungulate_Population_1906-2017_data_reg.csv")
        setup(CONTENT)
    startScreen()
    CHOICE = menu()
# PROCESSING # 
    if CHOICE == 1:
        # INPUTS #
        STARTYEAR, ENDYEAR = getTimespan()
        SPECIES = getSpecies()
        # PROCESSING #
        STARTPOPULATION = searchYear(STARTYEAR, SPECIES)
        ENDPOPULATION = searchYear(ENDYEAR, SPECIES)
        GROWTH = calculateGrowth(STARTPOPULATION, ENDPOPULATION, STARTYEAR, ENDYEAR)
        # OUTPUTS # 
        displayGrowth(GROWTH, STARTYEAR, ENDYEAR, SPECIES)
    elif CHOICE == 2:
        pass
    elif CHOICE == 3:
        pass
# OUTPUTS # 
    elif CHOICE == 4:
        exit()