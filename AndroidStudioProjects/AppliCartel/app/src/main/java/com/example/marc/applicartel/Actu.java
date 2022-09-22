package com.example.marc.applicartel;
// Cette petite classe rassemble seulement toutes les infos nécessaires à la création d'une actualité

import android.os.Parcelable;
import android.os.Parcel;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.Scanner;

/**
 * Created by marc on 06/02/16.
 */
public class Actu implements Parcelable {

    // #################  ATTRIBUTS  ##############################
    String titre;
    int idPhotoIcone;
    String date;
    String heure;

    int idPhotoGrande;
    String auteur;
    String texte;

    // ################ CONSTRUCTEUR ################################

    Actu(String titre,int idPhotoIcone,String date,String heure,
         int idPhotoGrande,String auteur,String texte){
        this.titre = titre;
        this.idPhotoIcone = idPhotoIcone;
        this.date = date;
        this.heure = heure;
        this.idPhotoGrande = idPhotoGrande;
        this.auteur = auteur;
        this.texte = texte;
    }

    // ############### PARCELABLE ######################

    @Override
    public int describeContents() {
        //On renvoie 0, car notre classe ne contient pas de FileDescriptor
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        // On ajoute les objets dans l'ordre dans lequel on les a déclarés
        dest.writeString(titre);
        dest.writeString(date);
        dest.writeString(heure);
        dest.writeInt(idPhotoGrande);
        dest.writeString(auteur);
        dest.writeString(texte);
    }


    public static final Parcelable.Creator<Actu> CREATOR = new Parcelable.Creator<Actu>() {
        @Override
        public Actu createFromParcel(Parcel source) {
            return new Actu(source);
        }

        @Override
        public Actu[] newArray(int size) {
            return new Actu[size];
        }
    };

    public Actu(Parcel in) {
        titre = in.readString();
        date = in.readString();
        heure = in.readString();
        idPhotoGrande = in.readInt();
        auteur = in.readString();
        texte = in.readString();
    }


}

