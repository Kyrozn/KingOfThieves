import csv
import os
import pandas
# File name
csv_file = "file.csv"


# Function to register a new user
def registerData(dataFrame: pandas.DataFrame):
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        print(
            str(dataFrame["StartPos"].values[0]),
        )
        writer.writerow(
            [
                str(dataFrame["StartPos"].values[0]),
                str(dataFrame["ObjectifPos"].values[0]),
                str(dataFrame["Piege1"]),
                str(dataFrame["Piege2"]),
                str(dataFrame["Piege3"]),
                dataFrame["Win"],
                dataFrame["Try"],
                dataFrame["Temps"],
                dataFrame["ActNb"],
                str(dataFrame["JumpsPos"]),
            ]
        )
    print("Données enregistrées avec succès !")
