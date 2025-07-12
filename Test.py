import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import traceback
import matplotlib.pyplot as plt
import plotly.express as px 
from streamlit_plotly_events import plotly_events
import seaborn as sns
import os
import warnings
import datetime
import plotly.graph_objects as go
import plotly.figure_factory as ff
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

# Configuration de l'application web
st.set_page_config(
    page_title="ISSEA Survey Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.issea.cm',
        'Report a bug': "mailto:landry.kengne99@gmail.com",
        'About': "Dashboard de suivi des enquêtes académiques - ISSEA 2025"
    }
)

# ============================================================================
# STYLES CSS POUR APPLICATION WEB MODERNE
# ============================================================================

webapp_styles = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700;800&family=Inter:wght@200;300;400;500;600;700&display=swap');

:root {
    /* Couleurs principales */
    --primary-50: #f0f9ff;
    --primary-100: #e0f2fe;
    --primary-200: #bae6fd;
    --primary-300: #7dd3fc;
    --primary-400: #38bdf8;
    --primary-500: #0ea5e9;
    --primary-600: #0284c7;
    --primary-700: #0369a1;
    --primary-800: #075985;
    --primary-900: #0c4a6e;
    
    /* Couleurs secondaires */
    --secondary-50: #fdf4ff;
    --secondary-100: #fae8ff;
    --secondary-200: #f3d2ff;
    --secondary-300: #e9a3ff;
    --secondary-400: #dc66ff;
    --secondary-500: #c533ff;
    --secondary-600: #a821c9;
    --secondary-700: #8b1a9e;
    --secondary-800: #731582;
    --secondary-900: #5e1065;
    
    /* Couleurs d'état */
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
    --info: #3b82f6;
    
    /* Couleurs neutres */
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-200: #e5e7eb;
    --gray-300: #d1d5db;
    --gray-400: #9ca3af;
    --gray-500: #6b7280;
    --gray-600: #4b5563;
    --gray-700: #374151;
    --gray-800: #1f2937;
    --gray-900: #111827;
    
    /* Effets */
    --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    
    --border-radius-sm: 0.375rem;
    --border-radius: 0.5rem;
    --border-radius-md: 0.75rem;
    --border-radius-lg: 1rem;
    --border-radius-xl: 1.5rem;
    --border-radius-2xl: 2rem;
}

/* Reset et base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

/* Cache les éléments Streamlit par défaut */
.stDeployButton {display:none;}
footer {visibility: hidden;}
.stApp > header {visibility: hidden;}

/* Main container */
.main {
    background: transparent;
    padding: 0;
}

/* Navigation Bar */
.navbar {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    padding: 1rem 2rem;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: var(--shadow-lg);
}

.navbar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1400px;
    margin: 0 auto;
}

.navbar-brand {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--gray-800);
    text-decoration: none;
}

.navbar-brand img {
    width: 40px;
    height: 40px;
    border-radius: var(--border-radius);
}

.navbar-nav {
    display: flex;
    align-items: center;
    gap: 2rem;
}

.nav-item {
    color: var(--gray-600);
    text-decoration: none;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: var(--border-radius);
    transition: all 0.3s ease;
}

.nav-item:hover {
    color: var(--primary-600);
    background: var(--primary-50);
}

.nav-item.active {
    color: var(--primary-600);
    background: var(--primary-100);
}

/* Sidebar moderne */
.sidebar {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.2);
    height: calc(100vh - 80px);
    position: sticky;
    top: 80px;
    overflow-y: auto;
}

section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: var(--shadow-lg);
}

section[data-testid="stSidebar"] > div {
    background: transparent;
    padding: 2rem 1rem;
}

/* Content area */
.content-wrapper {
    background: rgba(255, 255, 255, 0.02);
    min-height: calc(100vh - 80px);
    padding: 2rem;
}

.page-header {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: var(--border-radius-xl);
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-xl);
    border: 1px solid rgba(255, 255, 255, 0.2);
    position: relative;
    overflow: hidden;
}

.page-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary-500), var(--secondary-500));
}

.page-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--gray-800);
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, var(--primary-600), var(--secondary-600));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.page-subtitle {
    color: var(--gray-600);
    font-size: 1.1rem;
    font-weight: 400;
}

/* Breadcrumbs */
.breadcrumbs {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: var(--gray-500);
}

.breadcrumb-item {
    color: var(--gray-500);
    text-decoration: none;
}

.breadcrumb-item:hover {
    color: var(--primary-600);
}

.breadcrumb-separator {
    color: var(--gray-400);
}

/* Cards modernes */
.webapp-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: var(--border-radius-xl);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: var(--shadow-lg);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
    position: relative;
}

.webapp-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--primary-500), var(--secondary-500));
    opacity: 0.7;
}

.webapp-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-2xl);
    background: rgba(255, 255, 255, 0.98);
}

.card-header {
    padding: 1.5rem 1.5rem 0 1.5rem;
    border-bottom: 1px solid var(--gray-100);
    margin-bottom: 1rem;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--gray-800);
    margin-bottom: 0.5rem;
}

.card-subtitle {
    font-size: 0.9rem;
    color: var(--gray-500);
}

.card-body {
    padding: 0 1.5rem 1.5rem 1.5rem;
}

/* Métriques modernes */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.metric-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: var(--border-radius-lg);
    padding: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: var(--shadow-md);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--primary-500), var(--secondary-500));
}

.metric-card:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: var(--shadow-xl);
    background: rgba(255, 255, 255, 0.98);
}

.metric-icon {
    width: 48px;
    height: 48px;
    border-radius: var(--border-radius);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--primary-100), var(--secondary-100));
    color: var(--primary-600);
}

.metric-value {
    font-family: 'Poppins', sans-serif;
    font-size: 2.25rem;
    font-weight: 700;
    color: var(--gray-800);
    margin-bottom: 0.5rem;
}

.metric-label {
    font-size: 0.9rem;
    color: var(--gray-600);
    font-weight: 500;
    margin-bottom: 0.75rem;
}

.metric-change {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.75rem;
    border-radius: var(--border-radius);
    font-size: 0.8rem;
    font-weight: 600;
}

.metric-change.positive {
    background: var(--success);
    color: white;
}

.metric-change.negative {
    background: var(--error);
    color: white;
}

.metric-change.neutral {
    background: var(--gray-100);
    color: var(--gray-600);
}

/* Boutons webapp */
.webapp-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: var(--border-radius);
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    position: relative;
    overflow: hidden;
}

.webapp-button.primary {
    background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
    color: white;
    box-shadow: var(--shadow-md);
}

.webapp-button.primary:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
    background: linear-gradient(135deg, var(--primary-600), var(--primary-700));
}

.webapp-button.secondary {
    background: var(--gray-100);
    color: var(--gray-700);
    border: 1px solid var(--gray-200);
}

.webapp-button.secondary:hover {
    background: var(--gray-200);
    transform: translateY(-1px);
}

/* Streamlit component overrides */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
    border: none;
    border-radius: var(--border-radius);
    color: white;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-md);
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
    background: linear-gradient(135deg, var(--primary-600), var(--primary-700));
}

.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid var(--gray-200);
    border-radius: var(--border-radius);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.stSelectbox > div > div:focus-within,
.stMultiSelect > div > div:focus-within {
    border-color: var(--primary-500);
    box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
    background: white;
}

.stDateInput > div > div > input {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid var(--gray-200);
    border-radius: var(--border-radius);
    padding: 0.75rem;
    transition: all 0.3s ease;
}

.stDateInput > div > div > input:focus {
    border-color: var(--primary-500);
    box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
}

/* Tabs webapp */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: var(--border-radius-lg);
    padding: 0.5rem;
    gap: 0.25rem;
    box-shadow: var(--shadow-md);
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin-bottom: 2rem;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: var(--border-radius);
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
    border: none;
    color: var(--gray-600);
    font-size: 0.9rem;
}

.stTabs [data-baseweb="tab"]:hover {
    background: var(--primary-50);
    color: var(--primary-600);
    transform: translateY(-1px);
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
    color: white;
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}

/* Graphiques */
.stPlotlyChart {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: var(--border-radius-lg);
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: var(--shadow-md);
    transition: all 0.3s ease;
    margin-bottom: 1rem;
}

.stPlotlyChart:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: var(--border-radius);
    border: 1px solid var(--gray-200);
    box-shadow: var(--shadow-sm);
    transition: all 0.3s ease;
    padding: 1rem;
    margin-bottom: 1rem;
}

.streamlit-expanderHeader:hover {
    background: white;
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

/* Section separators */
.section-separator {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gray-200), transparent);
    margin: 3rem 0;
}

/* Status indicators */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.75rem;
    border-radius: var(--border-radius);
    font-size: 0.8rem;
    font-weight: 600;
}

.status-badge.success {
    background: var(--success);
    color: white;
}

.status-badge.warning {
    background: var(--warning);
    color: white;
}

.status-badge.error {
    background: var(--error);
    color: white;
}

.status-badge.info {
    background: var(--info);
    color: white;
}

/* Footer webapp */
.webapp-footer {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    padding: 2rem;
    margin-top: 3rem;
    text-align: center;
    color: var(--gray-600);
    box-shadow: var(--shadow-lg);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--gray-100);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, var(--primary-400), var(--primary-500));
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
}

/* Responsive design */
@media (max-width: 768px) {
    .navbar-content {
        flex-direction: column;
        gap: 1rem;
    }
    
    .navbar-nav {
        gap: 1rem;
    }
    
    .content-wrapper {
        padding: 1rem;
    }
    
    .page-title {
        font-size: 2rem;
    }
    
    .metric-grid {
        grid-template-columns: 1fr;
    }
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp 0.6s ease-out;
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.8;
    }
}

.pulse {
    animation: pulse 2s infinite;
}

/* Loading states */
.loading-skeleton {
    background: linear-gradient(90deg, var(--gray-200) 25%, var(--gray-100) 50%, var(--gray-200) 75%);
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
}

@keyframes loading {
    0% {
        background-position: 200% 0;
    }
    100% {
        background-position: -200% 0;
    }
}
</style>
"""

st.markdown(webapp_styles, unsafe_allow_html=True)

# ============================================================================
# COMPOSANTS D'INTERFACE WEBAPP
# ============================================================================

def create_navbar():
    """Crée la barre de navigation"""
    st.markdown("""
    <div class="navbar">
        <div class="navbar-content">
            <div class="navbar-brand">
                🏛️ <span>ISSEA Survey Dashboard</span>
            </div>
            <div class="navbar-nav">
                <a href="#" class="nav-item active">📊 Dashboard</a>
                <a href="#" class="nav-item">📈 Analytics</a>
                <a href="#" class="nav-item">⚙️ Settings</a>
                <a href="#" class="nav-item">👤 Profile</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_breadcrumbs(items):
    """Crée le fil d'Ariane"""
    breadcrumb_html = '<div class="breadcrumbs">'
    for i, item in enumerate(items):
        if i > 0:
            breadcrumb_html += '<span class="breadcrumb-separator">›</span>'
        breadcrumb_html += f'<a href="#" class="breadcrumb-item">{item}</a>'
    breadcrumb_html += '</div>'
    return breadcrumb_html

def create_webapp_metric(icon, title, value, change=None, change_type="positive"):
    """Crée une métrique webapp moderne"""
    change_class = f"metric-change {change_type}" if change else ""
    change_symbol = "↗" if change_type == "positive" else "↘" if change_type == "negative" else "→"
    change_html = f'<div class="{change_class}">{change_symbol} {change}%</div>' if change else ""
    
    return f"""
    <div class="metric-card fade-in-up">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value:,}</div>
        <div class="metric-label">{title}</div>
        {change_html}
    </div>
    """

def create_section_header(title, subtitle="", icon=""):
    """Crée un header de section webapp"""
    return f"""
    <div class="webapp-card" style="margin-bottom: 1.5rem;">
        <div class="card-header">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div>
                    <h3 class="card-title">{title}</h3>
                    {f'<p class="card-subtitle">{subtitle}</p>' if subtitle else ''}
                </div>
            </div>
        </div>
    </div>
    """

def create_update_notification(last_update):
    """Crée une notification de mise à jour"""
    return f"""
    <div class="webapp-card pulse" style="margin-bottom: 2rem;">
        <div class="card-body">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 1.5rem;">🔄</div>
                    <div>
                        <div style="font-weight: 600; color: var(--gray-800);">Statut du système</div>
                        <div style="color: var(--gray-600); font-size: 0.9rem;">Dernière mise à jour: {last_update}</div>
                    </div>
                </div>
                <div class="status-badge success">● En ligne</div>
            </div>
        </div>
    </div>
    """

# Fonction de langue simplifiée
def traduire_texte(text, lang):
    translations = {
        "Tableau de Bord Pour le suivi de la collecte sur l'enquête du ACADEMIQUE": {
            "English": "Academic Survey Data Collection Dashboard",
            "Français": "Tableau de Bord Pour le suivi de la collecte sur l'enquête du ACADEMIQUE"
        },
        "Sélectionner la date de collecte": {
            "English": "Select collection date",
            "Français": "Sélectionner la date de collecte"
        },
        "ANALYSE GENERALE": {
            "English": "GENERAL ANALYSIS", 
            "Français": "ANALYSE GENERALE"
        },
        "A propos": {
            "English": "About",
            "Français": "A propos"
        },
        "Sélectionner les arrondissement": {
            "English": "Select districts",
            "Français": "Sélectionner les arrondissement"
        },
        "Cartographie de la progression": {
            "English": "Progress mapping",
            "Français": "Cartographie de la progression"
        },
        "progression réelle par arrondissemnt": {
            "English": "Real progress by district", 
            "Français": "progression réelle par arrondissemnt"
        },
        "Progression par arrondissement": {
            "English": "Progress by district",
            "Français": "Progression par arrondissement"
        },
        "Sélectionner un (des) arrondissement (s)": {
            "English": "Select district(s)",
            "Français": "Sélectionner un (des) arrondissement (s)"
        },
        "Charge de travail accomplie par arrondissement": {
            "English": "Workload completed by district",
            "Français": "Charge de travail accomplie par arrondissement"
        },
        "Sélectionner un arrondissement": {
            "English": "Select a district",
            "Français": "Sélectionner un arrondissement"
        },
        "Progression de la collecte": {
            "English": "Collection progress",
            "Français": "Progression de la collecte"
        },
        "Taux de localisation des ménages": {
            "English": "Household localization rate",
            "Français": "Taux de localisation des ménages"
        },
        "Distribution du temps de remplissage en minute par arrondissement": {
            "English": "Distribution of completion time in minutes by district",
            "Français": "Distribution du temps de remplissage en minute par arrondissement"
        }
    }
    
    if text in translations and lang in translations[text]:
        return translations[text][lang]
    return text

def create_sidebar_controls():
    """Crée les contrôles de la sidebar"""
    st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h3 style="color: var(--gray-800); margin-bottom: 0.5rem;">🎛️ Contrôles</h3>
        <p style="color: var(--gray-600); font-size: 0.9rem;">Paramètres de l'analyse</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sélecteur de langue
    lang = st.sidebar.selectbox(
        "🌍 Langue / Language", 
        ["", "Français", "English"],
        help="Choisissez votre langue préférée"
    )
    
    return lang

def main():
    """Fonction principale webapp"""
    
    # Navigation bar
    create_navbar()
    
    # Sidebar controls
    lang = create_sidebar_controls()
    lang1 = "Français" if lang == "" else lang
    
    # Content wrapper
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    
    # Breadcrumbs
    st.markdown(create_breadcrumbs(["Accueil", "Dashboard", "Enquête Académique"]), unsafe_allow_html=True)
    
    # Page header
    st.markdown("""
    <div class="page-header fade-in-up">
        <h1 class="page-title">📊 Dashboard de Collecte d'Enquête</h1>
        <p class="page-subtitle">
            Suivi en temps réel de la collecte académique - Institut National de la Statistique (ISSEA)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données
    try:
        data = pd.read_excel("data_collected.xlsx")
        data = data.drop_duplicates(["id_menage","Duree_interview"])
        data["Date"] = data["Date"].dt.date
        data['arrondissement'] = data['arrondissement'].str.replace('Yaounde', 'Yaoundé', regex=False)
        fichier = Path("data_collected.xlsx")
        #date_up_date = datetime.datetime.now()
        
        data['distance_m'] = data.apply(lambda row: haversine(
            row['Longitude_GPS_Couverture'],
            row['Latitude_GPS_Couverture'],
            row['Longitude_collected'],
            row['Latitude_collected']
        ), axis=1)
        
        data['good_hh'] = (data['distance_m'] > 100).astype(int)
        
        data_rep = pd.read_excel("Repartition.xlsx", sheet_name="Repatition")
        data_rep['arrondissement'] = data_rep['arrondissement'].str.replace('Yaounde', 'Yaoundé', regex=False)
        data["Rejets_superviseur"] = data["Rejets_superviseur"].map({1:"Rejeté par les controleur", 0: "Approuvé par le Controleur"})
        data["Rejets_siege"] = data["Rejets_siege"].map({1:"Rejeté par le QG", 0: "Approuvé par le QG"})
        
        form = gpd.read_file("Arrondissement.shp")
        form = form.rename(columns={"arrondisse":"arrondissement"})
        geo_data = form.merge(data, on="arrondissement", how="left")
        geo_data = gpd.GeoDataFrame(geo_data, geometry='geometry')
        
        geo_data_rep = form.merge(data_rep, on="arrondissement", how="left")
        geo_data_rep = gpd.GeoDataFrame(geo_data_rep, geometry='geometry')
        
    except FileNotFoundError:
        st.error("⚠️ Fichiers de données non trouvés.")
        return
    
    # Notification de mise à jour
    #st.markdown(create_update_notification(date_up_date.strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
    
    # Section de mise à jour manuelle
    col_update = st.columns([1, 2, 1])
    with col_update[1]:
        if st.button("🔄 Actualiser les données", help="Recharger les données depuis la source"):
            with st.spinner("🔄 Actualisation en cours..."):
                time.sleep(2)
            st.success("✅ Données actualisées avec succès!")
    
    # Contrôles de date dans la sidebar
    st.sidebar.markdown("---")
    la_date = st.sidebar.date_input(
        "📅 " + traduire_texte("Sélectionner la date de collecte", lang),
        dt.datetime(2025, 5, 20).date(),
        min_value=dt.datetime(2023, 1, 1).date(),
        max_value=dt.datetime(2025, 12, 31).date(),
        help="Filtrer les données par date de collecte"
    )
    
    # Tabs principales
    tab1, tab2 = st.tabs([
        f"📈 {traduire_texte('ANALYSE GENERALE', lang)}", 
        f"💫 {traduire_texte('A propos', lang)}"
    ])
    
    with tab1:
        # Description des indicateurs
        with st.expander("ℹ️ Guide des indicateurs", expanded=False):
            st.markdown("""
            <div class="webapp-card">
                <div class="card-body">
                    <h4 style="color: var(--gray-800); margin-bottom: 1rem;">📋 Statuts des questionnaires</h4>
                    <div style="display: grid; gap: 0.75rem;">
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <span class="status-badge warning">🟡</span>
                            <span><strong>Questionnaires soumis:</strong> Achevés par les enquêteurs, en attente d'approbation des contrôleurs</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <span class="status-badge info">🟠</span>
                            <span><strong>Validés contrôleur:</strong> Approuvés par les contrôleurs, en attente du QG</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <span class="status-badge success">🟢</span>
                            <span><strong>Approuvés QG:</strong> Questionnaires définitifs et validés</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Section 1: Métriques principales
        st.markdown(create_section_header(
            "Vue d'ensemble des questionnaires", 
            "Statistiques en temps réel de la collecte",
            "📊"
        ), unsafe_allow_html=True)
        
        # Calculs des métriques
        nb_tontine = (data['Questionnaire'] == 'Tontine').sum()
        nb_dechet = (data['Questionnaire'] == 'Dechet').sum()
        rep_tontine = (data_rep['questionnaire'] == 'Tontine').sum()
        rep_dechet = (data_rep['questionnaire'] == 'Dechet').sum()
        
        # Grid de métriques
        metric_cols = st.columns(3)
        
        with metric_cols[0]:
            st.markdown(create_webapp_metric(
                "💰", "Questionnaires Tontine", nb_tontine,
                round(100*nb_tontine/rep_tontine,2) if rep_tontine > 0 else 0,
                "positive"
            ), unsafe_allow_html=True)
        
        with metric_cols[1]:
            st.markdown(create_webapp_metric(
                "🗑️", "Questionnaires Déchets", nb_dechet,
                round(100*nb_dechet/rep_dechet,2) if rep_dechet > 0 else 0,
                "positive"
            ), unsafe_allow_html=True)
        
        with metric_cols[2]:
            st.markdown(create_webapp_metric(
                "📋", "Total Questionnaires", nb_dechet+nb_tontine,
                round(100*(nb_dechet+nb_tontine)/(rep_tontine+rep_dechet),2) if (rep_tontine+rep_dechet) > 0 else 0,
                "positive"
            ), unsafe_allow_html=True)
        
        # Section graphiques principaux
        chart_row = st.columns([3, 2])
        
        with chart_row[0]:
            st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h4 class="card-title">🎯 Filtres d\'analyse</h4></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-body">', unsafe_allow_html=True)
            
            Type_questionnaire = st.multiselect(
                "Types de questionnaires", 
                options=data["Questionnaire"].unique(),
                default=data["Questionnaire"].unique(),
                help="Sélectionnez les types à analyser"
            )
            
            if len(Type_questionnaire) == 0:
                df_to_plot = data
                df_rep_to_plot = data_rep
            else:
                df_to_plot = data[data["Questionnaire"].isin(Type_questionnaire)]
                df_rep_to_plot = data_rep[data_rep["questionnaire"].isin(Type_questionnaire)]
            
            # Calculs progression
            a_test = pd.DataFrame(df_to_plot["arrondissement"].value_counts())
            b_test = pd.DataFrame(df_rep_to_plot["arrondissement"].value_counts())
            
            data_arr = a_test.join(b_test, how="outer", lsuffix="_collecte", rsuffix="_distribution")
            data_arr.reset_index(inplace=True)
            data_arr.rename(columns={"index": "id_enqueteur"}, inplace=True)
            data_arr["count_collecte"] = data_arr["count_collecte"].fillna(0)
            data_arr["progression"] = data_arr["count_collecte"] / (data_arr["count_distribution"])
            
            progress_all = df_to_plot.shape[0]/df_rep_to_plot.shape[0] if df_rep_to_plot.shape[0] > 0 else 0
            
            # Graphiques de progression
            progress_cols = st.columns(2)
            with progress_cols[0]:
                make_progress_char(progress_all, couleur="", titre=traduire_texte("Progression de la collecte", lang))
            
            with progress_cols[1]:
                time_std = round(data["Duree_interview"].std())
                time_mean = round(data["Duree_interview"].mean())
                create_questionnaire_time_gauge(time_mean, time_std, temps_cible=None, titre="Durée des interviews")
            
            # Graphique principal
            df_progress = data_arr[['arrondissement', 'count_collecte', 'count_distribution']]
            df_progress = df_progress.set_index('arrondissement')
            df_progress = df_progress.rename(columns={
                'count_collecte': 'Questionnaires soumis', 
                'count_distribution': 'Ménages distribués'
            })
            
            create_bar_chart_from_contingency(
                df_progress,
                title="📊 Répartition par arrondissement",
                colors=['#0ea5e9', '#6366f1', '#f59e0b'],
                orientation="vertical",
                var1_name="Arrondissement",
                var2_name="Nombre",
                height="400px"
            )
            
            st.markdown('</div></div>', unsafe_allow_html=True)
        
        with chart_row[1]:
            # Progression par arrondissement
            st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h4 class="card-title">📈 Progression</h4></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-body">', unsafe_allow_html=True)
            
            make_multi_progress_bar_echart(
                data_arr['arrondissement'],
                data_arr['progression'],
                colors=['#0ea5e9', '#6366f1', '#f59e0b', '#10b981', '#f97316'],
                titre="Par arrondissement",
                height=300
            )
            
            st.markdown('</div></div>', unsafe_allow_html=True)
            
            # Statut global
            st.markdown('<div class="webapp-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h4 class="card-title">🎯 Statut global</h4></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-body">', unsafe_allow_html=True)
            
            create_pie_chart_from_df(
                data, "Resultat_collecte", 
                style="donut", 
                title="", 
                colors=None,
                cle="status_global"
            )
            
            st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Section qualité
        quality_row = st.columns(2)
        
        with quality_row[0]:
            st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h4 class="card-title">⭐ Appréciation qualité</h4></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-body">', unsafe_allow_html=True)
            
            create_pie_chart_from_df(
                data, "Appreciation_qualite_interview", 
                style="donut", 
                title="", 
                colors=None
            )
            
            st.markdown('</div></div>', unsafe_allow_html=True)
        
        with quality_row[1]:
            st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h4 class="card-title">❓ Questions manquantes</h4></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-body">', unsafe_allow_html=True)
            
            data_qest = data.groupby("id_enqueteur").agg({"Nb_questions_sans_reponse":"size"})
            mean_qst_sans_rep = round(data_qest["Nb_questions_sans_reponse"].mean()) if len(data_qest) > 0 else 0
            std_qst_sans_rep = round(data_qest["Nb_questions_sans_reponse"].std()) if len(data_qest) > 0 else 0
            
            create_missing_questions_gauge(
                mean_qst_sans_rep, std_qst_sans_rep, 
                total_questions=None, 
                objectif_max=None, 
                titre="Moyenne par enquêteur", 
                cle="questions_manquantes"
            )
            
            st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Section 2: Validation
        st.markdown(create_section_header(
            "Suivi des validations", 
            "Questionnaires validés par les contrôleurs et le QG",
            "✅"
        ), unsafe_allow_html=True)
        
        data_qg = data[data["Statut"] != "Soumis"]
        
        # Métriques validation
        validation_cols = st.columns(3)
        
        nb_tontine_qg = data_qg[data_qg['Questionnaire'] == 'Tontine'].shape[0]
        nb_dechet_qg = data_qg[data_qg['Questionnaire'] == 'Dechet'].shape[0]
        rep_tontine_qg = data_rep[data_rep['questionnaire'] == 'Tontine'].shape[0]
        rep_dechet_qg = data_rep[data_rep['questionnaire'] == 'Dechet'].shape[0]
        
        with validation_cols[0]:
            st.markdown(create_webapp_metric(
                "✅", "Tontine Validées", nb_tontine_qg,
                round(100*nb_tontine_qg/rep_tontine_qg,2) if rep_tontine_qg > 0 else 0,
                "positive"
            ), unsafe_allow_html=True)
        
        with validation_cols[1]:
            st.markdown(create_webapp_metric(
                "✅", "Déchets Validés", nb_dechet_qg,
                round(100*nb_dechet_qg/rep_dechet_qg,2) if rep_dechet_qg > 0 else 0,
                "positive"
            ), unsafe_allow_html=True)
        
        with validation_cols[2]:
            st.markdown(create_webapp_metric(
                "📋", "Total Validé", nb_dechet_qg+nb_tontine_qg,
                round(100*(nb_dechet_qg+nb_tontine_qg)/(rep_tontine_qg+rep_dechet_qg),2) if (rep_tontine_qg+rep_dechet_qg) > 0 else 0,
                "positive"
            ), unsafe_allow_html=True)
        
        # Graphiques validation
        validation_charts = st.columns(2)
        
        with validation_charts[0]:
            st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h4 class="card-title">📊 Statuts par type</h4></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-body">', unsafe_allow_html=True)
            
            Type_questionnaire2 = st.multiselect(
                "Filtrer par thème", 
                options=data["Questionnaire"].unique(),
                default=data["Questionnaire"].unique(),
                key="Type2"
            )
            
            df_filtered = data[data["Questionnaire"].isin(Type_questionnaire2)]
            
            create_crossed_bar_chart(
                df_filtered, "Statut", "Questionnaire", 
                title="", 
                colors=["#10b981","#f59e0b","#3b82f6"],
                width="100%", height="400px",
                orientation="vertical"
            )
            
            st.markdown('</div></div>', unsafe_allow_html=True)
        
        with validation_charts[1]:
            st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h4 class="card-title">🗺️ Validations par zone</h4></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-body">', unsafe_allow_html=True)
            
            create_crossed_bar_chart(
                df_filtered, "arrondissement", "Statut", 
                title="", 
                colors=["#10b981","#f59e0b","#3b82f6"],
                width="100%", height="400px",
                orientation="vertical"
            )
            
            st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Section cartographie
        st.markdown(create_section_header(
            "Analyse géospatiale", 
            "Répartition géographique et progression par zone",
            "🗺️"
        ), unsafe_allow_html=True)
        
        arr = st.multiselect(
            "🏙️ Sélectionner les arrondissements", 
            options=data["arrondissement"].unique(), 
            default=data["arrondissement"].unique(),
            help="Choisir les zones à analyser"
        )
        
        # Calculs pour cartographie
        df_qg = data_qg[data_qg["Questionnaire"].isin(Type_questionnaire2)]
        df_qg_rep = data_rep[data_rep["questionnaire"].isin(Type_questionnaire2)]
        
        a_test = pd.DataFrame(df_qg["arrondissement"].value_counts())
        b_test = pd.DataFrame(df_qg_rep["arrondissement"].value_counts())
        
        data_arr_qg = a_test.join(b_test, how="outer", lsuffix="_collecte", rsuffix="_distribution")
        data_arr_qg.reset_index(inplace=True)
        data_arr_qg.rename(columns={"index": "arrondissement"}, inplace=True)
        data_arr_qg["count_collecte"] = data_arr_qg["count_collecte"].fillna(0)
        data_arr_qg["progression"] = data_arr_qg["count_collecte"] / (data_arr_qg["count_distribution"])
        
        # Cartes et progression
        map_row = st.columns(2)
        
        with map_row[0]:
            st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h4 class="card-title">🗺️ Carte interactive</h4></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-body">', unsafe_allow_html=True)
            
            data_arr_qg["label"] = (data_arr_qg["arrondissement"]).astype(str) + ": " + (data_arr_qg["progression"] * 100).round(2).astype(str) + "%"
            geo_df_plot = data_arr_qg.merge(form, on="arrondissement", how="left")
            geo_data_to_plot = geo_df_plot[geo_df_plot["arrondissement"].isin(arr)]
            
            create_choropleth_map(
                geo_data_to_plot, geometry_col='geometry', value_col='progression', 
                label_col='label', zoom_start=10, colormap='Greens',
                num_classes=5, title="", 
                legend_name="Progression", popup_cols="progression", 
                tooltip_format=None, width=800, height=500
            )
            
            st.markdown('</div></div>', unsafe_allow_html=True)
        
        with map_row[1]:
            st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h4 class="card-title">📊 Détail progression</h4></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-body">', unsafe_allow_html=True)
            
            make_multi_progress_bar_echart(
                data_arr_qg['arrondissement'],
                data_arr_qg['progression'],
                colors=['#0ea5e9', '#6366f1', '#f59e0b', '#10b981', '#f97316'],
                titre="",
                height=500,
                cle="progression_detail"
            )
            
            st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Section évolution temporelle
        st.markdown(create_section_header(
            "Évolution temporelle", 
            "Tendances et analyse dans le temps",
            "📈"
        ), unsafe_allow_html=True)
        
        st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><h4 class="card-title">📅 Évolution quotidienne</h4></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-body">', unsafe_allow_html=True)
        
        data_evolution = data.copy()
        data_evolution["Date"] = data_evolution["Date"].astype(str)
        create_crossed_bar_chart(
            data_evolution, "Date", "Statut", 
            title="",
            width="100%", height="400px",
            orientation="vertical"
        )
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Heatmap
        st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><h4 class="card-title">🔥 Carte de chaleur</h4></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-body">', unsafe_allow_html=True)
        
        enq_for_heat_map = st.multiselect(
            "Zones pour l'analyse temporelle",
            data["arrondissement"].unique(),
            default=data["arrondissement"].unique(), 
            key="heatmap_zones"
        )
        
        data_superviz_heat_map = data[(data["arrondissement"].isin(enq_for_heat_map))]
        cross_enq = pd.crosstab(data_superviz_heat_map["arrondissement"], data_superviz_heat_map["Date"])
        
        if data_superviz_heat_map.shape[0] > 0:
            make_st_heatmap_echat2(cross_enq, title="")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Section analyse détaillée
        st.markdown(create_section_header(
            "Analyse détaillée par zone", 
            "Focus sur un arrondissement spécifique",
            "🔍"
        ), unsafe_allow_html=True)
        
        detail_row = st.columns([1, 2])
        
        with detail_row[0]:
            st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h4 class="card-title">⚙️ Paramètres</h4></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-body">', unsafe_allow_html=True)
            
            select_arr = st.selectbox(
                "Arrondissement à analyser",
                data["arrondissement"].unique(),
                help="Sélectionner pour analyse détaillée"
            )
            
            select_theme = st.multiselect(
                "Thèmes à inclure", 
                options=data["Questionnaire"].unique(), 
                default=data["Questionnaire"].unique(),
                key="themes_detail"
            )
            
            # Calculs pour l'arrondissement sélectionné
            data_select = data[
                (data["arrondissement"] == select_arr) & 
                (data["Questionnaire"].isin(select_theme))
            ]
            
            if len(data_select) > 0:
                avg_duration = round(data_select["Duree_interview"].mean())
                std_duration = round(data_select["Duree_interview"].std())
                total_surveys = len(data_select)
                
                st.markdown(f"""
                <div style="margin-top: 1rem;">
                    <div style="background: var(--primary-50); padding: 1rem; border-radius: var(--border-radius); margin-bottom: 0.5rem;">
                        <div style="font-weight: 600; color: var(--primary-700);">📊 {total_surveys}</div>
                        <div style="font-size: 0.9rem; color: var(--primary-600);">Questionnaires</div>
                    </div>
                    <div style="background: var(--success); color: white; padding: 1rem; border-radius: var(--border-radius); margin-bottom: 0.5rem;">
                        <div style="font-weight: 600;">⏱️ {avg_duration} min</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">Durée moyenne</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                create_questionnaire_time_gauge(
                    avg_duration, std_duration, 
                    temps_cible=None, 
                    titre="",
                    cle="detail_gauge"
                )
            
            st.markdown('</div></div>', unsafe_allow_html=True)
        
        with detail_row[1]:
            st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h4 class="card-title">📊 Distribution des durées</h4></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-body">', unsafe_allow_html=True)
            
            box_fig = px.box(
                data, x="arrondissement", y="Duree_interview", color="arrondissement",
                title="",
                height=350
            )
            box_fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(box_fig, use_container_width=True)
            
            st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Graphiques finaux
        final_charts = st.columns(2)
        
        with final_charts[0]:
            st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h4 class="card-title">📋 Résultats collecte</h4></div>', unsafe_load_html=True)
            st.markdown('<div class="card-body">', unsafe_allow_html=True)
            
            data_for_analysis = data[data["Questionnaire"].isin(select_theme)]
            make_cross_echart(
                data_for_analysis, "arrondissement", "Resultat_collecte", 
                title="", x_label_rotation=0, colors=None, 
                height="350px", cle="resultats_collecte", normalize=False, 
                show_percentages=True, chart_type="bar", stack_mode="total"
            )
            
            st.markdown('</div></div>', unsafe_allow_html=True)
        
        with final_charts[1]:
            st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h4 class="card-title">⭐ Appréciation qualité</h4></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-body">', unsafe_allow_html=True)
            
            make_cross_echart(
                data_for_analysis, "arrondissement", "Appreciation_qualite_interview", 
                title="", x_label_rotation=0, 
                height="350px", cle="appreciation_qualite", 
                colors=["#10b981", "#3b82f6", "#f59e0b", "#ef4444"], 
                show_percentages=True, chart_type="bar", stack_mode="percentage"
            )
            
            st.markdown('</div></div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown(create_section_header(
            "À propos de l'application", 
            "Informations sur le développeur et les technologies",
            "💫"
        ), unsafe_allow_html=True)
        
        about_row = st.columns([1, 2, 1])
        
        with about_row[1]:
            st.markdown('<div class="webapp-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-body" style="text-align: center; padding: 2rem;">', unsafe_allow_html=True)
            
            # Profil développeur
            sample_data = {
                'name': 'Landry KENGNE',
                'title': 'Statistician & Developer',
                'about': 'Spécialisé en analyse statistique et développement d\'applications web.',
                'email': 'landry.kengne99@gmail.com',
                'phone': '+237 6 98 28 05 37',
                'skills': ['Statistiques', 'Data Science', 'Dashboard Development', 'Web Applications']
            }
            
            try:
                create_simple_background_profile(
                    name=sample_data['name'],
                    title=sample_data['title'],
                    about_text=sample_data['about'],
                    image_path="conceptor.jpg",
                    email=sample_data['email'],
                    phone=sample_data['phone'],
                    skills=sample_data['skills'],
                    theme_color="#0ea5e9",
                    height=600
                )
            except:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, var(--primary-500), var(--secondary-500)); margin: 0 auto 2rem; display: flex; align-items: center; justify-content: center; font-size: 3rem; color: white;">
                        👨‍💻
                    </div>
                    <h3 style="color: var(--gray-800); margin-bottom: 0.5rem;">{sample_data['name']}</h3>
                    <p style="color: var(--primary-600); font-weight: 500; margin-bottom: 1rem;">{sample_data['title']}</p>
                    <p style="color: var(--gray-600); margin-bottom: 2rem;">{sample_data['about']}</p>
                    
                    <div style="display: grid; gap: 0.5rem; margin-bottom: 2rem;">
                        <div style="color: var(--gray-700);">📧 {sample_data['email']}</div>
                        <div style="color: var(--gray-700);">📱 {sample_data['phone']}</div>
                    </div>
                    
                    <div>
                        <h4 style="color: var(--gray-800); margin-bottom: 1rem;">🛠️ Compétences</h4>
                        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center;">
                            {''.join([f'<span style="background: var(--primary-100); color: var(--primary-700); padding: 0.25rem 0.75rem; border-radius: var(--border-radius); font-size: 0.8rem;">{skill}</span>' for skill in sample_data['skills']])}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Footer webapp
    st.markdown("""
    <div class="webapp-footer">
        <div style="max-width: 1200px; margin: 0 auto;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; text-align: left; margin-bottom: 2rem;">
                <div>
                    <h4 style="color: var(--gray-800); margin-bottom: 1rem;">🏛️ ISSEA</h4>
                    <p style="margin-bottom: 0.5rem;">Institut National de la Statistique</p>
                    <p style="margin-bottom: 0.5rem;">Yaoundé, Cameroun</p>
                </div>
                <div>
                    <h4 style="color: var(--gray-800); margin-bottom: 1rem;">📊 Dashboard</h4>
                    <p style="margin-bottom: 0.5rem;">Version 2.0</p>
                    <p style="margin-bottom: 0.5rem;">Suivi d'enquêtes académiques</p>
                </div>
                <div>
                    <h4 style="color: var(--gray-800); margin-bottom: 1rem;">💻 Technologies</h4>
                    <p style="margin-bottom: 0.5rem;">Streamlit • Plotly • Python</p>
                    <p style="margin-bottom: 0.5rem;">Pandas • GeoPandas</p>
                </div>
            </div>
            <div style="border-top: 1px solid var(--gray-200); padding-top: 2rem; text-align: center;">
                <p>© 2025 ISSEA • Développé avec ❤️ par <strong>Landry KENGNE</strong></p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Fin content-wrapper

if __name__ == "__main__":
    main()