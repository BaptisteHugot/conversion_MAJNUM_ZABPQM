# Bibliothèques à importer
import pandas as pd
import time
from datetime import datetime

st = time.time() # Début du chronomètre
print("Programme démarré")

# On récupère la liste des ressources en numérotation
dataNumeros = pd.read_excel("https://www.data.gouv.fr/fr/datasets/r/90e8bdd0-0f5c-47ac-bd39-5f46463eb806", header=0, dtype=str);

dataZABPQM = [] # Table pour récupérer les éléments du fichier de numérotation au format ZABPQM
date_format = '%Y-%m-%d %H:%M:%S' # Format initial de la date d'attribution, qui servira à convertir cette date au format date pour conserver le bon format dans le fichier final

# On parcourt la liste des opérateurs
for num in range(0, len(dataNumeros)):
    tranche = dataNumeros.iloc[num, 0]
    
    if tranche[0] == "0": # Si la tranche commence par 0, c'est un numéro court
        if len(tranche) < 7: # Si la longueur de la tranche est inférieure à 7, il faut la traiter
            delta = pow(10,7-len(tranche)) # Nombre de lignes à ajouter
            for i in range(0, delta):
                trancheZABPQM = ""
                concat = str(i).rjust(7-len(tranche),"0") # On ajoute des 0 à gauche pour respecter le format à 7 chiffres
                trancheZABPQM = tranche + concat # On ajoute le suffixe aux tranches
                dataZABPQM.append([str(trancheZABPQM), str(trancheZABPQM)+"000", str(trancheZABPQM)+"999", str(dataNumeros.iloc[num, 3]), str(dataNumeros.iloc[num, 4]), str(datetime.strptime(dataNumeros.iloc[num, 5],date_format).strftime("%d/%m/%Y"))])
        else: # Longueur de tranche de 7 (ZABPQM) ou supérieure pour les numéros de longueur étendue, on la recopie telle quelle
            dataZABPQM.append([str(tranche), str(dataNumeros.iloc[num, 1]), str(dataNumeros.iloc[num, 2]), str(dataNumeros.iloc[num, 3]), str(dataNumeros.iloc[num, 4]), str(datetime.strptime(dataNumeros.iloc[num, 5],date_format).strftime("%d/%m/%Y"))])
    else: # Numéro court, on le recopie tel quel
        dataZABPQM.append([str(tranche), str(dataNumeros.iloc[num, 1]), str(dataNumeros.iloc[num, 2]), str(dataNumeros.iloc[num, 3]), str(dataNumeros.iloc[num, 4]), str(datetime.strptime(dataNumeros.iloc[num, 5],date_format).strftime("%d/%m/%Y"))])

dataframe = pd.DataFrame(dataZABPQM)
dataframe.to_excel(r"./MAJNUM_ZABPQM.xlsx", sheet_name='MAJNUM', header=["EZABPQM","Tranche_Debut","Tranche_Fin","Mnémo","Territoire","Date_Attribution"], index=False)

et = time.time() # Fin du chronomètre
elapsed_time = time.strftime("%H:%M:%S", time.gmtime(et - st)) # Durée d'exécution du programme
print("Programme exécuté en : ", elapsed_time, ".")
