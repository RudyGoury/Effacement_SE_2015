# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 14:20:12 2015

@author: Xavier
"""
import pandas as pd
import datetime
import matplotlib.pyplot as plt

def convert_to_datetime(date):
    jour = int(date[0:2])
    mois = int(date[3:5])
    annee = int(date[6:10])
    heure = int(date[11:13])
    minut = int(date[14:16])
    sec = 00
    return(datetime.datetime(annee,mois,jour,heure,minut,sec))
    

def date_selon_T_ext(tExt, marge) :
    data = pd.HDFStore('data_brut_mod.h5')
    df = data['Temperature_exterieure']
    nb_lignes1,nb_colonnes1 = df.shape
    date_debut = convert_to_datetime("01/12/2014 00:00")
    date_fin = convert_to_datetime("12/07/2015 00:00")
    date_init1 = df["date et heure"][0]
    date_stop1 = df["date et heure"][nb_lignes1 - 1]
    if date_debut > date_fin:
        date_debut,date_fin = date_fin,date_debut
    if date_debut < date_init1:
        date_debut = date_init1
    if date_fin > date_stop1:
        date_fin = date_stop1
    delta1 = date_debut - date_init1
    indice_debut1 = int(delta1.total_seconds()/600)
    list_indice1 = [k  for k in range(indice_debut1,32112) if ( (df['T° Exterieure'][k] < tExt + marge) and (df['T° Exterieure'][k] > tExt - marge))]
    list_date1 = [df['date et heure'][k] for k in list_indice1]
    data.close()
    return(list_date1)
    
    
    
def prevision_temperature(temperature, puissance, tExt, nom_temperature) : 
    dates_utiles = date_selon_T_ext(tExt, 0.005)
    
    #au cas où trop peu de valeurs correspondent
    k = 1
    while len(dates_utiles) <= 5 : 
        k+=1
        dates_utiles = date_selon_T_ext(tExt, 0.005*k)
    
    #initialisations
    puissances = []
    temperatures_int = []
    temperatures_int_apres = []
    date_debut = dates_utiles[0]
    date_fin = dates_utiles[-1]
    data = pd.HDFStore('data_brut_mod.h5')
    df1 = data["General_Clim"]
    df2 = data['Temperatures2']
    nb_lignes1,nb_colonnes1 = df1.shape
    nb_lignes2,nb_colonnes2 = df2.shape
    date_init1 = df1["date et heure"][0]
    date_stop1 = df1["date et heure"][nb_lignes1 - 1]
    date_init2 = df2["date et heure"][0]
    date_stop2 = df2["date et heure"][nb_lignes2 - 1]
    if date_debut > date_fin:
        date_debut,date_fin = date_fin,date_debut
    if date_debut < date_init1:
        date_debut = date_init1
    if date_fin > date_stop1:
        date_fin = date_stop1
    if date_debut < date_init2:
        date_debut = date_init2
    if date_fin > date_stop2:
        date_fin = date_stop2
    delta1 = date_debut - date_init1
    delta = date_fin - date_debut
    indice_debut1 = int(delta1.total_seconds()/600)
    nb_valeurs = int(delta.total_seconds()/600)+1
    indice_fin1 = indice_debut1 + nb_valeurs
    list_indice1 = [k for k in range(indice_debut1,indice_fin1)]
    list_date1 = [df1['date et heure'][k] for k in list_indice1]
    delta2 = date_debut - date_init2
    indice_debut2 = int(delta2.total_seconds()/600)
    indice_fin2 = indice_debut2 + nb_valeurs
    list_indice2 = [k for k in range(indice_debut2,indice_fin2)]
    list_date2 = [df2['date et heure'][k] for k in list_indice2]
    proches = []
    
    #calcul des normes des points proches
    for k in range(min(len(list_date1), len(list_date2))) : 
        if list_date1[k] in dates_utiles : 
            puiss = df1['Puissance'][k]
            temp_int = df2[nom_temperature][k]
            temp_int_apres = df2[nom_temperature][k+1]
            delta_T = temp_int_apres - temp_int
            norme = (temp_int - temperature)**2 + ((puiss - puissance)/200)**2
            proches.append([norme, delta_T])
    
    #obtention des points les plus proches en norme
    min1 = 0
    min2 = 1
    min3 = 2
    if proches[1][0] < proches[0][0] : 
        min1, min2 = min2, min1
    if proches[2][0] < proches[1][0] : 
        min3, min2 = min2, min3
    if proches[2][0] < proches[0][0] : 
        min1, min3 = min3, min1
    for k in range(3, len(proches)) : 
        norme0 = proches[k][0]
        if norme0 < proches[min1][0] : 
            min1, min2, min3 = min2, min3, k
        elif norme0 < proches[min2][0] : 
            min2, min3 = min3, k
        elif norme0 < proches[min3][0] : 
            min3 = k
    
    #calcul de la moyenne d'hausse    
    delta_moy = (proches[min1][1] + proches[min2][1] + proches[min3][1])/3
    data.close()
    return(delta_moy + temperature)

    
def prochaines_temperatures1(date) : 
    date = convert_to_datetime(date)
    data = pd.HDFStore('data_brut_mod.h5')
    df = data['Temperatures2']
    df1 = data["General_Clim"]
    df2 = data["Temperature_exterieure"]
    for k in range(len (df2["date et heure"])) : 
        if df2["date et heure"][k] == date :
            x = (prevision_temperature(df["T° Bureau Coordination Responsable de Service"][k], df1["Puissance"][k], df2["T° Exterieure"][k], "T° Bureau Coordination Responsable de Service"))
            df["T° Bureau Coordination Responsable de Service"][k+1] = x
            x = (prevision_temperature(df["T° Bureau Administration Assistantes de Direction"][k], df1["Puissance"][k], df2["T° Exterieure"][k], "T° Bureau Administration Assistantes de Direction"))
            df["T° Bureau Administration Assistantes de Direction"][k+1] = x
            x = (prevision_temperature(df["T° Bureau Gestion Financiere Comptable"][k], df1["Puissance"][k], df2["T° Exterieure"][k], "T° Bureau Gestion Financiere Comptable"))
            df["T° Bureau Gestion Financiere Comptable"][k+1] = x  
            x = (prevision_temperature(df["T° Bureau Administation Secretariat"][k], df1["Puissance"][k], df2["T° Exterieure"][k], "T° Bureau Administation Secretariat"))
            df["T° Bureau Administation Secretariat"][k+1] = x  
            data['Temperatures2'] = df
            data.close()
            return "done"
    data.close()

def effacement(date) : 
    date = convert_to_datetime(date)
    data = pd.HDFStore('data_brut_mod.h5')
    df = data['Temperatures2']
    df1 = data["General_Clim"]
    df2 = data["Temperature_exterieure"]
    for k in range(len (df2["date et heure"])) : 
        if df2["date et heure"][k] == date :
            x = (prevision_temperature(df["T° Bureau Coordination Responsable de Service"][k], 0, df2["T° Exterieure"][k], "T° Bureau Coordination Responsable de Service"))
            df["T° Bureau Coordination Responsable de Service"][k+1] = x
            x = (prevision_temperature(df["T° Bureau Administration Assistantes de Direction"][k], 0, df2["T° Exterieure"][k], "T° Bureau Administration Assistantes de Direction"))
            df["T° Bureau Administration Assistantes de Direction"][k+1] = x
            x = (prevision_temperature(df["T° Bureau Gestion Financiere Comptable"][k],0,  df2["T° Exterieure"][k], "T° Bureau Gestion Financiere Comptable"))
            df["T° Bureau Gestion Financiere Comptable"][k+1] = x  
            x = (prevision_temperature(df["T° Bureau Administation Secretariat"][k], 0, df2["T° Exterieure"][k], "T° Bureau Administation Secretariat"))
            df["T° Bureau Administation Secretariat"][k+1] = x  
            data['Temperatures2'] = df
            data.close()
            return "done"
    data.close()
 

"""
effacement ("06/06/2015 15:10")
effacement("06/06/2015 15:20")
effacement("06/06/2015 15:30")
effacement("06/06/2015 15:40")
effacement("06/06/2015 15:50")
effacement("06/06/2015 16:00")

prochaines_temperatures1("06/06/2015 16:10")
prochaines_temperatures1("06/06/2015 16:20")

prochaines_temperatures1("05/05/2015 15:10")
prochaines_temperatures1("05/05/2015 15:20")
prochaines_temperatures1("05/05/2015 15:30")
prochaines_temperatures1("05/05/2015 15:40")
prochaines_temperatures1("05/05/2015 15:50")
prochaines_temperatures1("05/05/2015 16:00")
prochaines_temperatures1("04/04/2015 15:10")
prochaines_temperatures1("04/04/2015 15:20")
prochaines_temperatures1("04/04/2015 15:30")
prochaines_temperatures1("04/04/2015 15:40")
prochaines_temperatures1("04/04/2015 15:50")
prochaines_temperatures1("04/04/2015 16:00")
prochaines_temperatures1("03/03/2015 15:10")
prochaines_temperatures1("03/03/2015 15:20")
prochaines_temperatures1("03/03/2015 15:30")
prochaines_temperatures1("03/03/2015 15:40")
prochaines_temperatures1("03/03/2015 15:50")
prochaines_temperatures1("03/03/2015 16:00")

prochaines_temperatures1("02/02/2015 08:00")
prochaines_temperatures1("02/02/2015 08:10")
prochaines_temperatures1("02/02/2015 08:20")
prochaines_temperatures1("02/02/2015 08:30")
prochaines_temperatures1("02/02/2015 08:40")
prochaines_temperatures1("02/02/2015 08:50")
 
prochaines_temperatures1("06/06/2015 05:10")
prochaines_temperatures1("06/06/2015 05:20")
prochaines_temperatures1("06/06/2015 05:30")
prochaines_temperatures1("06/06/2015 05:40")
prochaines_temperatures1("06/06/2015 05:50")
prochaines_temperatures1("06/06/2015 06:00")
prochaines_temperatures1("05/05/2015 05:10")
prochaines_temperatures1("05/05/2015 05:20")
prochaines_temperatures1("05/05/2015 05:30")
prochaines_temperatures1("05/05/2015 05:40")
prochaines_temperatures1("05/05/2015 05:50")
prochaines_temperatures1("05/05/2015 06:00")
prochaines_temperatures1("04/04/2015 05:10")
prochaines_temperatures1("04/04/2015 05:20")
prochaines_temperatures1("04/04/2015 05:30")
prochaines_temperatures1("04/04/2015 05:40")
prochaines_temperatures1("04/04/2015 05:50")
prochaines_temperatures1("04/04/2015 06:00")
prochaines_temperatures1("03/03/2015 05:10")
prochaines_temperatures1("03/03/2015 05:20")
prochaines_temperatures1("03/03/2015 05:30")
prochaines_temperatures1("03/03/2015 05:40")
prochaines_temperatures1("03/03/2015 05:50")
prochaines_temperatures1("03/03/2015 06:00")
prochaines_temperatures1("02/02/2015 05:10")
prochaines_temperatures1("02/02/2015 05:20")
prochaines_temperatures1("02/02/2015 05:30")
prochaines_temperatures1("02/02/2015 05:40")
prochaines_temperatures1("02/02/2015 05:50")
prochaines_temperatures1("02/02/2015 06:00")
prochaines_temperatures1("06/06/2015 10:10")
prochaines_temperatures1("06/06/2015 10:20")
prochaines_temperatures1("06/06/2015 10:30")
prochaines_temperatures1("06/06/2015 10:40")
prochaines_temperatures1("06/06/2015 10:50")
prochaines_temperatures1("06/06/2015 11:00")
prochaines_temperatures1("05/05/2015 10:10")
prochaines_temperatures1("05/05/2015 10:20")
prochaines_temperatures1("05/05/2015 10:30")
prochaines_temperatures1("05/05/2015 10:40")
prochaines_temperatures1("05/05/2015 10:50")
prochaines_temperatures1("05/05/2015 11:00")
prochaines_temperatures1("04/04/2015 10:10")
prochaines_temperatures1("04/04/2015 10:20")
prochaines_temperatures1("04/04/2015 10:30")
prochaines_temperatures1("04/04/2015 10:40")
prochaines_temperatures1("04/04/2015 10:50")
prochaines_temperatures1("04/04/2015 11:00")
prochaines_temperatures1("03/03/2015 10:10")
prochaines_temperatures1("03/03/2015 10:20")
prochaines_temperatures1("03/03/2015 10:30")
prochaines_temperatures1("03/03/2015 10:40")
prochaines_temperatures1("03/03/2015 10:50")
prochaines_temperatures1("03/03/2015 11:00")
prochaines_temperatures1("02/02/2015 10:10")
prochaines_temperatures1("02/02/2015 10:20")
prochaines_temperatures1("02/02/2015 10:30")
prochaines_temperatures1("02/02/2015 10:40")
prochaines_temperatures1("02/02/2015 10:50")
prochaines_temperatures1("02/02/2015 11:00")
prochaines_temperatures1("06/06/2015 20:10")
prochaines_temperatures1("06/06/2015 20:20")
prochaines_temperatures1("06/06/2015 20:30")
prochaines_temperatures1("06/06/2015 20:40")
prochaines_temperatures1("06/06/2015 20:50")
prochaines_temperatures1("06/06/2015 21:00")
prochaines_temperatures1("05/05/2015 20:10")
prochaines_temperatures1("05/05/2015 20:20")
prochaines_temperatures1("05/05/2015 20:30")
prochaines_temperatures1("05/05/2015 20:40")
prochaines_temperatures1("05/05/2015 20:50")
prochaines_temperatures1("05/05/2015 21:00")
prochaines_temperatures1("04/04/2015 20:10")
prochaines_temperatures1("04/04/2015 20:20")
prochaines_temperatures1("04/04/2015 20:30")
prochaines_temperatures1("04/04/2015 20:40")
prochaines_temperatures1("04/04/2015 20:50")
prochaines_temperatures1("04/04/2015 21:00")
prochaines_temperatures1("03/03/2015 20:10")
prochaines_temperatures1("03/03/2015 20:20")
prochaines_temperatures1("03/03/2015 20:30")
prochaines_temperatures1("03/03/2015 20:40")
prochaines_temperatures1("03/03/2015 20:50")
prochaines_temperatures1("03/03/2015 21:00")



"""

def verification_par_graphe2(date) :
    data = pd.HDFStore('data_brut.h5')
    data1 = pd.HDFStore('data_brut_mod.h5')
    df = data['Temperatures2']
    df1 = data1['Temperatures2']

    for k in range(len (df["date et heure"])) : 
        if df["date et heure"][k] == convert_to_datetime(date) : 
            ordonnees = [df["T° Bureau Coordination Responsable de Service"][k+j] for j in range(19)]
            abscisses = [j for j in range(19)]
            ordonnees1 = [df1["T° Bureau Coordination Responsable de Service"][k+j] for j in range(19)]
            plt.plot(abscisses, ordonnees, 'r')
            plt.plot(abscisses, ordonnees1, 'c')
            plt.show()
            ordonnees = [df["T° Bureau Administration Assistantes de Direction"][k+j] for j in range(19)]
            ordonnees1 = [df1["T° Bureau Administration Assistantes de Direction"][k+j] for j in range(19)]
            abscisses = [j for j in range(19)]
            plt.plot(abscisses, ordonnees, 'r')
            plt.plot(abscisses, ordonnees1, 'c')
            plt.show()
            ordonnees = [df["T° Bureau Gestion Financiere Comptable"][k+j] for j in range(19)]
            abscisses = [j for j in range(19)]
            ordonnees1 = [df1["T° Bureau Gestion Financiere Comptable"][k+j] for j in range(19)]
            plt.plot(abscisses, ordonnees, 'r')
            plt.plot(abscisses, ordonnees1, 'c')
            plt.show()
            ordonnees = [df["T° Bureau Administation Secretariat"][k+j] for j in range(19)]
            abscisses = [j for j in range(19)]
            ordonnees1 = [df1["T° Bureau Administation Secretariat"][k+j] for j in range(19)]
            plt.plot(abscisses, ordonnees1, 'c')
            plt.plot(abscisses, ordonnees, 'r')
            plt.show()
            data.close()
            data1.close()
            
            return "yes"
            
    
verification_par_graphe2("02/02/2015 08:00")
s


x = prevision_temperature(26, 0, 8, 'T° Bureau Administation Secretariat') 
x1 =  prevision_temperature(x, 0, 8, 'T° Bureau Administation Secretariat')
x2 =  prevision_temperature(x1, 0, 8, 'T° Bureau Administation Secretariat')
x3 =  prevision_temperature(x2, 0, 8, 'T° Bureau Administation Secretariat')
x4 =  prevision_temperature(x3, 0, 8, 'T° Bureau Administation Secretariat')
x5 =  prevision_temperature(x4, 0, 8, 'T° Bureau Administation Secretariat')
x6 =  prevision_temperature(x5, 2000, 8, 'T° Bureau Administation Secretariat')
x7 =  prevision_temperature(x6, 2000, 8, 'T° Bureau Administation Secretariat')
print(26,  x, x1, x2, x3, x4, x5, x6, x7)

x = prevision_temperature(22, 0, 30, 'T° Bureau Administation Secretariat') 
x1 =  prevision_temperature(x, 0, 30, 'T° Bureau Administation Secretariat')
x2 =  prevision_temperature(x1, 0, 30, 'T° Bureau Administation Secretariat')
x3 =  prevision_temperature(x2, 0, 30, 'T° Bureau Administation Secretariat')
x4 =  prevision_temperature(x3, 0, 30, 'T° Bureau Administation Secretariat')
x5 =  prevision_temperature(x4, 0, 30, 'T° Bureau Administation Secretariat')
x6 =  prevision_temperature(x5, 100, 30, 'T° Bureau Administation Secretariat')
x7 =  prevision_temperature(x6, 100, 30, 'T° Bureau Administation Secretariat')
print(22,  x, x1, x2, x3, x4, x5, x6, x7)