import sqlite3
import pandas as pd
import os
#import patoolib
import glob
from ftplib import FTP
import numpy as np
import zipfile
import streamlit as st

df_echantillon=pd.read_excel("ECHANTILLON.xlsx",sheet_name="AGENT")


dico_eleve_enseignant={
    "Etablissement":{101011: 'école publique de DARSO',
    102021: 'école publique de KANTALONG (PACARF)',
    102031: 'école publique de DARA EWA',
    103041: 'école publique de GASSOL-HARKA',
    103042: 'école publique de KOUI-LABBARE',
    104051: 'école publique bilingue de DHOHONG',
    104061: 'école publique de FADA',
    105071: 'école publiques de BEKA MATARI',
    105081: 'école publique de KOUBADJE',
    105091: 'école publique bilingue de DANG (PACARF)',
    201011: 'école publique de BOTOMO',
    201012: 'école publique de YAMBAYE',
    201033: 'école publique de BOTOMO',
    201034: 'école publique de YAMBAYE',
    201045: 'école publique de BOTOMO',
    201046: 'école publique de YAMBAYE',
    201021: 'école bilingue de GUENG',
    201022: 'école publique de ZAKAN',
    401011: 'école publique de BIR-PONDO',
    401012: 'école publique de MOKOLO 2',
    401013: 'école publique de NKOLBIKONG 3',
    401021: 'école publique de FRONTIERE',
    401022: 'école publique de NAGONDA',
    401023: 'école publique de SABAL VILLAGE',
    501031: 'école publique de SOURANDE',
    502041: 'école publique de MAKAMBARA (PIR)',
    502051: 'école publique de BOUBOUMA',
    502061: 'école publique de BOUNGOUR (PIR)',
    503071: 'école publique de NDOUDJIDA (PIR)',
    503081: 'école publique GOUNOUDA (PIR)',
    503091: 'école publique de BARABAYE',
    503101: 'école publique de GIDOUA',
    503111: 'école publique de VADA',
    503112: 'école publique de KAOUDOUS (PIR)',
    504121: 'école publique de KAYA (PIR)',
    504131: 'école publique de TCHADDE (PIR)',
    504141: 'école publique de MORDOK',
    504151: 'école publique de TOULOUM (Bilingue), MADIGALI (PIR)',
    505161: 'école publique de GOUDOUMBOUL (PIR)',
    505171: 'école publique bilingue de TOKOMBERE (PIR)',
    506181: 'école publique de DOUMBOULBAYE',
    506191: 'école publique de MALMAH (PIR)',
    506192: 'école publique de MARBA',
    506201: 'école publique de OUPAI KIRBI',
    601011: 'école publique Groupe 4 de Mbanga',
    601012: 'école Maternelle du quartier 9',
    601021: 'école annexe a Mbaressoumtou Carrière.',
    801011: 'école publique de Mbere',
    801012: 'école publique de Oumarou Ardo',
    801021: 'école publique de Maputki',
    801022: 'école publique de Laria',
    801031: 'école publique de Djalingo plateau',
    801041: 'école publique de Ouro-Barka',
    802051: 'école publique de More-Singai',
    802061: 'école publique de Bebere Gada-Mayo',
    901011: 'école primaire de MBVEH',
    902021: 'GS NWANGRI',
    1001011: 'école publique de BABETE G2',
    1001012: 'école publique de BATOUSSOP',
    1002021: 'école publique de KEKEM groupe 3',
    1003031: 'école publique de SUELAH',
    1003041: 'école publique de NGAZOM',
    1004051: 'école publique de FAMLENG',
    1005061: 'école publique de BANKOUOP',
    1005071: 'école publique de NAGHAM-NJIGOUMBE',
    1101011: "école publique d'ABELONG",
    1102021: "école publique Bilingue d'Efoulan"},
    "Région":{1: 'Adamaoua',
    2: 'Centre',
    3: 'Centre',
    4: 'Est',
    5: 'Extrême-Nord',
    6: 'Littoral',
    7: 'Littoral',
    8: 'Nord',
    9: 'Nord-Ouest',
    10: 'Ouest',
    11: 'Sud',
    12: 'Sud-Ouest'},
    "Departement":{ 10101: 'NGAOUNDAL',
    10202: 'KONTCHA',
    10203: 'TIGNERE',
    10304: 'BANYO',
    10405: 'DJOHONG',
    10406: 'MEIGANGA',
    10507: 'MARTAP',
    10508: 'NGANHA',
    10509: 'NGAOUNDERE 3ème',
    20101: 'BOKITO',
    20102: 'DEUK',
    20103: 'BOKITO',
    20104: 'BOKITO',
    40101: 'BERTOUA 1er',
    40102: 'GAROUA-BOULAI',
    50103: 'BOGO',
    50204: 'FOTOKOL',
    50205: 'GOULFEY',
    50206: 'MAKARY',
    50307: 'GOBO',
    50308: 'GUERE',
    50309: 'MAGA',
    50310: 'WINA',
    50311: 'YAGOUA',
    50412: 'DZIGUILAO',
    50413: 'KAELE',
    50414: 'MOUTOURWA',
    50415: 'TOULOUM',
    50516: 'KOLOFATA',
    50517: 'TOKOMBERE',
    50618: 'BOURRHA',
    50619: 'KOZA',
    50620: 'MOZOGO',
    60101: 'MBANGA',
    60102: 'NKONGSAMBA 1',
    80101: 'BARNDAKE',
    80102: 'BASCHEO',
    80103: 'GAROUA 3ème',
    80104: 'TOUROUA',
    80205: 'FIGUIL',
    80206: 'GUIDER',
    90101: 'KUMBO',
    90202: 'NKAMBE',
    100101: 'MBOUDA',
    100202: 'KEKEM',
    100303: 'PENKA-MICHEL',
    100304: 'SANTCHOU',
    100405: 'BAFOUSSAM 2ème',
    100506: 'FOUMBOT',
    100507: 'KOUOPTAMO',
    110101: 'DJOUM',
    110202: 'EFOULAN'},
    "Resultat":{1:"Rempli totalement",
                2:"Rempli partiellement",
                3:"Non rempli"}
        }

dico_maire={
    "Etablissement":dico_eleve_enseignant['Etablissement'],
    "Région": dico_eleve_enseignant['Région'],
    "Departement":dico_eleve_enseignant['Departement'],
    "Commune":{10101: "NGAOUNDAL",
    10202: "KONTCHA",
    10203: "TIGNERE",
    10304: "BANYO",
    10405: "DJOHONG",
    10406: "MEIGANGA",
    10507: "MARTAP",
    10508: "NGANHA",
    10509: "NGAOUNDERE 3ème",
    20101: "BOKITO",
    20102: "DEUK",
    40101: "BERTOUA 1er",
    40102: "GAROUA-BOULAI",
    50103: "BOGO",
    50204: "FOTOKOL",
    50205: "GOULFEY",
    50206: "MAKARY",
    50307: "GOBO",
    50308: "GUERE",
    50309: "MAGA",
    50310: "WINA",
    50311: "YAGOUA",
    50412: "DZIGUILAO",
    50413: "KAELE",
    50414: "MOUTOURWA",
    50415: "TOULOUM",
    50516: "KOLOFATA",
    50517: "TOKOMBERE",
    50618: "BOURRHA",
    50619: "KOZA",
    50620: "MOZOGO",
    60101: "MBANGA",
    60102: "NKONGSAMBA 1",
    80101: "BARNDAKE",
    80102: "BASCHEO",
    80103: "GAROUA 3ème",
    80104: "TOUROUA",
    80205: "FIGUIL",
    80206: "GUIDER",
    90101: "KUMBO",
    90202: "NKAMBE",
    100101: "MBOUDA",
    100202: "KEKEM",
    100303: "PENKA-MICHEL",
    100304: "SANTCHOU",
    100405: "BAFOUSSAM 2ème",
    100506: "FOUMBOT",
    100507: "KOUOPTAMO",
    110101: "DJOUM",
    110202: "EFOULAN"}}

dico_colonne_ens={
                #Enseignant
              "level-1-id":"ID",
              "s00q00":"Etablissement",
              "s00q01":"Région",
              "s00q02":"Département",
              "s00q03":"Arrondissement",
              "s00q04":"Localité",
              "s00q10":"Superviseur",
              "s00q11":"Controleur",
              "s00q12":"Enqueteur",
              "s00q13":"Date",
              "s00q17":"Résultat",
              "s00q17x":"Autre Résultat",
              "s00q17a":"Disponibilité",
              "g21a":"Longitude",
              "g21b":"Latitude",
              "hd":"Heure debut",
              "hf":"Heure fin",}


#Mairie
dico_colonne_maire={"level-1-id":"ID",
                    "ms00q00":"Etablissement",
              "ms00q01":"Région",
              "ms00q02":"Département",
              "ms00q03":"Arrondissement",
              "ms00q0n":"Localité",
              "ms00q07":"Superviseur",
              "ms00q08":"Controleur",
              "ms00q09":"Enqueteur",
              "ms00q10":"Date",
              "ms00q14":"Résultat",
              "ms00q14x":"Autre Résultat",
              "ms00q14a":"Disponibilité",
              "mg21a":"Longitude",
              "mg21b":"Latitude",
              "mhd":"Heure debut",
              "mhf":"Heure fin",}
              
#Ecole maire
dico_colonne_ec={"level-1-id":"ID",
                 "ecs00q00":"Etablissement",
              "ecs01q03":"Code Commune",
              "ecs00q01":"Région",
              "ecs00q02":"Département",
              "ecs00q03":"Arrondissement",
              "ecs00q03n":"Commune",
              "ecs00q07":"Superviseur",
              "ecs00q08":"Controleur",
              "ecs00q09":"Enqueteur",
              "ecs00q10":"Date",
              "ecs00q14":"Résultat",
              "ecs00q14x":"Autre Résultat",
              "ecs00q14a":"Disponibilité",
              "echd":"Heure debut",
              "echf":"Heure fin",}
              
#Chefferie
dico_colonne_ch={"level-1-id":"ID",
                 "as00q00":"Etablissement",
              "as00q01":"Région",
              "as00q02":"Département",
              "as00q03":"Arrondissement",
              "as00q04":"Localité",
              "as00q08":"Superviseur",
              "as00q09":"Controleur",
              "as00q10":"Enqueteur",
              "as00q11":"Date",
              "as00q15":"Résultat",
              "as00q15x":"Autre Résultat",
              "as00q15a":"Disponibilité",
              "ag21a":"Longitude",
              "ag21b":"Latitude",
              "ahd":"Heure debut",
              "ahf":"Heure fin",}
              
#Elève
dico_colonne_eleve={"level-1-id":"ID",
                    "es00q00":"Etablissement",
              "es00q01":"Région",
              "es00q02":"Département",
              "es00q03":"Arrondissement",
              "es00q04":"Localité",
              "es00q10":"Superviseur",
              "es00q11":"Controleur",
              "es00q12":"Enqueteur",
              "es00q13":"Date",
              "es00q17":"Résultat",
              "es00q17x":"Autre Résultat",
              "es00q17a":"Disponibilité",
              "eg21a":"Longitude",
              "eg21b":"Latitude",
              "ehd":"Heure debut",
              "ehf":"Heure fin",}

#Conversion de du dictionnaire CSpro en dictionnaire python
def transform_cspro_dict(dcf_path):
   
    new_dict = {}
    record = {}
    
    with open(dcf_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('File='):
            dcf_path = line.split('=')[1].strip()
        elif line.startswith('Name='):
            record['name'] = line.split('=')[1].strip()
        elif line.startswith('Label='):
            record['label'] = line.split('=')[1].strip()
        elif line.startswith('Start='):
            record['start'] = int(line.split('=')[1])
        elif line.startswith('Len='):
            record['len'] = int(line.split('=')[1])
        if line.startswith('[ValueSet]'):
            current_name = None
            value_dict = {}
            
            while i < len(lines) and not lines[i].strip().startswith('[Item]'):
                line = lines[i].strip()
                if line.startswith('Name='):
                    current_name = line.split('=')[1]
                elif line.startswith('Value='):
                    parts = line.split('=')
                    if len(parts) == 2:
                        value, label = parts[1].split(';', 1) if ';' in parts[1] else (parts[1], '')
                        value_dict[value] = label
                i += 1
            
            if current_name:
                new_dict[current_name] = value_dict
        else:
            i += 1
    return new_dict
    
#Importation de la table depuis le fichier .csdb
def lire_csdb(csdb_path, table_name=None, columns=None, remove=False):
    conn = sqlite3.connect(csdb_path)
    cursor = conn.cursor()
    # Rename the table 'level-1' to 'level' if it exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='level-1';")
    if cursor.fetchone():
        cursor.execute("ALTER TABLE 'level-1' RENAME TO level;")
        conn.commit()
    # Trouver la table principale si non spécifiée
    if not table_name:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_name = cursor.fetchall()[0][0]  # première table
    
    # Construire la requête SQL
    if columns:
        columns_str = ", ".join(columns)
        query = f"SELECT {columns_str} FROM {table_name}"
        #query = f"SELECT * FROM {table_name}"
    else:
        query = f"SELECT * FROM {table_name}"
    
    # Lire les données
    other_file=csdb_path + ".lst"
    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        if remove==True:
            os.remove(csdb_path)
            os.remove(other_file)
        return df
    except Exception as e:
        print(f"Error reading {csdb_path}: {str(e)}")
        conn.close()
        return None
  

#annotation du dataframe pour la visualisation
def annoter_dataframe(df, dico_cspro):
    for col in df.columns:
        if col in dico_cspro :
            mapping = dico_cspro[col]
            try:
                df[col] = df[col].map(mapping)
            except Exception as e:
                print(f"Erreur d'annotation sur la variable {col} : {e}")
    return df

# Délécharger le fichier .csdb depuis un serveur FTP
def download_ftp_files():
    try:
        ftp = FTP("ADRESS_DU_SERVEUR")
        ftp.login(user="Utilisateur",passwd="mot_de_passe")  # Connexion anonyme
        # Naviguer vers le dossier qui contient un fichier zip
        ftp.cwd('Chemain vers les fichiers contenant les données collectées')
        # Create Data directory if it doesn't exist
        data_dir = 'Data_Zip'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        # Liste les fichiers disponibles
        files = ftp.nlst()
        # Download all available zip files
        available_files = [f for f in files if f.endswith('.zip')]
        if available_files:
            for filename in available_files:
                # Create the full path for saving the file in Data_Zip directory
                local_filepath = os.path.join(data_dir, filename)
                # Download and save each file in Data_Zip directory
                with open(local_filepath, 'wb') as f:
                    ftp.retrbinary(f'RETR {filename}', f.write)
                print(f"File '{filename}' downloaded successfully to {data_dir}/")
        else:
            print("No .zip files found")

        # Fermer la connexion FTP
        ftp.quit()
    except:
        st.error("Impossible de faire la mise à jour, assurez vous d'avoir une bonne connection internet")
        st.stop()
        return
    

#Fonction d'extraction des données
def unzip_data_file(zip_filename):
    try:
        # Create extraction directory if it doesn't exist
        extract_dir = 'extracted_data'
        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)
            
        # Unzip the file
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            print(f"Successfully extracted {zip_filename} to {extract_dir}")
            
        # Return the list of extracted files
        extracted_files = os.listdir(extract_dir)
        return extracted_files
    
    except zipfile.BadZipFile:
        print(f"Error: {zip_filename} is not a valid zip file")
        return None
    except Exception as e:
        print(f"Error extracting {zip_filename}: {str(e)}")
        return None
      
#Fonction d'extraction entière
def Unzip_All_Files():
    zip_dir = 'Data_Zip'
    zip_files = [f for f in os.listdir(zip_dir) if f.endswith('.zip')]
    for zip_file in zip_files:
        zip_path = os.path.join(zip_dir, zip_file)
        extracted_files = unzip_data_file(zip_path)
        if extracted_files:  # Only delete if extraction was successful
            os.remove(zip_path) 
 
#Extractions des informations pour les questionnaires Enseignant
def extrat_enseignant(superviseur=None):
    merged_df = None
    import_col=['`level-1-id`','s00q01', 's00q02', 's00q03' , 's00q04', 's00q10', 's00q11','s00q12','s00q13','s00q17','s00q17x','s00q17a','g21a','g21b']
    col_time=['`level-1-id`','hd','hf']
    id_col=['`level-1-id`','s00q00']
    
    if superviseur:
        df_sup=df_echantillon[df_echantillon["SUP"]==superviseur]
        code_agent=df_sup["ENQ"].tolist()
    else:
        code_agent=df_echantillon["ENQ"].tolist()
    
    
    for agent in code_agent:
        fichier="extracted_data/ENS" + str(agent) + ".csdb"
        try:
            if os.path.exists(fichier):
                if merged_df is None:
                    
                    df_sec = lire_csdb(csdb_path=fichier ,table_name='sect00',columns=import_col)
                    df_time=lire_csdb(csdb_path=fichier,table_name='fin',columns=col_time)
                    df_id=lire_csdb(csdb_path=fichier,table_name='level',columns=id_col)
                    
                    final_df=pd.merge(df_sec,df_time,on="level-1-id",how="inner")
                    final_df=pd.merge(final_df,df_id,on="level-1-id",how="inner")
                                        
                    merged_df = final_df
                else:
                    
                    df_sec = lire_csdb(csdb_path=fichier ,table_name='sect00',columns=import_col)
                    df_time=lire_csdb(csdb_path=fichier,table_name='fin',columns=col_time)
                    df_id=lire_csdb(csdb_path=fichier,table_name='level',columns=id_col)
                    
                    final_df=pd.merge(df_sec,df_time,on="level-1-id",how="inner")
                    final_df=pd.merge(final_df,df_id,on="level-1-id",how="inner")
                                        
                    temp_df = final_df
                    
                    if temp_df is not None:
                        merged_df = pd.concat([merged_df, temp_df], ignore_index=True)
        except Exception as e:
            print(f"Error processing file {fichier}: {str(e)}")
            continue
        
        if os.path.exists(fichier):
            other_file=fichier + ".lst"
            os.remove(fichier)
            os.remove(other_file)
        #merged_df["Type"]="Enseignant"
        #merged_df=merged_df.rename(columns=dico_colonne_ens)


    return merged_df
 
#Extractions des informations pour les questionnaires Mairie
def extrat_maire(superviseur=None):
    merged_df = None
    import_col=['`level-1-id`','ms00q01', 'ms00q02', 'ms00q03' , 'ms00q0n', 'ms00q07', 'ms00q08','ms00q09','ms00q10','ms00q14','ms00q14x','ms00q14a','mg21a','mg21b']
    col_time=['`level-1-id`','mhd','mhf']
    id_col=['`level-1-id`','ms00q00']
    
    
    if superviseur:
        df_sup=df_echantillon[df_echantillon["SUP"]==superviseur]
        code_agent=df_sup["ENQ"].tolist()
    else:
        code_agent=df_echantillon["ENQ"].tolist()
    
    for agent in code_agent:
        fichier="extracted_data/MA" + str(agent) + ".csdb"
        try:
            if os.path.exists(fichier):
                if merged_df is None:
                    
                    df_sec = lire_csdb(csdb_path=fichier ,table_name='msect00',columns=import_col)
                    df_time=lire_csdb(csdb_path=fichier,table_name='mfin',columns=col_time)
                    df_id=lire_csdb(csdb_path=fichier,table_name='level',columns=id_col)
                    
                    final_df=pd.merge(df_sec,df_time,on="level-1-id",how="inner")
                    final_df=pd.merge(final_df,df_id,on="level-1-id",how="inner")
                                        
                    merged_df = final_df
                else:
                    
                    df_sec = lire_csdb(csdb_path=fichier ,table_name='msect00',columns=import_col)
                    df_time=lire_csdb(csdb_path=fichier,table_name='mfin',columns=col_time)
                    df_id=lire_csdb(csdb_path=fichier,table_name='level',columns=id_col)
                    
                    final_df=pd.merge(df_sec,df_time,on="level-1-id",how="inner")
                    final_df=pd.merge(final_df,df_id,on="level-1-id",how="inner")
                                        
                    temp_df = final_df
                    
                    if temp_df is not None:
                        merged_df = pd.concat([merged_df, temp_df], ignore_index=True)
        except Exception as e:
            print(f"Error processing file {fichier}: {str(e)}")
            continue
        
        if os.path.exists(fichier):
            other_file=fichier + ".lst"
            os.remove(fichier)
            os.remove(other_file)
        #merged_df["Type"]="Maire"
        #merged_df=merged_df.rename(columns=dico_colonne_maire)


    return merged_df 
 
#Extractions des informations pour les questionnaires Chefferie
def extrat_chef(superviseur=None):
    merged_df = None
    import_col=['`level-1-id`','as00q01', 'as00q02', 'as00q04' , 'as00q08','as00q09','as00q10','as00q11','as00q15','as00q15x','as00q15a','ag21a','ag21b']
    col_time=['`level-1-id`','ahd','ahf']
    id_col=['`level-1-id`','as00q00','as00q03']
    
    if superviseur:
        df_sup=df_echantillon[df_echantillon["SUP"]==superviseur]
        code_agent=df_sup["ENQ"].tolist()
    else:
        code_agent=df_echantillon["ENQ"].tolist()
    
    
    for agent in code_agent:
        fichier="extracted_data/CHE" + str(agent) + ".csdb"
        try:
            if os.path.exists(fichier):
                if merged_df is None:
                    
                    df_sec = lire_csdb(csdb_path=fichier ,table_name='asect00',columns=import_col)
                    df_time=lire_csdb(csdb_path=fichier,table_name='afin',columns=col_time)
                    df_id=lire_csdb(csdb_path=fichier,table_name='level',columns=id_col)
                    
                    final_df=pd.merge(df_sec,df_time,on="level-1-id",how="inner")
                    final_df=pd.merge(final_df,df_id,on="level-1-id",how="inner")
                                        
                    merged_df = final_df
                else:
                    
                    df_sec = lire_csdb(csdb_path=fichier ,table_name='asect00',columns=import_col)
                    df_time=lire_csdb(csdb_path=fichier,table_name='afin',columns=col_time)
                    df_id=lire_csdb(csdb_path=fichier,table_name='level',columns=id_col)
                    
                    final_df=pd.merge(df_sec,df_time,on="level-1-id",how="inner")
                    final_df=pd.merge(final_df,df_id,on="level-1-id",how="inner")
                                        
                    temp_df = final_df
                    
                    if temp_df is not None:
                        merged_df = pd.concat([merged_df, temp_df], ignore_index=True)
        except Exception as e:
            print(f"Error processing file {fichier}: {str(e)}")
            continue
        
        if os.path.exists(fichier):
            other_file=fichier + ".lst"
            os.remove(fichier)
            os.remove(other_file)
        #merged_df["Type"]="Chefferie"
        #merged_df=merged_df.rename(columns=dico_colonne_ch)

    return merged_df
 
#Extractions des informations pour les questionnaires Eleve
def extrat_eleve(superviseur=None):
    merged_df = None
    import_col=['`level-1-id`','es00q01', 'es00q02', 'es00q03' , 'es00q04', 'es00q10', 'es00q11','es00q12','es00q13','es00q17','es00q17x','es00q17a']
    col_time=['`level-1-id`','ehd','ehf']
    id_col=['`level-1-id`','es00q00']
    
    
    if superviseur:
        df_sup=df_echantillon[df_echantillon["SUP"]==superviseur]
        code_agent=df_sup["ENQ"].tolist()
    else:
        code_agent=df_echantillon["ENQ"].tolist()
        
    for agent in code_agent:
        fichier="extracted_data/ELE" + str(agent) + ".csdb"
        try:
            if os.path.exists(fichier):
                if merged_df is None:
                    
                    df_sec = lire_csdb(csdb_path=fichier ,table_name='esect00',columns=import_col)
                    df_time=lire_csdb(csdb_path=fichier,table_name='efin',columns=col_time)
                    df_id=lire_csdb(csdb_path=fichier,table_name='level',columns=id_col)
                    
                    final_df=pd.merge(df_sec,df_time,on="level-1-id",how="inner")
                    final_df=pd.merge(final_df,df_id,on="level-1-id",how="inner")
                                        
                    merged_df = final_df
                else:
                    
                    df_sec = lire_csdb(csdb_path=fichier ,table_name='esect00',columns=import_col)
                    df_time=lire_csdb(csdb_path=fichier,table_name='efin',columns=col_time)
                    df_id=lire_csdb(csdb_path=fichier,table_name='level',columns=id_col)
                    
                    final_df=pd.merge(df_sec,df_time,on="level-1-id",how="inner")
                    final_df=pd.merge(final_df,df_id,on="level-1-id",how="inner")
                                        
                    temp_df = final_df
                    
                    if temp_df is not None:
                        merged_df = pd.concat([merged_df, temp_df], ignore_index=True)
        except Exception as e:
            print(f"Error processing file {fichier}: {str(e)}")
            continue
        if os.path.exists(fichier):
            other_file=fichier + ".lst"
            os.remove(fichier)
            os.remove(other_file)
        #new_col=[dico_colonne_eleve[col] for col in merged_df.columns]
        #merged_df.columns=new_col
        #merged_df["Type"]="Elève"

    return merged_df

#Extractions des informations pour les questionnaires ecole maire
def extrat_ecole_maire(superviseur=None):
    merged_df = None
    import_col=['`level-1-id`','ecs00q01', 'ecs00q02', 'ecs00q03','ecs00q03n' , 'ecs00q07','ecs00q08','ecs00q09','ecs00q10','ecs00q14','ecs00q14x','ecs00q14a']
    col_time=['`level-1-id`','echd','echf']
    id_col=['`level-1-id`','ecs01q03','ecs00q00']
    
    if superviseur:
        df_sup=df_echantillon[df_echantillon["SUP"]==superviseur]
        code_agent=df_sup["ENQ"].tolist()
    else:
        code_agent=df_echantillon["ENQ"].tolist()
    
    
    for agent in code_agent:
        fichier="extracted_data/ECMA" + str(agent) + ".csdb"
        try:
            if os.path.exists(fichier):
                if merged_df is None:
                    
                    df_sec = lire_csdb(csdb_path=fichier ,table_name='ecsect00',columns=import_col)
                    df_time=lire_csdb(csdb_path=fichier,table_name='ecfin',columns=col_time)
                    df_id=lire_csdb(csdb_path=fichier,table_name='level',columns=id_col)
                    
                    final_df=pd.merge(df_sec,df_time,on="level-1-id",how="inner")
                    final_df=pd.merge(final_df,df_id,on="level-1-id",how="inner")
                                        
                    merged_df = final_df
                else:
                    
                    df_sec = lire_csdb(csdb_path=fichier ,table_name='ecsect00',columns=import_col)
                    df_time=lire_csdb(csdb_path=fichier,table_name='ecfin',columns=col_time)
                    df_id=lire_csdb(csdb_path=fichier,table_name='level',columns=id_col)
                    
                    final_df=pd.merge(df_sec,df_time,on="level-1-id",how="inner")
                    final_df=pd.merge(final_df,df_id,on="level-1-id",how="inner")
                                        
                    temp_df = final_df
                    
                    if temp_df is not None:
                        merged_df = pd.concat([merged_df, temp_df], ignore_index=True)
        except Exception as e:
            print(f"Error processing file {fichier}: {str(e)}")
            continue
        
        if os.path.exists(fichier):
            other_file=fichier + ".lst"
            os.remove(fichier)
            os.remove(other_file)
        #merged_df["Type"]="Ecole-Maire"
        #merged_df=merged_df.rename(columns=dico_colonne_ec)


    return merged_df






