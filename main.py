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

def checkInt(VALUE, MINVALUE=0, MAXVALUE=5000, NULLNESS=False) -> int:
    """
    checks if the value is a valid integer
    :param VALUE: str
    :param MINVALUE: int
    :param MAXVALUE: int
    :param NULLNESS: bool
    :return: int
    """
    if NULLNESS:
        if VALUE == None or VALUE == "":
            VALUE = None
            return VALUE
        else:
            try:
                VALUE = int(VALUE)
                if VALUE > MAXVALUE or VALUE < MINVALUE:
                    print("Please input a valid number within the range! ")
                    NEWVALUE = input("> ")
                    return checkInt(NEWVALUE, MINVALUE, MAXVALUE, NULLNESS)
                return VALUE
            except ValueError:
                print("Please input a valid number! ")
                NEWVALUE = input("> ")
                return checkInt(NEWVALUE, MINVALUE, MAXVALUE, NULLNESS)
    else:
        try:
            VALUE = int(VALUE)
            if VALUE > MAXVALUE or VALUE < MINVALUE:
                print("Please input a valid number within the range! ")
                NEWVALUE = input("> ")
                return checkInt(NEWVALUE, MINVALUE, MAXVALUE, NULLNESS)
            return VALUE
        except ValueError:
            print("Please input a valid number! ")
            NEWVALUE = input("> ")
            return checkInt(NEWVALUE, MINVALUE, MAXVALUE, NULLNESS)
    
def checkYear(VALUE):
    """
    checks if the year is in the list and converts the year into int
    :param VALUE: str 
    :return: int
    """
    global CURSOR
    YEARS = CURSOR.execute(f"""
        SELECT
            population_year
        FROM
            large_mammals
        WHERE
            population_year = ?
    """, [VALUE]).fetchall()
    if VALUE.isnumeric():
        VALUE = int(VALUE)
        if len(YEARS) == 0:
            print("Please input a valid year within the database! ")
            NEWVALUE = input("> ")
            return checkYear(NEWVALUE)
        else:
            return VALUE
    else:
        print("Please input a valid number! ")
        NEWVALUE = input("> ")
        return checkYear(NEWVALUE)

def checkValue(VALUE, STATEMENTNUMBER, CORRECTVALUE1, CORRECTVALUE2, CORRECTVALUE3="", CORRECTVALUE4="") -> str:
    """
    checks if a string has the correct value 
    :param VALUE: str
    :param STATEMENTNUMBER: int
    :param CORRECTVALUE1: str
    :param CORRECTVALUE2: str
    :param CORRECTVALUE3: str
    :return: str
    """
    if STATEMENTNUMBER == 2:
        if (not VALUE == CORRECTVALUE1) and (not VALUE == CORRECTVALUE2):
            print("Please input a correct value into the database! ")
            NEWVALUE = input("> ")
            return checkValue(NEWVALUE, 2, CORRECTVALUE1, CORRECTVALUE2)
        else:
            return VALUE
    elif STATEMENTNUMBER == 4:
        if (not VALUE == CORRECTVALUE1) and (not VALUE == CORRECTVALUE2) and (not VALUE == CORRECTVALUE3) and (not VALUE == CORRECTVALUE4):
            print("Please input a correct value into the database! ")
            NEWVALUE = input("> ")
            return checkValue(NEWVALUE, 4, CORRECTVALUE1, CORRECTVALUE2, CORRECTVALUE3, CORRECTVALUE4)
        else:
            return VALUE

def checkComment(COMMENT):
    """
    checks the survey comment for quotation marks
    :param COMMENT: str
    :return: str
    """
    COMMENTLIST = COMMENT.split('"')
    if COMMENTLIST[0] == "" and COMMENTLIST[-1] == "":
        return COMMENT
    elif COMMENT == "":
        COMMENT = None
        return COMMENT
    else:
        print("Please include quotation marks around the survey comment! ")
        NEWCOMMENT = input("Survey comment: ")
        return checkComment(NEWCOMMENT)

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
    3. Search for specific age or sex data
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
    STARTYEAR = input("What is the starting year? ")
    STARTYEAR = checkYear(STARTYEAR)
    ENDYEAR = input("What is the end year? ")
    ENDYEAR = checkYear(ENDYEAR)
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

    # INPUTS # 
    AREA = input("Area of park: ")
    AREA = checkValue(AREA, 2, "North", "South")
    POPULATIONYEAR = input("Population year: ")
    POPULATIONYEAR = checkInt(POPULATIONYEAR, 1000)
    SURVEYYEAR = input("Survey year: ")
    SURVEYYEAR = checkInt(SURVEYYEAR, 1000, 5000, True) 
    SURVEYMONTH = input("Survey month: ")
    SURVEYMONTH = checkInt(SURVEYMONTH, 1, 12, True)
    SURVEYDAY = input("Survey day: ")
    SURVEYDAY = checkInt(SURVEYDAY, 1, 31, True) 
    SPECIESNAME = input("Species name: ")
    SPECIESNAME = checkValue(SPECIESNAME, 4, "Elk", "Bison", "Deer", "Moose") 
    UNKNOWNAGESEX = input("Unknown age and sex count: ")
    UNKNOWNAGESEX = checkInt(UNKNOWNAGESEX, 0, 5000, True)
    ADULTMALE = input("Adult male count: ")
    ADULTMALE = checkInt(ADULTMALE, 0, 5000, True) 
    ADULTFEMALE = input("Adult female count: ")
    ADULTFEMALE = checkInt(ADULTFEMALE, 0, 5000, True) 
    ADULTUNKNOWN = input("Adult unknown count: ")
    ADULTUNKNOWN = checkInt(ADULTUNKNOWN, 0, 5000, True)
    YEARLING = input("Yearling count: ")
    YEARLING = checkInt(YEARLING, 0, 5000, True) 
    CALF = input("Calf count: ")
    CALF = checkInt(CALF, 0, 5000, True) 
    SURVEYTOTAL = input("Survey total: ")
    SURVEYTOTAL = checkInt(SURVEYTOTAL, 0, 5000, True)
    SIGHTABILITY = input("Sightability correction factor: ")
    SIGHTABILITY = checkInt(SIGHTABILITY, 0, 5000, True) 
    CAPTIVE = input("Additional captive count: ")
    CAPTIVE = checkInt(CAPTIVE, 0, 5000, True)
    ANIMALSREMOVED = input("Animals removed prior to survey: ")
    ANIMALSREMOVED = checkInt(ANIMALSREMOVED, 0, 5000, True)
    POPULATIONESTIMATE = input("Fall population estimate: ")
    POPULATIONESTIMATE = checkInt(POPULATIONESTIMATE, 0)
    SURVEYCOMMENT = input("Survey comment: ") 
    SURVEYCOMMENT = checkComment(SURVEYCOMMENT)
    ESTIMATEMETHOD = input("Estimate method: ")
    ESTIMATEMETHOD = checkValue(ESTIMATEMETHOD, 2, "Ground", "Aerial") 
    NEWDATA = [AREA, POPULATIONYEAR, SURVEYYEAR, SURVEYMONTH, SURVEYDAY, SPECIESNAME, UNKNOWNAGESEX, ADULTMALE, ADULTFEMALE, ADULTUNKNOWN, YEARLING, CALF, SURVEYTOTAL, SIGHTABILITY, CAPTIVE, ANIMALSREMOVED, POPULATIONESTIMATE, SURVEYCOMMENT, ESTIMATEMETHOD]

    # PROCESSING # 
    # insert into database 
    try:
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
    except sqlite3.IntegrityError:
        print("Please input valid, unique values into the database! ")
        return addNewData()
    CONNECTION.commit()

    # OUTPUTS # 
    print("Data has been added into the database! ")

def selectData() -> int:
    """
    user selects which option to search for
    :return: int
    """
    print("""
Please select which option to search for:
    1. Unknown age and sex count 
    2. Adult male count 
    3. Adult female count
    4. Adult unknown count
    5. Yearling count
    6. Calf count
    """)
    CHOICE = input("> ")
    CHOICE = checkInt(CHOICE, 1, 6)
    return CHOICE

def selectYear() -> int:
    """
    user selects year from database 
    :return: int
    """
    YEAR = input("What is the year to search from? ")
    YEAR = checkYear(YEAR)
    return YEAR

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
                estimate_method TEXT NOT NULL,
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

def searchData(DATA, YEAR) -> int:
    """
    searches database for selected data from selected year
    :param DATA: int
    :param YEAR: int 
    :return: int 
    """
    global CURSOR
    if DATA == 1:
        DATA = "unknown_age_and_sex"
    elif DATA == 2:
        DATA = "adult_male_count"
    elif DATA == 3:
        DATA = "adult_female_count"
    elif DATA == 4:
        DATA = "adult_unknown_count"
    elif DATA == 5:
        DATA = "yearling_count"
    elif DATA == 6: 
        DATA = "calf_count"

    POPULATION = 0 

    DATALIST = CURSOR.execute(f"""
        SELECT
            {DATA}
        FROM
            large_mammals
        WHERE
            population_year = {YEAR}
    """).fetchall()
    for i in range(len(DATALIST)):
        for j in range(len(DATALIST[i])):
            if DATALIST[i][j] == None:
                DATALIST[i][j] = 0
            POPULATION = DATALIST[i][j] + POPULATION
    return POPULATION

# OUTPUTS #

def displayGrowth(GROWTH, STARTYEAR, ENDYEAR, SPECIES) -> None:
    """
    displays the population growth per year
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
        ANIMAL = "deer"
    
    if SPECIES < 5:
        print(f"The growth rate of {ANIMAL.title()} between {STARTYEAR} and {ENDYEAR} is {round(GROWTH, 2)} {ANIMAL.title()}/year. ")
    elif SPECIES == 5:
        print(f"The growth rate of all animals between {STARTYEAR} and {ENDYEAR} is {round(GROWTH, 2)} animals/year. ")
    return

def displayData(DATA, POPULATION, YEAR) -> None:
    """
    displays the population of the selected age and sex for that year
    :param DATA: int
    :param YEAR: int
    :return: None
    """
    if DATA == 1:
        DATA = "animals with unknown age and sex"
    elif DATA == 2:
        DATA = "adult males"
    elif DATA == 3:
        DATA = "adult females"
    elif DATA == 4:
        DATA = "adults whose ages are unknown"
    elif DATA == 5:
        DATA = "yearlings"
    elif DATA == 6: 
        DATA = "calves"

    print(f"The number of {DATA} in the year {YEAR} is {POPULATION}. ")

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
        addNewData()
    elif CHOICE == 3:
        # INPUTS #
        DATA = selectData()
        YEAR = selectYear()
        # PROCESSING # 
        POPULATION = searchData(DATA, YEAR)
        # OUTPUTS # 
        displayData(DATA, POPULATION, YEAR)
# OUTPUTS # 
    elif CHOICE == 4:
        exit()