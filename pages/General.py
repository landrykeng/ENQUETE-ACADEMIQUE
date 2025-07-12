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
    if 0==0:


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
        
        
        # ===================================================
        
        data=pd.read_excel("data_collected.xlsx")
        data=data.drop("Unnamed: 0",axis=1)
        data=data.drop_duplicates()
        #data=data.drop_duplicates(["id_menage","Duree_interview","arrondissement"])
        data["Date"]=data["Date"].dt.date
        data['arrondissement'] = data['arrondissement'].str.replace('Yaounde', 'Yaoundé', regex=False)
        fichier=Path("data_collected.xlsx")
        date_up_date = datetime.fromtimestamp(fichier.stat().st_mtime)
        
        data['distance_m'] = data.apply(lambda row: haversine(
                                                            row['Longitude_GPS_Couverture'],
                                                            row['Latitude_GPS_Couverture'],
                                                            row['Longitude_collected'],
                                                            row['Latitude_collected']
                                                        ), axis=1)

        # Créer la variable good_hh
        data['good_hh'] = (data['distance_m'] > 100).astype(int)

        
        data_rep=pd.read_excel("Repartition.xlsx",sheet_name="Repatition")
        data_rep['arrondissement'] = data_rep['arrondissement'].str.replace('Yaounde', 'Yaoundé', regex=False)
        data["Rejets_superviseur"]=data["Rejets_superviseur"].map({1:"Rejeté par les controleur", 0: "Approuvé par le Controleur"})
        data["Rejets_siege"]=data["Rejets_siege"].map({1:"Rejeté par le QG", 0: "Approuvé par le QG"})
        
        

        
        
        form = gpd.read_file("Arrondissement.shp")
        form = form.rename(columns={"arrondisse":"arrondissement"})
        geo_data=form.merge(data, on="arrondissement", how="left")
        geo_data= gpd.GeoDataFrame(geo_data, geometry='geometry')
        
        geo_data_rep=form.merge(data_rep, on="arrondissement", how="left")
        geo_data_rep= gpd.GeoDataFrame(geo_data_rep, geometry='geometry')

        #data
        #geo_data
        
        
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
                    pass
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
                        <span style="color: #FFFFFF;">{date_up_date.strftime("%Y-%m-%d %H:%M:%S")}</span>
                    </span>
                </div>
                
            """, unsafe_allow_html=True)
        
        
        
        
        #Table de donneés
        #data
        
        
        
        
        # Remplacer les valeurs manquantes de la colonne count_collecte par 0
        #data_arr
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

        tabs = st.tabs([
            f"📈 {traduire_texte('ANALYSE GENERALE', lang)}", 
            f"💫 {traduire_texte('A propos', lang)}"
            ])
        
        with tabs[0]:
            with st.expander("Description des indicateurs"):
                
                st.subheader("1. Les questionnaire soumis sont ceux achevé par les enquêteurs en attente d'approbation des controleurs")
                st.subheader("2. Les Questionnaire Validé par les controleur sont les questionnaire en attente d'approbation du QG. ")
                st.subheader("3. Les questionnaire approuvé par le QG sont les questionnaires définitifs: à la fin de l'enquête, tous les questionnaires doivent avoir ce statut")
            
            st.title("SECTION1: STATISTIQUES SUR LES QUESTIONNAIRES SOUMIS")
            ca=st.columns(3)
            
            nb_tontine = (data['Questionnaire'] == 'Tontine').sum()
            nb_dechet = (data['Questionnaire'] == 'Dechet').sum()
            
            rep_tontine=(data_rep['questionnaire'] == 'Tontine').sum()
            rep_dechet=(data_rep['questionnaire'] == 'Dechet').sum()
            
            with ca[0]:
                display_single_metric_advanced(" 💰Tontine",nb_tontine, delta=round(100*nb_tontine/rep_tontine,2), color_scheme="blue")
            with ca[1]:
                display_single_metric_advanced(" 🗑️ dechet menagers", nb_dechet, delta=round(100*nb_dechet/rep_dechet,2), color_scheme="green")
            with ca[2]:
                display_single_metric_advanced("Total", nb_dechet+nb_tontine, delta=round(100*(nb_dechet+nb_tontine)/(rep_tontine+rep_dechet),2), color_scheme="orange")
            st.write('')  
            col=st.columns([5.3,4.7])
            
            with col[0] :
                Type_questionnaire=st.multiselect("Thème de l'enquête", options=data["Questionnaire"].unique(),default=data["Questionnaire"].unique())
                
                if len(Type_questionnaire)==0:
                    df_to_plot=data
                    df_rep_to_plot=data_rep
                else:
                    df_to_plot=data[data["Questionnaire"].isin(Type_questionnaire)]
                    df_rep_to_plot=data_rep[data_rep["questionnaire"].isin(Type_questionnaire)]
                
                #progression par enqueteur
                a_test=pd.DataFrame(df_to_plot["arrondissement"].value_counts())
                b_test=pd.DataFrame(df_rep_to_plot["arrondissement"].value_counts())
                        
                        # Agrégation des deux tables a_test et b_test sur "id_enqueteur"
                data_arr = a_test.join(b_test, how="outer", lsuffix="_collecte", rsuffix="_distribution")
                data_arr.reset_index(inplace=True)
                data_arr.rename(columns={"index": "id_enqueteur"}, inplace=True)
                        # Ajout de la colonne progression
                data_arr["count_collecte"] = data_arr["count_collecte"].fillna(0)
                data_arr["progression"] = data_arr["count_collecte"] / (data_arr["count_distribution"] )
                
                progress_all=df_to_plot.shape[0]/df_rep_to_plot.shape[0]
                st.write("")
                sublcb1=st.columns(2)
                
                with sublcb1[0]:
                    make_progress_char(progress_all,couleur="",titre=traduire_texte("Progression de la collecte",lang))
                with sublcb1[1]:
                    time_std=round(data["Duree_interview"].std())
                    time_mean=round(data["Duree_interview"].mean())
                    create_questionnaire_time_gauge(time_mean, time_std, temps_cible=None, titre="Durée des interviews")
                    #nb_missing_longitude = df_to_plot["Longitude_collected"].isna().sum()
                    #make_progress_char((df_to_plot.shape[0]-nb_missing_longitude)/df_to_plot.shape[0],couleur="",titre=traduire_texte("Taux de localisation des ménages",lang))
                    st.write("")
                
                
                
                df_progress=data_arr[['arrondissement', 'count_collecte', 'count_distribution']]
                df_progress=df_progress.set_index('arrondissement')
                df_progress=df_progress.rename(columns={'count_collecte': 'Nombre de questionnaire soumis', 'count_distribution': 'Nombre de ménages distribués'})
                create_bar_chart_from_contingency(df_progress,
                                    title="Répartition et charge accomplie par arrondissement",
                                    colors=['#1abc9c', '#34495e', '#e67e22'],
                                    orientation="vertical",
                                    var1_name="Code enqueteur",
                                    var2_name="Nombre de ménages",
                                    height="400px")
                    
            with col[1]:
                
                make_multi_progress_bar_echart(data_arr['arrondissement'],data_arr['progression'],colors=palette[0:11],titre=traduire_texte("Progression par arrondissement",lang),height=500)
                create_pie_chart_from_df(data, "Resultat_collecte", style="donut", title="Statut global", colors=None,cle="sdhkdil")
            
            cb=st.columns(2)
            with cb[0]:
                create_pie_chart_from_df(data, "Appreciation_qualite_interview", style="donut", title="Appréciation Generale", colors=None,) 
            
            with cb[1]:
                data_qest=data.groupby("id_enqueteur").agg({"Nb_questions_sans_reponse":"size"})
                mean_qst_sans_rep=round(data_qest["Nb_questions_sans_reponse"].mean())
                std_qst_sans_rep=round(data_qest["Nb_questions_sans_reponse"].mean())
                create_missing_questions_gauge(mean_qst_sans_rep, std_qst_sans_rep, total_questions=None, 
                                 objectif_max=None, titre="Total Questions Sans Réponse", cle="jhdskj")
            st.title("SECTION 2: STATISTIQUES SUR LES QUESTIONNAIRES VALIDES PAR LE QG ET LES CONTROLEURS")

            data_qg=data[data["Statut"]!="Soumis"]
            ca2=st.columns(3)
            nb_tontine_qg = data_qg[data_qg['Questionnaire'] == 'Tontine'].shape[0]
            nb_dechet_qg = data_qg[data_qg['Questionnaire'] == 'Dechet'].shape[0]
            
            rep_tontine_qg=data_rep[data_rep['questionnaire'] == 'Tontine'].shape[0]
            rep_dechet_qg=data_rep[data_rep['questionnaire'] == 'Dechet'].shape[0]
            
            with ca2[0]:
                display_single_metric_advanced(" 💰Tontine",nb_tontine_qg, delta=round(100*nb_tontine_qg/rep_tontine_qg,2), color_scheme="blue")
            with ca2[1]:
                display_single_metric_advanced(" 🗑️ dechet menagers", nb_dechet_qg, delta=round(100*nb_dechet_qg/rep_dechet_qg,2), color_scheme="green")
            with ca2[2]:
                display_single_metric_advanced("Total", nb_dechet_qg+nb_tontine_qg, delta=round(100*(nb_dechet_qg+nb_tontine_qg)/(rep_tontine_qg+rep_dechet_qg),2), color_scheme="orange")
            st.write('')  
            
            c2=st.columns(2)
            
            with c2[0]:
                Type_questionnaire2=st.multiselect("Thème de l'enquête", options=data["Questionnaire"].unique(),default=data["Questionnaire"].unique(),key="Type2")
                df_to_plot=df_to_plot[df_to_plot["Questionnaire"].isin(Type_questionnaire2)]
                #create_bar_chart(data, "Statut", title="Statut des questionnaires", color="#181ce2", width="100%", height="400px",orientation="vertical")
                create_crossed_bar_chart(df_to_plot, "Statut", "Questionnaire", title="Statut des questionnaires", colors=["#41be0f","#e78608","#0b58e6"],width="105%", height="500px",orientation="vertical",)
            with c2[1]:
                pass
                create_crossed_bar_chart(df_to_plot, "arrondissement", "Statut", title="Diagramme des validations", colors=["#41be0f","#e78608","#0b58e6"],width="100%", height="500px",orientation="vertical",)
            
            
            
            
            
            
            arr=st.multiselect(traduire_texte("Sélectionner les arrondissement",lang), options=data["arrondissement"].unique(), default=data["arrondissement"].unique())
            
            df_qg=data_qg[data_qg["Questionnaire"].isin(Type_questionnaire2)]
            df_qg_rep=data_rep[data_rep["questionnaire"].isin(Type_questionnaire2)]
            
            a_test=pd.DataFrame(df_qg["arrondissement"].value_counts())
            b_test=pd.DataFrame(df_qg_rep["arrondissement"].value_counts())
                        
            # Agrégation des deux tables a_test et b_test sur "id_enqueteur"
            data_arr_qg = a_test.join(b_test, how="outer", lsuffix="_collecte", rsuffix="_distribution")
            data_arr_qg.reset_index(inplace=True)
            data_arr_qg.rename(columns={"index": "arrondissement"}, inplace=True)
                        # Ajout de la colonne progression
            data_arr_qg["count_collecte"] = data_arr_qg["count_collecte"].fillna(0)
            data_arr_qg["progression"] = data_arr_qg["count_collecte"] / (data_arr_qg["count_distribution"] )
            col_map=st.columns(2)
            with col_map[0]:
                # Données de points
                data_arr_qg["label"] = (data_arr_qg["arrondissement"]).astype(str)+ ": "+(data_arr_qg["progression"] * 100).round(2).astype(str) + "%"
                geo_df_plot=data_arr_qg.merge(form, on="arrondissement",how="left")
                
                geo_data_to_plot= geo_df_plot[geo_df_plot["arrondissement"].isin(arr) ]
                st.subheader(traduire_texte("Cartographie de la progression",lang))
                create_choropleth_map(geo_data_to_plot, geometry_col='geometry', value_col='progression', 
                         label_col='label', zoom_start=10, colormap='Greens',
                         num_classes=5, title="Carte de la progression", 
                         legend_name="Nombre de questionnaires", popup_cols="progression", 
                         tooltip_format=None, width=800, height=600)
                
            with col_map[1]:
                st.subheader(traduire_texte(" progression réelle par arrondissemnt",lang))
                
                
                make_multi_progress_bar_echart(data_arr_qg['arrondissement'],data_arr_qg['progression'],colors=palette[0:11],titre=traduire_texte("Progression par arrondissement",lang),height=600, cle="gdksjh")
                

            st.header("EVOLUTION DE LA COLLECTE")
            data_evolution=data.copy()
            data_evolution["Date"] = data_evolution["Date"].astype(str)
            create_crossed_bar_chart(data_evolution, "Date", "Statut", title="evolution",width="100%", height="500px",orientation="vertical",)
            
            enq_for_heat_map=st.multiselect(traduire_texte("Sélectionner un (des) arrondissement (s)",lang),data["arrondissement"].unique(),default=data["arrondissement"].unique(), key="Enq_for_map")
           
                #enq_type=st.multiselect(traduire_texte("Sélectionner un type de questionnaire",lang),data_to_plot["Type"].unique(), default=data_to_plot["Type"].unique()[1])
            data_superviz_heat_map=data[(data["arrondissement"].isin(enq_for_heat_map))]
            cross_enq=pd.crosstab(data_superviz_heat_map["arrondissement"],data_superviz_heat_map["Date"])
            make_st_heatmap_echat2(cross_enq,title=traduire_texte("Charge de travail accomplie par arrondissement",lang)) if data_superviz_heat_map.shape[0]>0 else None
        
            st.title("SECTION 3: QUALITE ET APPRECIATION GENERALE DE LA COLLECTE")
            col1=st.columns([1,1])
            
            with col1[0]:
                sbcl=st.columns([1,1])
                with sbcl[0]:
                    
                    
                    
                        select_arr=st.selectbox(traduire_texte("Sélectionner un arrondissement",lang),data["arrondissement"].unique())
                        select_teme=st.multiselect("Choisir le (les) thème (s)", options=data["Questionnaire"].unique(), default=data["Questionnaire"].unique())
                        #progression par enqueteur
                        df_ar2=data[data["Questionnaire"].isin(select_teme)]
                        df_ar2_rep=data_rep[data_rep["questionnaire"].isin(select_teme)]
                        a_test2=pd.DataFrame(df_ar2["arrondissement"].value_counts())
                        b_test2=pd.DataFrame(df_ar2_rep["arrondissement"].value_counts())
                                
                                # Agrégation des deux tables a_test et b_test sur "id_enqueteur"
                        data_arr2 = a_test2.join(b_test2, how="outer", lsuffix="_collecte", rsuffix="_distribution")
                        data_arr2.reset_index(inplace=True)
                        data_arr2.rename(columns={"index": "id_enqueteur"}, inplace=True)
                                # Ajout de la colonne progression
                        data_arr2["count_collecte"] = data_arr2["count_collecte"].fillna(0)
                        data_arr2["progression"] = data_arr2["count_collecte"] / (data_arr2["count_distribution"] )
                        
                        data_select_arr=data[(data["arrondissement"]==select_arr)] if len(select_teme)==0 else data[(data["arrondissement"]==select_arr)&(data["Questionnaire"].isin(select_teme))] 
                        count_select_arr= data_arr2.loc[data_arr2['arrondissement']==select_arr,"count_collecte"].values[0]
                        progress_select_arr=data_arr2.loc[data_arr2['arrondissement']==select_arr,"progression"].values[0]
                    
                        display_single_metric_advanced(" Total", round(count_select_arr), delta=round(100*progress_select_arr , 2), color_scheme="teal")
                st.write("")
                    
                with sbcl[1]:
                        time_std_enq=round(data_select_arr["Duree_interview"].std())
                        time_mean_enq=round(data_select_arr["Duree_interview"].mean())
                        create_questionnaire_time_gauge(time_mean_enq, time_std_enq, temps_cible=None, titre="Durée des interviews",cle="jhckjdsk")
                    #make_progress_char(progress_select_enq,couleur="",titre=traduire_texte("Progression de la collecte",lang))
                st.write("")
                
                    
                with col1[1]:
                        box_fig = px.box(data, x="arrondissement", y="Duree_interview", color="arrondissement",
                                            title=traduire_texte("Distribution du temps de remplissage en minute par arrondissement", lang),
                                            height=400)
                        st.plotly_chart(box_fig)
            c3=st.columns(2)
            data_for=data[data["Questionnaire"].isin(select_teme)]
            with c3[0]:
                    make_cross_echart(data_for, "arrondissement", "Resultat_collecte", title="Resultat collecte", x_label_rotation=0, colors=None, 
                            height="400px", cle="cross_chart", normalize=False, 
                            show_percentages=True, chart_type="bar", stack_mode="total")
            with c3[1]:
                    make_cross_echart(data_for, "arrondissement", "Appreciation_qualite_interview", title="Appréciation de la collecte", x_label_rotation=0, 
                            height="400px", cle="kjdsnk", colors = ["#CC6606", "#BECA10", "#36BD14","#D3B26B", "#3A3025", "#2514BD","#47093D", "#10C4CA", "#D9FF00"], 
                            show_percentages=True, chart_type="bar", stack_mode="percentage",)
                        
        with tabs[1]:
            pc=st.columns(3)
            with pc[0]:
                sample_data = {
                'name': 'Landry KENGNE',
                'title': 'Statistician',
                'about': '.',
                'email': 'landry.kengne99@gmail.com',
                'phone': '+237 6 98 28 05 37',
                'skills': ['Statistiques', 'Economics', 'Dashbord conceptor', 'Data analist']
            }
                create_simple_background_profile(
                name=sample_data['name'],
                title=sample_data['title'],
                about_text=sample_data['about'],
                image_path="conceptor.jpg",
                email=sample_data['email'],
                phone=sample_data['phone'],
                skills=sample_data['skills'],
                theme_color="#CC6606",
                height=700
            ) 
            
                
            
if __name__ == "__main__":
    main()     