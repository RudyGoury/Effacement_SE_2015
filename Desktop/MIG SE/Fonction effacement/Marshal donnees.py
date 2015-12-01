# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 10:41:50 2015

@author: Pierre
"""

import marshal as ms
from datetime import *
import Matrice_exemple_affichage

def datetime_to_str(date_time):
    date = ""
    if date_time.day < 10:
        date+='0'+str(date_time.day)
    else:
        date+=str(date_time.day)
    date+='/'
    if date_time.month < 10:
        date+='0'+str(date_time.month)
    else:
        date+=str(date_time.month)
    date+='/' + str(date_time.year) + ' '
    if date_time.hour < 10:
        date+='0'+str(date_time.hour)
    else:
        date+=str(date_time.hour)
    date+=':'
    if date_time.minute < 10:
        date+='0'+str(date_time.minute)
    else:
        date+=str(date_time.minute)
    date+=':'
    if date_time.second < 10:
        date+='0'+str(date_time.second)
    else:
        date+=str(date_time.second)
    return(date)

def donnees_to_bytes(liste_dates,liste_temperatures,liste_matrices,liste_effacements,d_init):
    liste_dates_str = []
    for date_time in liste_dates:
        liste_dates_str.append(datetime_to_str(date_time))
    ms.dump([liste_dates_str,liste_temperatures,liste_matrices,d_init],open('file_data.dat','ab'))

def bytes_to_donnees(file_path):
    file_data = open(file_path,'rb')
    tuple_d_t_m = ms.load(file_data)
    dates = []
    print(tuple_d_t_m[0])
    for date in tuple_d_t_m[0]:
        print(date)
        jour = int(date[0:2])
        mois= int(date[3:5])
        année = int(date[6:10])
        heure = int(date[11:13])
        minutes = int(date[14:16])
        secondes = int(date[17:19])
        dates.append(datetime(année,mois,jour,heure,minutes,secondes))
    return([dates,tuple_d_t_m[1],tuple_d_t_m[2],tuple_d_t_m[3],tuple_d_t_m[4]])
    
def Test():
    tuple_date_temp_mat = Matrice_test()
    # print(tuple_date_temp_mat)
    dates = tuple_date_temp_mat[0]
    temp = tuple_date_temp_mat[1]
    mat = tuple_date_temp_mat[2]
    donnees_to_bytes(dates,temp,mat)
    print(bytes_to_donnees('file_data.dat'))