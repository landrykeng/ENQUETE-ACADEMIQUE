import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from PIL import Image
from my_fonction import *
from Authentification import *

# Configuration de la page
st.set_page_config(
    page_title="Suivi d'Enquêtes - Yaoundé",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

#import_users_from_excel()

# Ajout de la police Google Fonts et augmentation de la taille de police globale
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"]  {
        font-family: 'Britannic Bold', Palatino Linotype, Times New Roman !important;
        font-size: 1.1rem !important;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Britannic Bold', Palatino Linotype, Times New Roman !important;
        letter-spacing: 0.01em;
    }
</style>
""", unsafe_allow_html=True)

# CSS personnalisé pour le style
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    }
    
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1rem;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .survey-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 6px 25px rgba(0,0,0,0.1);
        border-left: 6px solid;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .survey-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 35px rgba(0,0,0,0.15);
    }
    
    .survey-card-tontine {
        border-left-color: #FF6B35;
        background: linear-gradient(135deg, #fff 0%, #FFF8F5 100%);
    }
    
    .survey-card-dechets {
        border-left-color: #4ECDC4;
        background: linear-gradient(135deg, #fff 0%, #F0FFFE 100%);
    }
    
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #333;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(255, 154, 158, 0.3);
    }
    
    .success-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(168, 237, 234, 0.3);
    }
    
    .legal-frame {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #333;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border: 2px solid #fcb69f;
    }
    
    .status-indicator {
        display: inline-block;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        margin-right: 10px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
        100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
    }
    
    .status-active {
        background-color: #4CAF50;
    }
    
    .survey-details {
        background: rgba(0,0,0,0.05);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .confidence-badge {
        position: absolute;
        top: 15px;
        right: 15px;
        background: rgba(255,255,255,0.9);
        color: #333;
        padding: 6px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .checklist-item {
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(0,0,0,0.1);
    }
    
    .checklist-item:last-child {
        border-bottom: none;
    }
    
    .important-highlight {
        background: linear-gradient(135deg, #FFE066 0%, #FF6B6B 100%);
        color: #333;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 600;
        text-align: center;
    }
    
    .team-info {
        background: linear-gradient(135deg, #e3ffe7 0%, #d9e7ff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Ajout du logo officiel local (Logo1_ISSEA doit être dans le dossier du projet ou dans le répertoire approprié)

logo_path = "Logo1_ISSEA.png"  # Assurez-vous que ce fichier est dans le même dossier que ce script
logo = Image.open(logo_path)
st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 1.5rem;">
    """,
    unsafe_allow_html=True,
)
st.image(logo, width=4020)
st.markdown("</div>", unsafe_allow_html=True)
# Header principal
st.markdown("""
<div class="main-header">
    <div class="logo-container">
        🇨🇲 SUIVI DE L'ENQUÊTE ACADÉMIQUE - YAOUNDÉ
    </div>
    <h2 style="margin: 0; font-weight: 400;">
        Enquêtes Socio-économiques dans la Ville de Yaoundé
    </h2>
    <p style="font-size: 1.1rem; margin-top: 1rem; opacity: 0.9;">
        Plateforme de suivi et de contrôle qualité des données
    </p>
</div>
""", unsafe_allow_html=True)

# Cadre légal et confidentialité
st.markdown("""
<div class="legal-frame">
    <h3>⚖️ Cadre Légal et Confidentialité</h3>
    <p><strong>Loi de référence :</strong> N°2020/10 du 20 juillet 2020 régissant l'activité statistique au Cameroun</p>
    <p><strong>Article 13 :</strong> « Les données individuelles recueillies dans le cadre des opérations de collecte de données statistiques ne peuvent faire l'objet de divulgation de quelque manière que ce soit, sauf autorisation explicite accordée par les personnes physiques ou morales concernées. »</p>
    <p><strong>Zone d'étude :</strong> Ville de Yaoundé (7 arrondissements)</p>
    <p><strong>Type d'enquête :</strong> Enquêtes ménages avec questionnaires structurés</p>
</div>
""", unsafe_allow_html=True)

# Données des enquêtes
enquete_tontine = {
    "nom": "Pratique des Tontines au Cameroun",
    "sous_titre": "Cas de la ville de Yaoundé",
    "description": "Enquête sur la connaissance, la participation et l'impact économique des tontines dans les ménages yaoundéens",
    "sections": [
        "Section 0: Information sur la collecte",
        "Section 1: Identification et localisation du ménage", 
        "Section 2: Connaissance et participation aux tontines",
        "Section 3: Analyse des pratiques et impacts économiques",
        "Section 4: Pratiques et impacts économiques des tontines",
        "Section 5: Perspectives et recommandations"
    ],
    "questions_cles": [
        "Connaissance des différents types de tontines",
        "Participation et durée d'adhésion",
        "Motivations et avantages perçus",
        "Modalités de fonctionnement",
        "Impacts économiques et sociaux",
        "Innovations numériques"
    ],
    "statut": "En cours de collecte",
    "date_debut": "08 Juillet 2025",
    "participants_cible": 500,
    "participants_actuels": 287,
    "couleur": "#FF6B35",
    "icon": "💰"
}

enquete_dechets = {
    "nom": "Gestion des Ordures à Yaoundé",
    "sous_titre": "Opinion de la population sur la gestion des déchets",
    "description": "Enquête sur la perception, les comportements et les attentes des habitants concernant la gestion des déchets",
    "sections": [
        "Section 0: Information sur la collecte/ménage",
        "Section 1: Perception de l'insalubrité due aux déchets",
        "Section 2: Évaluation des services de collecte (HYSACAM, CUY)",
        "Section 3: Impacts de la mauvaise gestion sur la vie des habitants",
        "Section 4: Comportements, participation et incivisme",
        "Section 5: Attentes, suggestions et voies d'amélioration"
    ],
    "questions_cles": [
        "Appréciation de la propreté du quartier",
        "Fréquence des services de collecte",
        "Impacts sanitaires des déchets",
        "Comportements de tri et d'élimination",
        "Participation citoyenne",
        "Suggestions d'amélioration"
    ],
    "statut": "En cours de collecte",
    "date_debut": "08 Juillet 2025",
    "participants_cible": 400,
    "participants_actuels": 198,
    "couleur": "#4ECDC4",
    "icon": "🗑️"
}

# Affichage des enquêtes
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="survey-card survey-card-tontine">
        <div class="confidence-badge">🔒 Confidentiel</div>
        <h2 style="color: {enquete_tontine['couleur']}; margin-bottom: 0.5rem; display: flex; align-items: center;">
            {enquete_tontine['icon']} {enquete_tontine['nom']}
        </h2>
        <h4 style="color: #666; margin-bottom: 1rem; font-weight: 400;">
            {enquete_tontine['sous_titre']}
        </h4>
        <p style="color: #555; margin-bottom: 1.5rem; line-height: 1.6;">
            {enquete_tontine['description']}
        </p>
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span class="status-indicator status-active"></span>
            <strong>Statut:</strong> {enquete_tontine['statut']}
        </div>
        <div style="margin-bottom: 1rem;">
            <strong>📅 Début:</strong> {enquete_tontine['date_debut']}<br>
            <strong>🎯 Objectif:</strong> {enquete_tontine['participants_cible']} ménages<br>
            <strong>✅ Réalisés:</strong> {enquete_tontine['participants_actuels']} questionnaires
        </div>
        <div class="survey-details">
            <strong>📋 Structure du questionnaire:</strong><br>
            {'<br>'.join(['• ' + section for section in enquete_tontine['sections']])}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="survey-card survey-card-dechets">
        <div class="confidence-badge">🔒 Confidentiel</div>
        <h2 style="color: {enquete_dechets['couleur']}; margin-bottom: 0.5rem; display: flex; align-items: center;">
            {enquete_dechets['icon']} {enquete_dechets['nom']}
        </h2>
        <h4 style="color: #666; margin-bottom: 1rem; font-weight: 400;">
            {enquete_dechets['sous_titre']}
        </h4>
        <p style="color: #555; margin-bottom: 1.5rem; line-height: 1.6;">
            {enquete_dechets['description']}
        </p>
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span class="status-indicator status-active"></span>
            <strong>Statut:</strong> {enquete_dechets['statut']}
        </div>
        <div style="margin-bottom: 1rem;">
            <strong>📅 Début:</strong> {enquete_dechets['date_debut']}<br>
            <strong>🎯 Objectif:</strong> {enquete_dechets['participants_cible']} ménages<br>
            <strong>✅ Réalisés:</strong> {enquete_dechets['participants_actuels']} questionnaires
        </div>
        <div class="survey-details">
            <strong>📋 Structure du questionnaire:</strong><br>
            {'<br>'.join(['• ' + section for section in enquete_dechets['sections']])}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Section d'informations importantes
st.markdown("## 📢 Informations Importantes")

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.markdown("""
    <div class="important-highlight">
        ⚠️ RAPPEL : Respecter strictement la confidentialité des données collectées
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h4>🎯 Objectifs des Enquêtes</h4>
        <p><strong>Enquête Tontines :</strong></p>
        <ul>
            <li>Comprendre la pratique des systèmes d'épargne rotatifs</li>
            <li>Évaluer l'impact économique sur les ménages</li>
            <li>Identifier les innovations numériques</li>
            <li>Proposer des améliorations réglementaires</li>
        </ul>
        <p><strong>Enquête Déchets :</strong></p>
        <ul>
            <li>Évaluer la perception de la gestion des ordures</li>
            <li>Analyser l'efficacité des services publics</li>
            <li>Identifier les impacts sanitaires</li>
            <li>Recueillir les suggestions d'amélioration</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_info2:
    st.markdown("""
    <div class="team-info">
        <h4>👥 Organisation de l'Équipe</h4>
        <p><strong>Hiérarchie de supervision :</strong></p>
        <ul>
            <li><strong>Superviseur :</strong> Coordination générale</li>
            <li><strong>Superviseur Assistant :</strong> Support terrain</li>
            <li><strong>Contrôleur :</strong> Vérification qualité</li>
            <li><strong>Enquêteur :</strong> Collecte de données</li>
        </ul>
        <p><strong>Zones de couverture :</strong></p>
        <ul>
            <li>Yaoundé 1, 2, 3, 4, 5, 6, 7</li>
            <li>Enquête par quartier avec numérotation ZD</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Guide pratique pour les enquêteurs
st.markdown("## 📚 Guide Pratique - Enquêteurs")

col_guide1, col_guide2 = st.columns(2)

with col_guide1:
    st.markdown("""
    <div class="success-card">
        <h4>✅ Bonnes Pratiques - Avant l'Interview</h4>
        <div class="checklist-item">🆔 Vérifier votre matériel d'identification</div>
        <div class="checklist-item">📋 Préparer le questionnaire et les codes</div>
        <div class="checklist-item">🕒 Respecter les horaires convenus</div>
        <div class="checklist-item">📍 Localiser précisément l'adresse (ZD/Quartier)</div>
        <div class="checklist-item">🤝 Présentation courtoise et professionnelle</div>
        <div class="checklist-item">🔒 Rappeler la confidentialité des données</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-card">
        <h4>⚠️ Points de Vigilance</h4>
        <div class="checklist-item"><strong>Enquête Tontines :</strong> Bien expliquer ce qu'est une tontine si nécessaire</div>
        <div class="checklist-item"><strong>Questions sensibles :</strong> Revenus, problèmes familiaux</div>
        <div class="checklist-item"><strong>Filtres :</strong> Respecter les conditions de passage entre questions</div>
        <div class="checklist-item"><strong>Codes multiples :</strong> Vérifier les questions à choix multiples</div>
        <div class="checklist-item"><strong>Non-réponse :</strong> Noter les motifs précis</div>
    </div>
    """, unsafe_allow_html=True)

with col_guide2:
    st.markdown("""
    <div class="success-card">
        <h4>✅ Bonnes Pratiques - Pendant l'Interview</h4>
        <div class="checklist-item">🗣️ Poser les questions dans l'ordre du questionnaire</div>
        <div class="checklist-item">✏️ Écrire lisiblement dans les cases prévues</div>
        <div class="checklist-item">🔄 Reformuler si la personne ne comprend pas</div>
        <div class="checklist-item">⏱️ Prendre le temps nécessaire sans presser</div>
        <div class="checklist-item">🚫 Ne pas influencer les réponses</div>
        <div class="checklist-item">✔️ Vérifier la cohérence des réponses</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h4>📞 Contacts Utiles</h4>
        <p><strong>Support Technique :</strong> [À compléter]</p>
        <p><strong>Superviseur :</strong> [À compléter]</p>
        <p><strong>Urgences Terrain :</strong> [À compléter]</p>
        <p><strong>Horaires Support :</strong> 8h-18h du lundi au samedi</p>
    </div>
    """, unsafe_allow_html=True)

# Conseils spécifiques par enquête
st.markdown("## 🎯 Conseils Spécifiques par Enquête")

col_spec1, col_spec2 = st.columns(2)

with col_spec1:
    st.markdown(f"""
    <div class="survey-card survey-card-tontine">
        <h4 style="color: {enquete_tontine['couleur']};">💰 Spécificités Enquête Tontines</h4>
        <p><strong>Définition à retenir :</strong> Une tontine est un système d'épargne et de crédit rotatif où les membres cotisent régulièrement et reçoivent à tour de rôle la somme totale collectée.</p>
        
        <p><strong>Types de tontines à identifier :</strong></p>
        <ul>
            <li>Tontines d'épargne (classiques)</li>
            <li>Tontines de crédit (prêt collectif)</li>
            <li>Tontines festives (célébrations)</li>
            <li>Tontines d'aide mutuelle</li>
            <li>Tontines agricoles/rurales</li>
            <li>Tontines d'achat collectif</li>
        </ul>
        
        <p><strong>Questions délicates :</strong></p>
        <ul>
            <li>Montants des cotisations (tranches proposées)</li>
            <li>Problèmes vécus (détournements, conflits)</li>
            <li>Revenus du ménage</li>
        </ul>
        
        <p><strong>Innovation numérique :</strong> Mobile Money, WhatsApp, plateformes web</p>
    </div>
    """, unsafe_allow_html=True)

with col_spec2:
    st.markdown(f"""
    <div class="survey-card survey-card-dechets">
        <h4 style="color: {enquete_dechets['couleur']};">🗑️ Spécificités Enquête Déchets</h4>
        <p><strong>Acteurs à connaître :</strong></p>
        <ul>
            <li><strong>HYSACAM :</strong> Société de collecte des ordures</li>
            <li><strong>CUY :</strong> Communauté Urbaine de Yaoundé</li>
            <li><strong>MINEPDED :</strong> Ministère de l'Environnement</li>
            <li><strong>MINHDU :</strong> Ministère de l'Habitat et du Développement Urbain</li>
        </ul>
        
        <p><strong>Types de déchets à identifier :</strong></p>
        <ul>
            <li>Plastiques (bouteilles, emballages)</li>
            <li>Déchets organiques (restes alimentaires)</li>
            <li>Papiers et cartons</li>
            <li>Verre et métaux</li>
            <li>Déchets dangereux (piles, médicaments)</li>
        </ul>
        
        <p><strong>Zones sensibles :</strong> Marchés, carrefours, caniveaux, abords habitations</p>
        
        <p><strong>Maladies à noter :</strong> Diarrhées, paludisme, allergies, démangeaisons</p>
    </div>
    """, unsafe_allow_html=True)

# Guide pour les contrôleurs
st.markdown("## 🔍 Guide Pratique - Contrôleurs")

st.markdown("""
<div class="info-card">
    <h4>📋 Points de Contrôle Qualité</h4>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
        <div>
            <p><strong>✅ Vérifications Formelles :</strong></p>
            <ul>
                <li>Identification complète du ménage</li>
                <li>Numérotation séquentielle correcte</li>
                <li>Codes de réponse dans les bonnes cases</li>
                <li>Écriture lisible et encre durable</li>
                <li>Signature de l'enquêteur</li>
                <li>Date et heure de l'interview</li>
            </ul>
        </div>
        <div>
            <p><strong>✅ Vérifications de Cohérence :</strong></p>
            <ul>
                <li>Âge et niveau d'éducation cohérents</li>
                <li>Emploi et tranche de revenus compatibles</li>
                <li>Filtres de questions respectés</li>
                <li>Nombre de membres du ménage exact</li>
                <li>Localisation géographique précise</li>
                <li>Réponses multiples bien marquées</li>
            </ul>
        </div>
    </div>
    
    
    🎯 Objectif : Taux de qualité > 95% pour validation des questionnaires
    
</div>
""", unsafe_allow_html=True)

# Sidebar améliorée
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    st.markdown("- 🏠 **Accueil** (Actuel)")
    st.markdown("- 💰 Enquête Tontines")
    st.markdown("- 🗑️ Enquête Déchets")
    st.markdown("- 📊 Tableau de Bord")
    st.markdown("- 📈 Analytics Avancés")
    st.markdown("- 📋 Rapports & Exports")
    st.markdown("- ⚙️ Configuration")
    
    st.markdown("---")
    st.markdown("### 📍 Zone d'Étude")
    st.info("**Yaoundé - 7 Arrondissements**\n\n"
            "• Yaoundé 1 - Centre-ville\n"
            "• Yaoundé 2 - Tsinga, Emana\n" 
            "• Yaoundé 3 - Efoulan\n"
            "• Yaoundé 4 - Kondengui\n"
            "• Yaoundé 5 - Essos\n"
            "• Yaoundé 6 - Biyem-Assi\n"
            "• Yaoundé 7 - Nkolbisson")
    
    st.markdown("---")
    st.markdown("### 📞 Support")
    st.warning("**Assistance Technique**\n\n"
               "En cas de problème :\n"
               "• Contacter le superviseur\n"
               "• Documenter les incidents\n"
               "• Signaler les refus\n"
               "• Noter les adresses introuvables")
    
    st.markdown("---")
    st.markdown("### ⏰ Statut Actuel")
    current_time = datetime.now().strftime("%H:%M")
    current_date = datetime.now().strftime("%d/%m/%Y")
    st.success(f"**{current_date}**\n{current_time}\n\n✅ Système Opérationnel")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🇨🇲 <strong>République du Cameroun</strong> - Enquêtes Socio-économiques Yaoundé</p>
    <p>Plateforme de suivi développée dans le respect de la Loi N°2020/10 du 20 juillet 2020</p>
    <p><em>Données confidentielles - Usage strictement professionnel</em></p>
</div>
""", unsafe_allow_html=True)