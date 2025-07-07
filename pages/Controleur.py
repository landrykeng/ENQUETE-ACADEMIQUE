import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import streamlit as st
import traceback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px 
from streamlit_plotly_events import plotly_events
import seaborn as sns
import os
import warnings
import datetime
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.offline as py
import plotly.tools as tls
from scipy.stats import chi2_contingency
from scipy.stats import ttest_ind
from scipy.stats import levene
import plotly
import time
import datetime as dt
import warnings
warnings.filterwarnings('ignore')
from my_fonction import *
from Authentification import *
from My_Cspro_function import *
from New_Function import *
from PIL import Image
from pathlib import Path
import json
from streamlit_echarts import st_echarts
from PIL import Image

st.set_page_config(layout="wide")
#import_users_from_excel()

zoom_css = """
    <style>
        .main {
            transform: scale(0.67);
            transform-origin: top left;
        }
    </style>
"""

st.markdown(zoom_css, unsafe_allow_html=True)

st.markdown("""
            <style>
            /* Quand la sidebar est fermée */
            [data-testid="stSidebar"][aria-expanded="false"] {
                width: 0;
                min-width: 0;
                overflow: hidden;
                transition: width 0.3s ease;
            }
            
            /* Extension complète du contenu principal quand sidebar fermée */
            [data-testid="stSidebar"][aria-expanded="false"] + div [data-testid="stAppViewContainer"] {
                max-width: 100% !important;
                padding: 0 !important;
            }
            
            /* Graphiques en plein écran */
            [data-testid="stSidebar"][aria-expanded="false"] + div .stPlotlyChart {
                width: 100% !important;
                max-width: 100% !important;
            }
            
            /* Conteneurs étendus */
            [data-testid="stSidebar"][aria-expanded="false"] + div [data-testid="stBlock"] {
                width: 100% !important;
                padding: 0 !important;
                margin: 0 !important;
            }
            
            /* Style de la sidebar quand ouverte */
            [data-testid="stSidebar"][aria-expanded="true"] {
                width: 250px !important;
                min-width: 250px !important;
                transition: width 0.3s ease;
            }
            
            /* Ajustements généraux */
            .stPlotlyChart {
                width: 100%;
                max-width: 100%;
            }
            </style>
            """, unsafe_allow_html=True)

        #pour les conteneurs de graphiques

st.markdown("""
                <style>
                /* Styles de base pour tous les thèmes */
                .stContainer {
                    border-radius: 10px;  /* Coins arrondis */
                    border: 2px solid transparent;  /* Bordure transparente par défaut */
                    padding: 20px;  /* Espacement intérieur */
                    margin-bottom: 20px;  /* Espace entre les conteneurs */
                    transition: all 0.3s ease;  /* Animation douce */
                }

                /* Mode Clair (par défaut) */
                body:not(.dark) .stContainer {
                    background-color: rgba(255, 255, 255, 0.9);  /* Fond blanc légèrement transparent */
                    border-color: rgba(224, 224, 224, 0.7);  /* Bordure grise légère */
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08);  /* Ombre douce */
                }

                /* Mode Sombre */
                body.dark .stContainer {
                    background-color: rgba(30, 30, 40, 0.9);  /* Fond sombre légèrement transparent */
                    border-color: rgba(60, 60, 70, 0.7);  /* Bordure sombre légère */
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);  /* Ombre plus marquée */
                }

                /* Effet de survol - Mode Clair */
                body:not(.dark) .stContainer:hover {
                    box-shadow: 0 8px 12px rgba(0, 0, 0, 0.5);  /* Ombre plus prononcée */
                    transform: translateY(-5px);  /* Léger soulèvement */
                    border-color: rgba(200, 200, 200, 0.9);  /* Bordure plus visible */
                }

                /* Effet de survol - Mode Sombre */
                body.dark .stContainer:hover {
                    box-shadow: 0 8px 12px rgba(255, 255, 255, 0.5);  /* Ombre claire */
                    transform: translateY(-5px);  /* Léger soulèvement */
                    border-color: rgba(100, 100, 110, 0.9);  /* Bordure plus visible */
                }

                /* Style spécifique pour les graphiques - Mode Clair */
                body:not(.dark) .stPlotlyChart {
                    background-color: rgba(250, 250, 250, 0.95);  /* Fond très légèrement gris */
                    border-radius: 8px;  /* Coins légèrement arrondis */
                    padding: 10px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);  /* Ombre très légère */
                }

                /* Style spécifique pour les graphiques - Mode Sombre */
                body.dark .stPlotlyChart {
                    background-color: rgba(40, 40, 50, 0.95);  /* Fond sombre légèrement transparent */
                    border-radius: 8px;  /* Coins légèrement arrondis */
                    padding: 10px;
                    box-shadow: 0 2px 4px rgba(255, 255, 255, 0.05);  /* Ombre très légère */
                }
                </style>
                """, unsafe_allow_html=True)

useless_style="""
        <style>
        .sidebar-link {
            display: block;
            margin-bottom: 15px;
            padding: 10px 15px;
            text-decoration: none;
            color: #333;
            background-color: #f8f9fa;
            border-radius: 8px;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .sidebar-link-right {
            display: block;
            margin-bottom: 15px;
            padding: 10px 15px;
            text-decoration: none;
            color: #333;
            background-color: #f8f9fa;
            border-radius: 8px;
            transition: all 0.3s ease;
            font-weight: 500;
            text-align: right;
        }

        .sidebar-link-center {
            display: block;
            margin-bottom: 15px;
            padding: 10px 15px;
            text-decoration: none;
            color: #333;
            background-color: #f8f9fa;
            border-radius: 8px;
            transition: all 0.3s ease;
            font-weight: 500;
            text-align: center;
        }
        </style>
        """

sidebar_css = """
        <style>
        .sidebar-link {
            display: block;
            margin-bottom: 15px;
            padding: 10px 15px;
            text-decoration: none;
            color: #333;
            background-color: #f8f9fa;
            border-radius: 8px;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .sidebar-link:hover {
            background-color: #e9ecef;
            color: #007bff;
            transform: translateX(5px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .sidebar-link-icon {
            margin-right: 10px;
        }
        </style>
        """
        
table_css = """
        <style>
        /* Style général des tableaux */
        .stDataFrame {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }

        /* En-tête du tableau */
        .stDataFrame thead {
            background-color: #4b8bff;
            color: white;
            font-weight: bold;
        }

        /* Lignes du tableau */
        .stDataFrame tbody tr:nth-child(even) {
            background-color: #f8f9fa;
        }

        .stDataFrame tbody tr:nth-child(odd) {
            background-color: #ffffff;
        }

        /* Effet de survol */
        .stDataFrame tbody tr:hover {
            background-color: #e9ecef;
            transition: background-color 0.3s ease;
        }

        /* Cellules */
        .stDataFrame th, .stDataFrame td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }

        /* Style des colonnes */
        .stDataFrame th {
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 1px;
        }
        </style>
        """

title_css = """
        <style>
        .dashboard-title-container {
            background: linear-gradient(135deg, #ff4b4b 0%, #ff6b6b 100%);
            color: white;
            padding: 30px 20px;
            border-radius: 15px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            text-align: center;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }

        .dashboard-title-container:hover {
            transform: scale(1.02);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        }

        .dashboard-main-title {
            font-size: 2.5em;
            font-weight: 800;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .dashboard-subtitle {
            font-size: 1.2em;
            font-weight: 300;
            color: rgba(255,255,255,0.9);
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.6;
        }

        .title-icon {
            margin: 0 15px;
            opacity: 0.8;
        }
        </style>
        """

header_css = """
        <style>
        .header-container {
            background: linear-gradient(135deg, #ff4b4b 0%, #ff6b6b 100%);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .header-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255,255,255,0.1);
            transform: skew(-15deg) rotate(-15deg);
            z-index: 1;
        }

        .header-title {
            color: white;
            font-size: 2.5em;
            font-weight: 800;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            position: relative;
            z-index: 2;
        }

        .header-subtitle {
            color: rgba(255,255,255,0.9);
            font-size: 1.2em;
            font-weight: 300;
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
            line-height: 1.6;
            position: relative;
            z-index: 2;
        }

        .image-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }

        .image-wrapper {
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }

        .image-wrapper:hover {
            transform: scale(1.03);
        }
        </style>
        """

tabs_css="""
<style>
.stTabs [data-baseweb="tab-list"] {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: 
#f0f2f6;
    border-radius: 15px;
    padding: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.stTabs [data-baseweb="tab"] {
    padding: 10px 15px;
    margin: 0 5px;
    border-radius: 10px;
    transition: all 0.3s ease;
    font-weight: 500;
    color: 
#4a4a4a;
    background-color: transparent;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(75, 139, 255, 0.1);
    color: 
#4b8bff;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: 
#4b8bff;
    color: white;
    box-shadow: 0 4px 6px rgba(75, 139, 255, 0.3);
}

.stTabs [data-baseweb="tab"] svg {
    margin-right: 8px;
}
</style>
"""

global_font_css = """
        <style>
        /* Définit la taille de police par défaut pour toute la page */
        body, .stMarkdown, .stTextInput>div>div>input, .stSelectbox>div>div>select, 
        .stMultiSelect>div>div>div, .stDateInput>div>div>input, 
        .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
            font-size: 19px !important; /* Taille de police de base */
        }

        /* Styles pour différents types de texte */
        h1 { font-size: 2.5em !important; }  /* Titres principaux */
        h2 { font-size: 2em !important; }    /* Sous-titres */
        h3 { font-size: 1.5em !important; }  /* Titres de section */
        p, div, span { font-size: 19px !important; } /* Texte de paragraphe */

        /* Option pour ajuster la taille de police de manière responsive */
        @media (max-width: 600px) {
            body, .stMarkdown {
                font-size: 14px !important;
            }
        }
        </style>
        """

profile_css = """
        <style>
        .profile-container {
            background-color: #1e2736;
            border-radius: 15px;
            padding: 20px;
            color: white;
            display: flex;
            align-items: center;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            max-width: 600px;
            margin: 20px auto;
        }

        .profile-image {
            width: 150px;
            height: 150px;
            object-fit: cover;
            margin-right: 20px;
            border-radius: 10px; /* Légèrement arrondi si souhaité */
        }

        .profile-content {
            flex-grow: 1;
        }

        .profile-name {
            font-size: 1.8em;
            color: #4b8bff;
            margin-bottom: 5px;
        }

        .profile-title {
            font-size: 1em;
            color: #a0a0a0;
            margin-bottom: 10px;
        }
        </style>
        """

button_style = """
            <style>
            div[data-baseweb="segmented-control"] > div {
                background-color: #f0f2f6;  /* Couleur de fond */
                border-radius: 10px;  /* Coins arrondis */
                padding: 5px;
            }
            
            div[data-baseweb="segmented-control"] button {
                color: white !important;  /* Couleur du texte */
                background-color: #4CAF50 !important;  /* Couleur de fond des boutons */
                border-radius: 8px !important;  /* Arrondi des boutons */
                padding: 10px 20px !important;  /* Espacement interne */
                font-weight: bold !important;
            }

            div[data-baseweb="segmented-control"] button:hover {
                background-color: #45a049 !important;  /* Couleur au survol */
            }
            </style>
            """

            # Custom CSS for beautiful effects and styling
custom_effects_css = """
            <style>
            /* Beautiful gradient animations */
            @keyframes gradient {
                0% {background-position: 0% 50%;}
                50% {background-position: 100% 50%;}
                100% {background-position: 0% 50%;}
            }

            /* Cards and containers styling */
            .stCard {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 1.5rem;
                box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.18);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .stCard:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 40px rgba(31, 38, 135, 0.25);
            }

            /* Button styling */
            .stButton > button {
                background: linear-gradient(45deg, #4b8bff, #7b5fff);
                border: none;
                border-radius: 10px;
                color: white;
                padding: 0.6em 1.2em;
                font-weight: 600;
                transition: all 0.3s ease;
            }

            .stButton > button:hover {
                background: linear-gradient(45deg, #7b5fff, #4b8bff);
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(123, 95, 255, 0.4);
            }

            /* Selectbox styling */
            .stSelectbox > div > div > select {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                padding: 0.5em;
                transition: all 0.3s ease;
            }

            .stSelectbox > div > div > select:focus {
                border-color: #4b8bff;
                box-shadow: 0 0 0 2px rgba(75, 139, 255, 0.2);
            }

            /* Metric styling */
            .stMetric {
                background: linear-gradient(135deg, #f6f9fe 0%, #f1f4f9 100%);
                border-radius: 15px;
                padding: 1rem;
                border: 1px solid #e0e6ed;
                transition: all 0.3s ease;
            }

            .stMetric:hover {
                transform: scale(1.02);
                box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            }

            /* Slider styling */
            .stSlider > div > div {
                color: #4b8bff;
            }

            .stSlider > div > div > div > div {
                background-color: #4b8bff;
            }

            /* Custom scrollbar */
            ::-webkit-scrollbar {
                width: 10px;
                height: 10px;
            }

            ::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 5px;
            }

            ::-webkit-scrollbar-thumb {
                background: #4b8bff;
                border-radius: 5px;
            }

            ::-webkit-scrollbar-thumb:hover {
                background: #7b5fff;
            }

            /* Text highlights */
            ::selection {
                background: rgba(75, 139, 255, 0.3);
            }

            /* Loading animation */
            .stSpinner > div {
                border-color: #4b8bff transparent transparent;
            }

            /* Progress bar */
            .stProgress > div > div > div {
                background-color: #4b8bff;
                background-image: linear-gradient(45deg, 
                    rgba(255,255,255,.15) 25%, 
                    transparent 25%, 
                    transparent 50%, 
                    rgba(255,255,255,.15) 50%, 
                    rgba(255,255,255,.15) 75%, 
                    transparent 75%, 
                    transparent);
                background-size: 1rem 1rem;
                animation: progress-bar-stripes 1s linear infinite;
            }

            @keyframes progress-bar-stripes {
                from {background-position: 1rem 0}
                to {background-position: 0 0}
            }
            </style>
            """

st.markdown(custom_effects_css, unsafe_allow_html=True)
st.markdown(global_font_css, unsafe_allow_html=True)
        #=======================================================================
        #================== Sélecteur de langue ================================


def set_language():
    return st.sidebar.selectbox("🌍 Choisissez la langue / Choose the language", ["", "Français", "English"])


def main():
    #st.write("Autre approche: Au cas ou la première approche ne marche pas, inscrivez vous dans l'onglet connexion ci contre et utiliser vos identifiants pour vous connecter")
    st.markdown(tabs_css, unsafe_allow_html=True)
    is_authenticated = authentication_system("Controleur")
    if is_authenticated:

        user = st.session_state['username']

        st.markdown(sidebar_css, unsafe_allow_html=True)
        st.markdown(useless_style, unsafe_allow_html=True)
        st.markdown(title_css, unsafe_allow_html=True)
        st.markdown(header_css, unsafe_allow_html=True)
        st.markdown(profile_css, unsafe_allow_html=True)
        st.markdown(table_css, unsafe_allow_html=True)
        st.markdown(button_style, unsafe_allow_html=True)
        st.markdown(global_font_css, unsafe_allow_html=True)
        lang = set_language()
        lang1="Français" if lang=="" else lang
        
        
        
        
        def load_data():
            download_ftp_files()
            Unzip_All_Files()
            
            #Maping (remplacement des codes par les valeurs) des données
            df_eleve=extrat_eleve()
            a=[dico_colonne_eleve[col] for col in df_eleve.columns]
            df_eleve.columns=a
            df_eleve["Type"]="Elève"
            df_eleve["Région"]=df_eleve["Région"].replace(dico_eleve_enseignant["Région"])
            df_eleve["Etablissement"]=df_eleve["Etablissement"].replace(dico_eleve_enseignant["Etablissement"])
            df_eleve["Département"]=df_eleve["Département"].replace(dico_eleve_enseignant["Departement"])
            df_eleve["Résultat"]=df_eleve["Résultat"].replace(dico_eleve_enseignant["Resultat"])
            df_eleve["Date"]=pd.to_datetime(df_eleve["Date"],format='%Y%m%d',errors='coerce').dt.date
            df_eleve=df_eleve[["Etablissement","Région","Localité","Superviseur","Controleur","Enqueteur","Date","Résultat","Autre Résultat","Disponibilité","Heure debut","Heure fin","Type"]]
            df_eleve["Longitude"]=None
            df_eleve["Latitude"]=None
            
            
            
            df_enseignant=extrat_enseignant()
            a=[dico_colonne_ens[col] for col in df_enseignant.columns]
            df_enseignant.columns=a
            df_enseignant["Type"]="Enseignant"
            df_enseignant["Région"]=df_enseignant["Région"].replace(dico_eleve_enseignant["Région"])
            df_enseignant["Etablissement"]=df_enseignant["Etablissement"].replace(dico_eleve_enseignant["Etablissement"])
            df_enseignant["Département"]=df_enseignant["Département"].replace(dico_eleve_enseignant["Departement"])
            df_enseignant["Résultat"]=df_enseignant["Résultat"].replace(dico_eleve_enseignant["Resultat"])
            df_enseignant["Date"]=pd.to_datetime(df_enseignant["Date"],format='%Y%m%d',errors='coerce').dt.date
            df_enseignant=df_enseignant[["Etablissement","Région","Localité","Superviseur","Controleur","Enqueteur","Date","Résultat","Autre Résultat","Disponibilité","Heure debut","Heure fin","Type","Longitude","Latitude"]]
            
            
            df_maire=extrat_maire()
            a=[dico_colonne_maire[col] for col in df_maire.columns]
            df_maire.columns=a
            df_maire["Type"]="Maire"
            df_maire["Région"]=df_maire["Région"].replace(dico_maire["Région"])
            df_maire["Etablissement"]=df_maire["Etablissement"].replace(dico_maire["Etablissement"])
            df_maire["Département"]=df_maire["Département"].replace(dico_maire["Departement"])
            df_maire["Résultat"]=df_maire["Résultat"].replace(dico_eleve_enseignant["Resultat"])
            df_maire["Date"]=pd.to_datetime(df_maire["Date"],format='%Y%m%d',errors='coerce').dt.date
            df_maire["Etablissement"]=None
            df_maire=df_maire[["Etablissement","Région","Localité","Superviseur","Controleur","Enqueteur","Date","Résultat","Autre Résultat","Disponibilité","Heure debut","Heure fin","Type","Longitude","Latitude"]]
            
            
            df_ec_maire=extrat_ecole_maire()
            a=[dico_colonne_ec[col] for col in df_ec_maire.columns]
            df_ec_maire.columns=a
            df_ec_maire["Type"]="Ecole-Maire"
            df_ec_maire["Région"]=df_ec_maire["Région"].replace(dico_maire["Région"])
            df_ec_maire["Etablissement"]=df_ec_maire["Etablissement"].replace(dico_maire["Etablissement"])
            df_ec_maire["Département"]=df_ec_maire["Département"].replace(dico_maire["Departement"])
            df_ec_maire["Résultat"]=df_ec_maire["Résultat"].replace(dico_eleve_enseignant["Resultat"])
            df_ec_maire["Code Commune"]=df_ec_maire["Code Commune"].replace(dico_maire["Commune"])
            df_ec_maire=df_ec_maire.rename(columns={"Code Commune":"Localité"})
            df_ec_maire["Date"]=pd.to_datetime(df_ec_maire["Date"],format='%Y%m%d',errors='coerce').dt.date
            df_ec_maire=df_ec_maire[["Etablissement","Région","Localité","Superviseur","Controleur","Enqueteur","Date","Résultat","Autre Résultat","Disponibilité","Heure debut","Heure fin","Type"]]
            df_ec_maire["Longitude"]=None
            df_ec_maire["Latitude"]=None
            
            
            df_chef=extrat_chef()
            a=[dico_colonne_ch[col] for col in df_chef.columns]
            df_chef.columns=a
            df_chef["Type"]="Chefferie"
            df_chef["Région"]=df_chef["Région"].replace(dico_maire["Région"])
            df_chef["Etablissement"]=df_chef["Etablissement"].replace(dico_maire["Etablissement"])
            df_chef["Département"]=df_chef["Département"].replace(dico_maire["Departement"])
            df_chef["Résultat"]=df_chef["Résultat"].replace(dico_eleve_enseignant["Resultat"])
            df_chef["Date"]=pd.to_datetime(df_chef["Date"],format='%Y%m%d',errors='coerce').dt.date
            df_chef=df_chef[["Etablissement","Région","Localité","Superviseur","Controleur","Enqueteur","Date","Résultat","Autre Résultat","Disponibilité","Heure debut","Heure fin","Type","Longitude","Latitude"]]
            
            final_df=pd.concat([df_chef,df_ec_maire,df_maire,df_enseignant,df_eleve],ignore_index=True)
            
            final_df.to_excel('DataGood.xlsx', index=False)
            
            #fusion avec le shape file
            
            data_shp=gpd.read_file("Cameroun.shp")
            region_mapping = {
                                'ADAMAOUA': 'Adamaoua',
                                'CENTRE': 'Centre',
                                'EST': 'Est',
                                'EXTREME-NORD': 'Extrême-Nord',
                                'LITTORAL': 'Littoral',
                                'NORD': 'Nord',
                                'NORD-OUEST': 'Nord-Ouest',
                                'OUEST': 'Ouest',
                                'SUD': 'Sud',
                                'SUD-OUEST': 'Sud-Ouest'
                            }
            
            data_shp['Nom_Régio']=data_shp['Nom_Régio'].replace(region_mapping)
            data_shp=data_shp[["Nom_Régio", "geometry"]]
            data_shp=data_shp.rename(columns={"Nom_Régio":"Région"})  
            geo_df=data_shp.merge(final_df, on="Région", how="inner")
            geo_df=gpd.GeoDataFrame(geo_df, geometry="geometry")
            geo_df.to_file("geo_data.shp")
            
            last_update=datetime.now()
            return final_df, geo_df,  last_update
        # Test pour le chargegement et la récupération
        
        
        
        # ===================================================
        
        @st.cache_data()
        def load_data2():
            All_data=pd.read_excel("DataGood.xlsx")
            data_rep=pd.read_excel("ECHANTILLON.xlsx")
            All_data["Date"]=All_data["Date"].dt.date
            
            All_data["Superviseur"] = "S_" + All_data["Superviseur"].astype(str)
            All_data["Enqueteur"] = "E_" + All_data["Enqueteur"].astype(str)
            All_data["Temp"]=round((All_data["Heure fin"]-All_data["Heure debut"])/60,2)
            
            rep_region=pd.DataFrame(data_rep["SRegion"].value_counts())
            rep_sup=pd.DataFrame(data_rep["SUP"].value_counts())
            
            return All_data, data_rep, rep_region, rep_sup
        
        
        All_data, data_rep, rep_region, rep_sup = load_data2()
       
        enq_data=pd.read_excel("Simulation.xlsx",sheet_name="Données Collectées")
        
        
        enq_data_rep=pd.read_excel("Simulation.xlsx",sheet_name="Distribution Ménages")
        C_enq_data=enq_data[enq_data["id_controleur"]==user]
        
        # Conversion des colonnes heure_debut et heure_fin en objets datetime.time
        C_enq_data['heure_debut'] = pd.to_datetime(C_enq_data['heure_debut'], format='%H:%M:%S').dt.time
        C_enq_data['heure_fin'] = pd.to_datetime(C_enq_data['heure_fin'], format='%H:%M:%S').dt.time

        # Création d'une colonne datetime combinant date_collecte et heure_debut/heure_fin
        C_enq_data['datetime_debut'] = C_enq_data.apply(lambda row: pd.Timestamp.combine(row['date_collecte'], row['heure_debut']), axis=1)
        C_enq_data['datetime_fin'] = C_enq_data.apply(lambda row: pd.Timestamp.combine(row['date_collecte'], row['heure_fin']), axis=1)

        # Calcul du temps de remplissage en minutes
        C_enq_data['temps_remplissage'] = (C_enq_data['datetime_fin'] - C_enq_data['datetime_debut']).dt.total_seconds() / 60

        C_enq_data_rep=enq_data_rep[enq_data_rep["id_controleur"]==user]
        
        form = gpd.read_file("Arrondissement.shp")
        form = form.rename(columns={"arrondisse":"arrondissement"})
        geo_data=form.merge(C_enq_data, on="arrondissement", how="left")
        geo_data= gpd.GeoDataFrame(geo_data, geometry='geometry')
        
        geo_data_rep=form.merge(C_enq_data_rep, on="arrondissement", how="left")
        geo_data_rep= gpd.GeoDataFrame(geo_data_rep, geometry='geometry')
       
        
        # Create a dictionary of dictionaries
        role_counts = {
            "Superviseur": data_rep["SUP"].value_counts().to_dict(),
            "Contrôleur": data_rep["CTR"].value_counts().to_dict(),
            "Enquêteur": data_rep["ENQ"].value_counts().to_dict()
        }

        charge_equeteur=data_rep["ENQ"].value_counts()
        charge_controleur=data_rep["CTR"].value_counts()
        charge_superviseur=data_rep["SUP"].value_counts()
        
        All_data['Total_enfa'] = np.where(All_data['Type'] == 'Enfant', 1, 0)
        All_data['Total_ense'] = np.where(All_data['Type'] == 'Enseignant', 1, 0)
        logo=Image.open("Logo_ISSEA.png")
        logo2=Image.open("Logo_ISSEA.png")
        cl_tb=st.columns([1,7,1])
        
        #============ESPACE DE MISE A JOUR=======================================
        col_fonfig=st.columns(2)
        last_update=None
        with col_fonfig[0]:
            upload_bt=st.button("Mettre à jour")
            if upload_bt:
                with st.spinner("Téléchargement des nouvelles données...",show_time=True):
                    All_data, geo_data, last_update =load_data()
                    #All_data["Date"]=All_data["Date"].dt.date
        
                    All_data["Superviseur"] = "S_" + All_data["Superviseur"].astype(str)
                    All_data["Enqueteur"] = "E_" + All_data["Enqueteur"].astype(str)
                    All_data["Temp"]=round((All_data["Heure fin"]-All_data["Heure debut"])/60,2)
                    
                    All_data['Total_enfa'] = np.where(All_data['Type'] == 'Enfant', 1, 0)
                    All_data['Total_ense'] = np.where(All_data['Type'] == 'Enseignant', 1, 0)
                    
                    rep_region=pd.DataFrame(data_rep["SRegion"].value_counts())
                    rep_sup=pd.DataFrame(data_rep["SUP"].value_counts())
                    st.success("Mise à jour effectuée.")
        with col_fonfig[1]:
            st.markdown(f"""
                <div style="
                    background: linear-gradient(45deg, #4b8bff, #7b5fff);
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                    text-align: center;
                    font-weight: 1300;
                    animation: pulse 2s infinite;
                ">
                    <span style="font-size: 5.2em;">
                        <span style="color: #FFE5E5;">🔄 Dernière mise à jour : </span>
                        <span style="color: #FFFFFF;">{last_update.strftime("%d/%m/%Y %H:%M:%S") if last_update else "Aucune mise à jour"}</span>
                    </span>
                </div>
                
            """, unsafe_allow_html=True)
        
        
        
        
        #Table de donneés
        #C_enq_data
        
        
        
        #progression par enqueteur
        a_test=pd.DataFrame(C_enq_data["id_enqueteur"].value_counts())
        b_test=pd.DataFrame(C_enq_data_rep["id_enqueteur"].value_counts())
                
                # Agrégation des deux tables a_test et b_test sur "id_enqueteur"
        agg_test = a_test.join(b_test, how="outer", lsuffix="_collecte", rsuffix="_distribution")
        agg_test.reset_index(inplace=True)
        agg_test.rename(columns={"index": "id_enqueteur"}, inplace=True)
                # Ajout de la colonne progression
        agg_test["progression"] = agg_test["count_collecte"] / (agg_test["count_distribution"] )
        
        #==========================================================================
        
        with cl_tb[0]:
            st.image(logo,caption="INSTITUT NATIONAL DE LA STATISTIQUE",width=165)
        with cl_tb[1]:
            st.markdown(
            f"""
            <div class="dashboard-title-container" style="background-color: #3717BF;">
                <h1 class="dashboard-main-title"> 
                <img src="https://cdn-icons-png.flaticon.com/512/190/190411.png" alt="Icon" class="title-icon" width="50" height="50">
                {traduire_texte("Tableau de Bord Pour le suivi de la collecte sur l'enquête du ACADEMIQUE", lang)}
                </h1>
                <p class="dashboard-subtitle"> 
                {"ISSEA - Enquête "}
                </p>
            </div>
            """,
            unsafe_allow_html=True)
        with cl_tb[2]:
            st.image(logo2,caption="",width=165)
        la_date=st.sidebar.date_input(traduire_texte("Sélectionner la date de collecte",lang),dt.datetime(2025, 5, 20).date(),min_value=dt.datetime(2023, 1, 1).date(),max_value=dt.datetime(2025, 12, 31).date())
        All_data["Date"]=pd.to_datetime(All_data["Date"], format="%d/%m/%Y")
        #data=data[data["Date_Colle"]<=la_date.strftime("%Y-%m-%d")]
        
        data_to_plot=All_data
        tabs = st.tabs([
            f"📈 {traduire_texte('ANALYSE GENERALE', lang)}", 
            f"📊 {traduire_texte('PERFORMANCE ET QUALITE DES DONNEES', lang)}"
            ])
        
        with tabs[0]:
            ca=st.columns(3)

            
            with ca[0]:
                display_single_metric_advanced(" 💰Tontine", 25, delta=2.25, color_scheme="blue")
            with ca[1]:
                display_single_metric_advanced(" 🗑️ Dechets menagers", 159, delta=13, color_scheme="green")
            with ca[2]:
                display_single_metric_advanced("Total", 184, delta=7.2, color_scheme="orange")
            st.write('')  
            col=st.columns([5.3,4.7])
            
            with col[0] :
                progress_all=C_enq_data.shape[0]/C_enq_data_rep.shape[0]
                st.write("")
                sublcb1=st.columns(2)
                
                with sublcb1[0]:
                    make_progress_char(progress_all,couleur="",titre=traduire_texte("Progression de la collecte",lang))
                with sublcb1[1]:
                    make_progress_char(0.0568,couleur="",titre=traduire_texte("Taux de non-reponse",lang))
                    st.write("")
                
                total_charge=[]
                for j in range(len(All_data["Région"].unique())):
                    reg=All_data["Région"].unique()[j]
                    el=[[reg,"Elève"] for i in range(1,18*rep_region["count"][reg]+1)]
                    ens=[[reg,"Enseignant"] for i in range(1,3*rep_region["count"][reg]+1)]
                    charge=el + ens + [[reg, "Chefferie"]] + [[reg, "Mairie"] for i in range(1,rep_region["count"][reg]+1)] + [[reg, "Ecole-Mairie"] for i in range(1,rep_region["count"][reg]+1)]
                    total_charge += charge
                total_charge=pd.DataFrame(total_charge, columns=["Région", "Type"])
                
                
                df_progress=agg_test[['id_enqueteur', 'count_collecte', 'count_distribution']]
                df_progress=df_progress.set_index('id_enqueteur')
                df_progress=df_progress.rename(columns={'count_collecte': 'Nombre de ménages collectés', 'count_distribution': 'Nombre de ménages distribués'})
                create_bar_chart_from_contingency(df_progress,
                                    title="Répartition et charge accomplie des enqueteurs",
                                    colors=['#1abc9c', '#34495e', '#e67e22'],
                                    orientation="vertical",
                                    var1_name="Code enqueteur",
                                    var2_name="Nombre de ménages",
                                    height="400px")
                    
            with col[1]:
                
                make_multi_progress_bar(agg_test['id_enqueteur'],agg_test['progression'],colors=palette[0:11],titre=traduire_texte("Progression par Enqueteur",lang),height=700)

            cl_config_cart=st.columns([1,1,1,2])
            with cl_config_cart[0]:
                opacity=st.slider(traduire_texte("Opacité de la carte",lang), 0.0, 1.0, value=0.5)
            with cl_config_cart[1]:  
                type_questionnaire=st.selectbox("Type de Questionnaire", options=All_data["Type"].unique())
            with cl_config_cart[2]:
                style_carte=st.selectbox(traduire_texte("Style de la carte",lang), ["carto-positron", "carto-darkmatter", "open-street-map", "CartoDB positron", "CartoDB dark_matter"])  
            with cl_config_cart[3]:
                enqueteur=st.multiselect(traduire_texte("Sélectionner les enqueteurs",lang), options=C_enq_data["id_enqueteur"].unique(), default=C_enq_data["id_enqueteur"].unique())
            
            col_map=st.columns(2)
            with col_map[0]:
                # Données de points
                geo_data_to_plot= geo_data[geo_data["id_enqueteur"].isin(enqueteur) ]
                st.subheader(traduire_texte("Carte de la position des ménages enquétés",lang))
                create_categorical_map(geo_data_to_plot, lat_col="latitude", lon_col="longitude", category_col="id_enqueteur", 
                          center_lat=None, center_lon=None, zoom_start=12,
                          popup_cols=None, tooltip_cols=None)
                
            with col_map[1]:
                geo_data_rep_to_plot= geo_data_rep[geo_data_rep["id_enqueteur"].isin(enqueteur)]
                st.subheader(traduire_texte("Disposition des ménages à enquéter",lang))
                create_categorical_map(geo_data_rep_to_plot, lat_col="latitude", lon_col="longitude", category_col="id_enqueteur", 
                          center_lat=None, center_lon=None, zoom_start=12,
                          popup_cols=None, tooltip_cols=None)
            
        with tabs[1]:
            col1=st.columns([1,1])
            with col1[0]:
                sbcl=st.columns([1,1])
                with sbcl[0]:
                    select_enq=st.selectbox(traduire_texte("Sélectionner le Superviseur",lang),C_enq_data["id_enqueteur"].unique())
                    data_superviz=All_data[All_data["Superviseur"]==select_enq]   
                    
                    display_single_metric_advanced(" Total", 12, delta=round(100*0.678 , 2), color_scheme="teal")
                st.write("")
                with sbcl[1]:
                   make_progress_char(0.678,couleur="",titre=traduire_texte("Progression de la collecte",lang))
                   
                
                
            st.write("")
            with col1[1]:
                box_fig = px.box(C_enq_data, x="id_enqueteur", y="temps_remplissage", color="id_enqueteur",
                                    title=traduire_texte("Distribution du temps de remplissage en minute par enquêteur", lang),
                                    height=400)
                st.plotly_chart(box_fig)
                
                
            tcol=st.columns(2)
            with tcol[0]:
                enq_for_heat_map=st.multiselect(traduire_texte("Sélectionner un (des) enquêteur (s)",lang),C_enq_data["id_enqueteur"].unique(),default=C_enq_data["id_enqueteur"].unique(), key="Enq_for_map")
            with tcol[1]:
                enq_type=st.multiselect(traduire_texte("Sélectionner un type de questionnaire",lang),data_to_plot["Type"].unique(), default=data_to_plot["Type"].unique()[1])
            data_superviz_heat_map=data_to_plot[(data_to_plot["Enqueteur"].isin(enq_for_heat_map)) & (data_to_plot["Type"].isin(enq_type))]
            cross_enq=pd.crosstab(data_superviz_heat_map["Enqueteur"],data_superviz_heat_map["Date"])
            make_st_heatmap_echat2(cross_enq,title=traduire_texte("Charge de travail accomplie par enquêteur",lang)) if data_superviz_heat_map.shape[0]>0 else None
            
            
            cltime=st.columns([2.5,9])
            with cltime[0]:
                time_type=st.selectbox("Choississez un type de questionnaire", options=All_data["Type"].unique())
            with cltime[1]:
                Sup_time=st.multiselect("SUPERVISEUR", options=All_data["Superviseur"].unique(), default=All_data["Superviseur"].unique())
            time_All_data=All_data[All_data["Superviseur"].isin(Sup_time)]
            time_All_data=All_data[All_data["Type"]==time_type]
            time_distribution=px.box(time_All_data,y="Temp",x="Enqueteur",color="Résultat",title=traduire_texte(f"Distribution des temps de remplissage (en minutes) du questionnaire {time_type} par enquêteur",lang))
            st.plotly_chart(time_distribution)
        
if __name__ == "__main__":
    main()     