import csv
import os
import pandas
# File name
csv_file = "file.csv"

# Function to register data
def registerData(dataFrame: pandas.DataFrame):
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                str(dataFrame["StartPos"].values[0]),
                str(dataFrame["ObjectifPos"].values[0]),
                str(dataFrame["Piege1"].values[0]),
                str(dataFrame["Piege2"].values[0]),
                str(dataFrame["Piege3"].values[0]),
                str(dataFrame["Win"].values[0]),
                str(dataFrame["TryRemaining"].values[0]),
                dataFrame["Temps"].values[0],
                dataFrame["ActNb"].values[0],
                str(dataFrame["JumpsPos"].values[0]),
            ]
        )
    print("Données enregistrées avec succès !")
