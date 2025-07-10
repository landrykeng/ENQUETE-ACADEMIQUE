"""
Module pour créer des graphiques avec streamlit-echarts
Auteur: Assistant IA
Date: 2025
"""

import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts
import numpy as np
from typing import List, Optional, Union
import geopandas as gpd
import pandas as pd
import folium
from shapely.geometry import Point
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import branca.colormap as cm

from math import radians, cos, sin, asin, sqrt

# Fonction pour calculer la distance entre deux points GPS
def haversine(lon1, lat1, lon2, lat2):
    # Convertir les degrés en radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Formule de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Rayon de la Terre en mètres
    r = 6371000  
    return c * r


def graphique_barre_simple(df: pd.DataFrame, 
                          x_col: str, 
                          y_col: str, 
                          titre: str = "Graphique à barres",
                          horizontal: bool = False,
                          couleur: str = "#5470c6") -> None:
    """
    Crée un graphique à barres simple (vertical ou horizontal)
    
    Args:
        df: DataFrame contenant les données
        x_col: nom de la colonne pour l'axe X
        y_col: nom de la colonne pour l'axe Y
        titre: titre du graphique
        horizontal: True pour horizontal, False pour vertical
        couleur: couleur des barres
    """
    
    # Préparer les données
    x_data = df[x_col].tolist()
    y_data = df[y_col].tolist()
    
    if horizontal:
        option = {
            "title": {"text": titre, "left": "center"},
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "value"},
            "yAxis": {"type": "category", "data": x_data},
            "series": [{
                "type": "bar",
                "data": y_data,
                "itemStyle": {"color": couleur}
            }]
        }
    else:
        option = {
            "title": {"text": titre, "left": "center"},
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": x_data},
            "yAxis": {"type": "value"},
            "series": [{
                "type": "bar",
                "data": y_data,
                "itemStyle": {"color": couleur}
            }]
        }
    
    st_echarts(options=option, height="400px")


def graphique_barre_croise_effectifs(df: pd.DataFrame,
                                   x_col: str,
                                   group_col: str,
                                   y_col: str,
                                   titre: str = "Graphique à barres croisées",
                                   empile: bool = False) -> None:
    """
    Crée un graphique à barres croisées des effectifs
    
    Args:
        df: DataFrame contenant les données
        x_col: nom de la colonne pour l'axe X
        group_col: nom de la colonne pour le regroupement
        y_col: nom de la colonne des valeurs
        titre: titre du graphique
        empile: True pour empilé, False pour juxtaposé
    """
    
    # Pivoter les données
    pivot_df = df.pivot_table(values=y_col, index=x_col, columns=group_col, fill_value=0)
    
    x_data = pivot_df.index.tolist()
    series_data = []
    
    for col in pivot_df.columns:
        series_data.append({
            "name": str(col),
            "type": "bar",
            "data": pivot_df[col].tolist(),
            "stack": "total" if empile else None
        })
    
    option = {
        "title": {"text": titre, "left": "center"},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": [str(col) for col in pivot_df.columns]},
        "xAxis": {"type": "category", "data": x_data},
        "yAxis": {"type": "value"},
        "series": series_data
    }
    
    st_echarts(options=option, height="400px")


def graphique_barre_croise_frequences(df: pd.DataFrame,
                                    x_col: str,
                                    group_col: str,
                                    titre: str = "Graphique à barres croisées (fréquences)") -> None:
    """
    Crée un graphique à barres croisées des fréquences empilées
    
    Args:
        df: DataFrame contenant les données
        x_col: nom de la colonne pour l'axe X
        group_col: nom de la colonne pour le regroupement
        titre: titre du graphique
    """
    
    # Calculer les fréquences
    freq_df = pd.crosstab(df[x_col], df[group_col], normalize='index') * 100
    
    x_data = freq_df.index.tolist()
    series_data = []
    
    for col in freq_df.columns:
        series_data.append({
            "name": str(col),
            "type": "bar",
            "data": freq_df[col].round(2).tolist(),
            "stack": "total"
        })
    
    option = {
        "title": {"text": titre, "left": "center"},
        "tooltip": {
            "trigger": "axis",
            "formatter": "{b}<br/>{a}: {c}%"
        },
        "legend": {"data": [str(col) for col in freq_df.columns]},
        "xAxis": {"type": "category", "data": x_data},
        "yAxis": {"type": "value", "axisLabel": {"formatter": "{value}%"}},
        "series": series_data
    }
    
    st_echarts(options=option, height="400px")


def diagramme_secteur(df: pd.DataFrame,
                     label_col: str,
                     value_col: str,
                     titre: str = "Diagramme en secteur") -> None:
    """
    Crée un diagramme en secteur (camembert)
    
    Args:
        df: DataFrame contenant les données
        label_col: nom de la colonne des étiquettes
        value_col: nom de la colonne des valeurs
        titre: titre du graphique
    """
    
    data = [{"value": row[value_col], "name": row[label_col]} for _, row in df.iterrows()]
    
    option = {
        "title": {"text": titre, "left": "center"},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "left": "left"},
        "series": [{
            "type": "pie",
            "radius": "50%",
            "data": data,
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                }
            }
        }]
    }
    
    st_echarts(options=option, height="400px")


def diagramme_donut(df: pd.DataFrame,
                   label_col: str,
                   value_col: str,
                   titre: str = "Diagramme en donut") -> None:
    """
    Crée un diagramme en donut
    
    Args:
        df: DataFrame contenant les données
        label_col: nom de la colonne des étiquettes
        value_col: nom de la colonne des valeurs
        titre: titre du graphique
    """
    
    data = [{"value": row[value_col], "name": row[label_col]} for _, row in df.iterrows()]
    
    option = {
        "title": {"text": titre, "left": "center"},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "left": "left"},
        "series": [{
            "type": "pie",
            "radius": ["40%", "70%"],
            "data": data,
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                }
            }
        }]
    }
    
    st_echarts(options=option, height="400px")


def diagramme_progression(valeur_actuelle: float,
                         valeur_max: float,
                         titre: str = "Diagramme de progression") -> None:
    """
    Crée un diagramme de progression (jauge)
    
    Args:
        valeur_actuelle: valeur actuelle
        valeur_max: valeur maximale
        titre: titre du graphique
    """
    
    pourcentage = (valeur_actuelle / valeur_max) * 100
    
    option = {
        "title": {"text": titre, "left": "center"},
        "series": [{
            "type": "gauge",
            "data": [{"value": pourcentage, "name": "Progression"}],
            "progress": {"show": True},
            "detail": {"valueAnimation": True, "formatter": "{value}%"}
        }]
    }
    
    st_echarts(options=option, height="400px")


def barre_progression_multiple(df: pd.DataFrame,
                              label_col: str,
                              value_col: str,
                              max_col: str,
                              titre: str = "Barres de progression multiples") -> None:
    """
    Crée des barres de progression multiples
    
    Args:
        df: DataFrame contenant les données
        label_col: nom de la colonne des étiquettes
        value_col: nom de la colonne des valeurs actuelles
        max_col: nom de la colonne des valeurs maximales
        titre: titre du graphique
    """
    
    labels = df[label_col].tolist()
    values = df[value_col].tolist()
    max_values = df[max_col].tolist()
    
    # Calculer les pourcentages
    percentages = [(v/m)*100 for v, m in zip(values, max_values)]
    
    option = {
        "title": {"text": titre, "left": "center"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "value", "max": 100},
        "yAxis": {"type": "category", "data": labels},
        "series": [{
            "type": "bar",
            "data": percentages,
            "itemStyle": {"color": "#91cc75"}
        }]
    }
    
    st_echarts(options=option, height="400px")


def heatmap(df: pd.DataFrame,
           x_col: str,
           y_col: str,
           value_col: str,
           titre: str = "Heatmap") -> None:
    """
    Crée une heatmap
    
    Args:
        df: DataFrame contenant les données
        x_col: nom de la colonne pour l'axe X
        y_col: nom de la colonne pour l'axe Y
        value_col: nom de la colonne des valeurs
        titre: titre du graphique
    """
    
    # Pivoter les données
    pivot_df = df.pivot_table(values=value_col, index=y_col, columns=x_col, fill_value=0)
    
    x_data = pivot_df.columns.tolist()
    y_data = pivot_df.index.tolist()
    
    # Préparer les données pour ECharts
    data = []
    for i, y in enumerate(y_data):
        for j, x in enumerate(x_data):
            data.append([j, i, pivot_df.loc[y, x]])
    
    option = {
        "title": {"text": titre, "left": "center"},
        "tooltip": {"position": "top"},
        "grid": {"height": "50%", "top": "10%"},
        "xAxis": {"type": "category", "data": x_data, "splitArea": {"show": True}},
        "yAxis": {"type": "category", "data": y_data, "splitArea": {"show": True}},
        "visualMap": {
            "min": 0,
            "max": pivot_df.values.max(),
            "calculable": True,
            "orient": "horizontal",
            "left": "center",
            "bottom": "15%"
        },
        "series": [{
            "type": "heatmap",
            "data": data,
            "label": {"show": True}
        }]
    }
    
    st_echarts(options=option, height="500px")


def boxplot(df: pd.DataFrame,
           category_col: str,
           value_col: str,
           titre: str = "Boxplot") -> None:
    """
    Crée un boxplot
    
    Args:
        df: DataFrame contenant les données
        category_col: nom de la colonne des catégories
        value_col: nom de la colonne des valeurs
        titre: titre du graphique
    """
    
    categories = df[category_col].unique()
    boxplot_data = []
    
    for cat in categories:
        values = df[df[category_col] == cat][value_col].values
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        median = np.percentile(values, 50)
        min_val = np.min(values)
        max_val = np.max(values)
        
        boxplot_data.append([min_val, q1, median, q3, max_val])
    
    option = {
        "title": {"text": titre, "left": "center"},
        "tooltip": {"trigger": "item"},
        "xAxis": {"type": "category", "data": categories.tolist()},
        "yAxis": {"type": "value"},
        "series": [{
            "type": "boxplot",
            "data": boxplot_data
        }]
    }
    
    st_echarts(options=option, height="400px")


def graphique_ligne(df: pd.DataFrame,
                   x_col: str,
                   y_col: str,
                   titre: str = "Graphique linéaire",
                   group_col: Optional[str] = None) -> None:
    """
    Crée un graphique linéaire
    
    Args:
        df: DataFrame contenant les données
        x_col: nom de la colonne pour l'axe X
        y_col: nom de la colonne pour l'axe Y
        titre: titre du graphique
        group_col: nom de la colonne pour les groupes (optionnel)
    """
    
    if group_col is None:
        # Graphique simple
        x_data = df[x_col].tolist()
        y_data = df[y_col].tolist()
        
        option = {
            "title": {"text": titre, "left": "center"},
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": x_data},
            "yAxis": {"type": "value"},
            "series": [{
                "type": "line",
                "data": y_data,
                "smooth": True
            }]
        }
    else:
        # Graphique avec groupes
        groups = df[group_col].unique()
        x_data = df[x_col].unique()
        x_data = sorted(x_data)
        
        series_data = []
        for group in groups:
            group_df = df[df[group_col] == group]
            group_df = group_df.set_index(x_col).reindex(x_data, fill_value=0)
            
            series_data.append({
                "name": str(group),
                "type": "line",
                "data": group_df[y_col].tolist(),
                "smooth": True
            })
        
        option = {
            "title": {"text": titre, "left": "center"},
            "tooltip": {"trigger": "axis"},
            "legend": {"data": [str(g) for g in groups]},
            "xAxis": {"type": "category", "data": x_data.tolist()},
            "yAxis": {"type": "value"},
            "series": series_data
        }
    
    st_echarts(options=option, height="400px")



def create_bar_chart(df, variable, 
                    title="Diagramme à barres", 
                    color="#5470c6", 
                    width="100%", 
                    height="400px",
                    orientation="vertical",
                    show_values=True,
                    sort_data=False,
                    ascending=True):
    """
    Crée un diagramme à barres avec st_echarts
    
    Paramètres:
    -----------
    df : pd.DataFrame
        Le dataframe contenant les données
    variable : str
        Le nom de la colonne à représenter
    title : str, optional
        Le titre du graphique (défaut: "Diagramme à barres")
    color : str, optional
        La couleur des barres (défaut: "#5470c6")
    width : str, optional
        La largeur du graphique (défaut: "100%")
    height : str, optional
        La hauteur du graphique (défaut: "400px")
    orientation : str, optional
        "vertical" ou "horizontal" (défaut: "vertical")
    show_values : bool, optional
        Afficher les valeurs sur les barres (défaut: True)
    sort_data : bool, optional
        Trier les données par valeur (défaut: False)
    ascending : bool, optional
        Ordre croissant si sort_data=True (défaut: True)
    
    Returns:
    --------
    None (affiche le graphique directement)
    """
    
    # Vérifier que la variable existe dans le dataframe
    if variable not in df.columns:
        st.error(f"La variable '{variable}' n'existe pas dans le dataframe")
        return
    
    # Calculer les fréquences/valeurs
    if df[variable].dtype in ['object', 'category']:
        # Variable catégorielle : compter les occurrences
        data_counts = df[variable].value_counts()
        x_data = data_counts.index.tolist()
        y_data = data_counts.values.tolist()
        y_axis_name = "Fréquence"
    else:
        # Variable numérique : utiliser les valeurs directement
        # On suppose qu'il y a une colonne index ou qu'on veut afficher les valeurs
        if len(df) > 50:
            st.warning("Trop de valeurs pour un diagramme à barres. Affichage des 50 premières.")
            df_plot = df.head(50)
        else:
            df_plot = df
        
        x_data = df_plot.index.tolist()
        y_data = df_plot[variable].tolist()
        y_axis_name = variable
    
    # Trier les données si demandé
    if sort_data:
        sorted_data = sorted(zip(x_data, y_data), key=lambda x: x[1], reverse=not ascending)
        x_data, y_data = zip(*sorted_data)
        x_data, y_data = list(x_data), list(y_data)
    
    # Configuration du graphique
    if orientation == "horizontal":
        option = {
            "title": {
                "text": title,
                "left": "center",
                "textStyle": {"fontSize": 16}
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"}
            },
            "grid": {
                "left": "10%",
                "right": "4%",
                "bottom": "3%",
                "containLabel": True
            },
            "xAxis": {
                "type": "value",
                "name": y_axis_name,
                "nameLocation": "middle",
                "nameGap": 30
            },
            "yAxis": {
                "type": "category",
                "data": x_data,
                "name": variable,
                "nameLocation": "middle",
                "nameGap": 50
            },
            "series": [{
                "name": y_axis_name,
                "type": "bar",
                "data": y_data,
                "itemStyle": {"color": color},
                "label": {
                    "show": show_values,
                    "position": "right"
                }
            }]
        }
    else:  # vertical
        option = {
            "title": {
                "text": title,
                "left": "center",
                "textStyle": {"fontSize": 16}
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"}
            },
            "grid": {
                "left": "3%",
                "right": "4%",
                "bottom": "10%",
                "containLabel": True
            },
            "xAxis": {
                "type": "category",
                "data": x_data,
                "name": variable,
                "nameLocation": "middle",
                "nameGap": 30,
                "axisLabel": {"rotate": 45 if len(x_data) > 10 else 0}
            },
            "yAxis": {
                "type": "value",
                "name": y_axis_name,
                "nameLocation": "middle",
                "nameGap": 50
            },
            "series": [{
                "name": y_axis_name,
                "type": "bar",
                "data": y_data,
                "itemStyle": {"color": color},
                "label": {
                    "show": show_values,
                    "position": "top"
                }
            }]
        }
    
    # Afficher le graphique
    st_echarts(options=option, width=width, height=height)



def create_crossed_bar_chart(df, var1, var2, 
                           title="Diagramme à barres croisées", 
                           colors=None,
                           width="100%", 
                           height="400px",
                           orientation="vertical",
                           show_values=True,
                           stacked=False,
                           normalize=False):
    """
    Crée un diagramme à barres croisées à partir d'un dataframe
    
    Paramètres:
    -----------
    df : pd.DataFrame
        Le dataframe contenant les données
    var1 : str
        Première variable (axe principal)
    var2 : str
        Deuxième variable (groupement des barres)
    title : str, optional
        Le titre du graphique
    colors : list, optional
        Liste des couleurs pour chaque modalité de var2
    width : str, optional
        La largeur du graphique
    height : str, optional
        La hauteur du graphique
    orientation : str, optional
        "vertical" ou "horizontal"
    show_values : bool, optional
        Afficher les valeurs sur les barres
    stacked : bool, optional
        Barres empilées ou côte à côte
    normalize : bool, optional
        Normaliser en pourcentages
    """
    
    # Vérifier que les variables existent
    if var1 not in df.columns or var2 not in df.columns:
        st.error(f"Une ou plusieurs variables n'existent pas dans le dataframe")
        return
    
    # Créer le tableau de contingence
    contingency_table = pd.crosstab(df[var1], df[var2])
    
    # Normaliser si demandé
    if normalize:
        contingency_table = contingency_table.div(contingency_table.sum(axis=1), axis=0) * 100
    
    # Appeler la fonction avec le tableau de contingence
    create_bar_chart_from_contingency(
        contingency_table, 
        title=title, 
        colors=colors,
        width=width, 
        height=height,
        orientation=orientation,
        show_values=show_values,
        stacked=stacked,
        var1_name=var1,
        var2_name=var2,
        is_percentage=normalize
    )


def create_bar_chart_from_contingency(contingency_table, 
                                    title="Diagramme à barres croisées",
                                    colors=None,
                                    width="100%", 
                                    height="400px",
                                    orientation="vertical",
                                    show_values=True,
                                    stacked=False,
                                    var1_name="Variable 1",
                                    var2_name="Variable 2",
                                    is_percentage=False):
    """
    Crée un diagramme à barres croisées à partir d'un tableau de contingence
    
    Paramètres:
    -----------
    contingency_table : pd.DataFrame
        Tableau de contingence (crosstab)
    title : str, optional
        Le titre du graphique
    colors : list, optional
        Liste des couleurs pour chaque colonne
    width : str, optional
        La largeur du graphique
    height : str, optional
        La hauteur du graphique
    orientation : str, optional
        "vertical" ou "horizontal"
    show_values : bool, optional
        Afficher les valeurs sur les barres
    stacked : bool, optional
        Barres empilées ou côte à côte
    var1_name : str, optional
        Nom de la première variable (pour les labels)
    var2_name : str, optional
        Nom de la deuxième variable (pour la légende)
    is_percentage : bool, optional
        Indique si les valeurs sont en pourcentage
    """
    
    # Préparer les données
    categories = contingency_table.index.tolist()
    series_names = contingency_table.columns.tolist()
    
    # Couleurs par défaut
    if colors is None:
        default_colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']
        colors = default_colors[:len(series_names)]
    
    # Créer les séries de données
    series = []
    for i, col in enumerate(series_names):
        series_data = contingency_table[col].tolist()
        series.append({
            "name": str(col),
            "type": "bar",
            "data": series_data,
            "itemStyle": {"color": colors[i % len(colors)]},
            "label": {
                "show": show_values,
                "position": "inside" if stacked else ("top" if orientation == "vertical" else "right"),
                "formatter": "{c}%" if is_percentage else "{c}"
            }
        })
        
        # Pour les barres empilées, ajuster la position des labels
        if stacked:
            series[i]["stack"] = "total"
    
    # Configuration du graphique
    if orientation == "horizontal":
        option = {
            "title": {
                "text": title,
                "left": "center",
                "textStyle": {"fontSize": 16}
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "formatter": "{b}<br/>{a}: {c}" + ("%" if is_percentage else "")
            },
            "legend": {
                "data": series_names,
                "top": "bottom",
                "left": "center"
            },
            "grid": {
                "left": "15%",
                "right": "4%",
                "bottom": "15%",
                "containLabel": True
            },
            "xAxis": {
                "type": "value",
                "name": "Effectifs" + (" (%)" if is_percentage else ""),
                "nameLocation": "middle",
                "nameGap": 30
            },
            "yAxis": {
                "type": "category",
                "data": categories,
                "name": var1_name,
                "nameLocation": "middle",
                "nameGap": 60
            },
            "series": series
        }
    else:  # vertical
        option = {
            "title": {
                "text": title,
                "left": "center",
                "textStyle": {"fontSize": 16}
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "formatter": "{b}<br/>{a}: {c}" + ("%" if is_percentage else "")
            },
            "legend": {
                "data": series_names,
                "top": "bottom",
                "left": "center"
            },
            "grid": {
                "left": "3%",
                "right": "4%",
                "bottom": "20%",
                "containLabel": True
            },
            "xAxis": {
                "type": "category",
                "data": categories,
                #"name": var1_name,
                "nameLocation": "middle",
                "nameGap": 30,
                "axisLabel": {"rotate": 45 if len(categories) > 8 else 0}
            },
            "yAxis": {
                "type": "value",
                "name": "Effectifs" + (" (%)" if is_percentage else ""),
                "nameLocation": "middle",
                "nameGap": 50
            },
            "series": series
        }
    
    # Afficher le graphique
    st_echarts(options=option, width=width, height=height)



def create_categorical_map(gdf, lat_col, lon_col, category_col, 
                          center_lat=None, center_lon=None, zoom_start=10,
                          popup_cols=None, tooltip_cols=None, style="OpenStreetMap"):
    """
    Crée une carte interactive avec des marqueurs colorés selon une variable catégorielle
    
    Paramètres:
    -----------
    gdf : GeoDataFrame ou DataFrame
        Les données à afficher
    lat_col : str
        Nom de la colonne contenant les latitudes
    lon_col : str
        Nom de la colonne contenant les longitudes
    category_col : str
        Nom de la colonne catégorielle pour la coloration
    center_lat : float, optional
        Latitude du centre de la carte (par défaut: moyenne des points)
    center_lon : float, optional
        Longitude du centre de la carte (par défaut: moyenne des points)
    zoom_start : int, optional
        Niveau de zoom initial (défaut: 10)
    popup_cols : list, optional
        Colonnes à afficher dans le popup
    tooltip_cols : list, optional
        Colonnes à afficher dans le tooltip
    
    Returns:
    --------
    folium.Map : La carte créée
    """
    
    # Vérifier les colonnes requises
    required_cols = [lat_col, lon_col, category_col]
    missing_cols = [col for col in required_cols if col not in gdf.columns]
    if missing_cols:
        st.error(f"Colonnes manquantes dans le DataFrame: {missing_cols}")
        return None
    
    # Supprimer les lignes avec des valeurs manquantes
    gdf_clean = gdf.dropna(subset=[lat_col, lon_col, category_col])
    
    if len(gdf_clean) == 0:
        st.error("Aucune donnée valide trouvée après nettoyage")
        return None
    
    # Calculer le centre si non spécifié
    if center_lat is None:
        center_lat = gdf_clean[lat_col].mean()
    if center_lon is None:
        center_lon = gdf_clean[lon_col].mean()
    
    # Créer la carte
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles=style
    )
    
    # Définir les couleurs pour chaque catégorie
    categories = sorted(gdf_clean[category_col].unique())
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
              'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white',
              'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
    
    # Créer un dictionnaire couleur-catégorie
    color_map = {cat: colors[i % len(colors)] for i, cat in enumerate(categories)}
    
    # Ajouter les marqueurs
    for idx, row in gdf_clean.iterrows():
        # Préparer le popup
        if popup_cols:
            popup_text = "<br>".join([f"<b>{col}:</b> {row[col]}" for col in popup_cols if col in gdf_clean.columns]) + "<br>" + f"<b>ID Ménage:</b> {row['id_menage']}"
        else:
            popup_text = f"<b>{category_col}:</b> {row[category_col]}"+ "<br>" + f"<b>ID Ménage:</b> {row['id_menage']}"
        
        # Préparer le tooltip
        if tooltip_cols:
            tooltip_text = " | ".join([f"{col}: {row[col]}" for col in tooltip_cols if col in gdf_clean.columns]) + "<br>" + f"<b>ID Ménage:</b> {row['id_menage']}"
        else:
            tooltip_text = str(row[category_col])+ "<br>" + str(row['id_menage'])
        
        # Ajouter le marqueur
        folium.Marker(
            location=[row[lat_col], row[lon_col]],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=tooltip_text,
            icon=folium.Icon(
                color=color_map[row[category_col]],
                icon='info-sign'
            )
        ).add_to(m)
    
    # Ajouter une légende
    legend_html = f"""
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: auto; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <h4>Légende - {category_col}-{row["id_menage"]}</h4>
    """
    
    for category, color in color_map.items():
        legend_html += f'<p><i class="fa fa-circle" style="color:{color}"></i> {category}</p>'
    
    legend_html += "</div>"
    folium_static(m)
    
    return m


def calculate_boxplot_stats(data):
    """
    Calcule les statistiques nécessaires pour un boxplot
    
    Returns:
    --------
    dict : Contient min, Q1, médiane, Q3, max, outliers
    """
    if len(data) == 0:
        return None
    
    # Supprimer les valeurs manquantes
    clean_data = data.dropna()
    
    if len(clean_data) == 0:
        return None
    
    # Calculer les quartiles
    Q1 = clean_data.quantile(0.25)
    Q3 = clean_data.quantile(0.75)
    median = clean_data.median()
    
    # Calculer les limites des moustaches (whiskers)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Valeurs min et max dans les limites
    whisker_min = clean_data[clean_data >= lower_bound].min()
    whisker_max = clean_data[clean_data <= upper_bound].max()
    
    # Outliers
    outliers = clean_data[(clean_data < lower_bound) | (clean_data > upper_bound)].tolist()
    
    return {
        'min': whisker_min,
        'Q1': Q1,
        'median': median,
        'Q3': Q3,
        'max': whisker_max,
        'outliers': outliers
    }

def create_boxplot(df, quantitative_col, categorical_col=None, 
                   title="Boxplot", y_axis_label=None, 
                   colors=None, width=800, height=500,
                   show_outliers=True):
    """
    Crée un boxplot interactif avec streamlit_echarts
    
    Paramètres:
    -----------
    df : DataFrame
        Les données à visualiser
    quantitative_col : str
        Nom de la colonne quantitative à représenter
    categorical_col : str, optional
        Nom de la colonne catégorielle pour grouper les données
    title : str
        Titre du graphique
    y_axis_label : str, optional
        Label de l'axe Y (par défaut: nom de la colonne quantitative)
    colors : list, optional
        Liste des couleurs pour chaque catégorie
    width : int
        Largeur du graphique
    height : int
        Hauteur du graphique
    show_outliers : bool
        Afficher ou non les outliers
    
    Returns:
    --------
    dict : Configuration ECharts pour le boxplot
    """
    
    # Vérifications
    if quantitative_col not in df.columns:
        st.error(f"Colonne '{quantitative_col}' non trouvée dans le DataFrame")
        return None
    
    if categorical_col and categorical_col not in df.columns:
        st.error(f"Colonne '{categorical_col}' non trouvée dans le DataFrame")
        return None
    
    # Supprimer les lignes avec des valeurs manquantes
    cols_to_check = [quantitative_col]
    if categorical_col:
        cols_to_check.append(categorical_col)
    
    df_clean = df.dropna(subset=cols_to_check)
    
    if len(df_clean) == 0:
        st.error("Aucune donnée valide après nettoyage")
        return None
    
    # Couleurs par défaut
    if colors is None:
        colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', 
                  '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']
    
    # Label de l'axe Y
    if y_axis_label is None:
        y_axis_label = quantitative_col
    
    # Préparer les données
    if categorical_col:
        # Boxplot par catégorie
        categories = sorted(df_clean[categorical_col].unique())
        boxplot_data = []
        scatter_data = []
        
        for i, category in enumerate(categories):
            category_data = df_clean[df_clean[categorical_col] == category][quantitative_col]
            stats = calculate_boxplot_stats(category_data)
            
            if stats:
                # Données pour le boxplot [min, Q1, median, Q3, max]
                boxplot_data.append([stats['min'], stats['Q1'], stats['median'], 
                                   stats['Q3'], stats['max']])
                
                # Données pour les outliers
                if show_outliers:
                    for outlier in stats['outliers']:
                        scatter_data.append([i, outlier])
        
        # Configuration ECharts
        option = {
            "title": {
                "text": title,
                "left": "center",
                "textStyle": {"fontSize": 16, "fontWeight": "bold"}
            },
            "tooltip": {
                "trigger": "item",
                "axisPointer": {"type": "shadow"}
            },
            "grid": {
                "left": "10%",
                "right": "10%",
                "bottom": "15%",
                "top": "15%"
            },
            "xAxis": {
                "type": "category",
                "data": categories,
                "boundaryGap": True,
                "nameGap": 30,
                "splitArea": {"show": False},
                "splitLine": {"show": False}
            },
            "yAxis": {
                "type": "value",
                "name": y_axis_label,
                "splitArea": {"show": True}
            },
            "series": [
                {
                    "name": "Boxplot",
                    "type": "boxplot",
                    "data": boxplot_data,
                    "itemStyle": {
                        "color": colors[0],
                        "borderColor": "#000"
                    },
                    "tooltip": {
                        "formatter": """"""
                                }
                }
            ]
        }
            
        
        
        # Ajouter les outliers si demandé
        if show_outliers and scatter_data:
            option["series"].append({
                "name": "Outliers",
                "type": "scatter",
                "data": scatter_data,
                "itemStyle": {
                    "color": colors[1] if len(colors) > 1 else "#ee6666",
                    "opacity": 0.6
                },
                "symbolSize": 6
            })
    
    else:
        # Boxplot simple (une seule série)
        stats = calculate_boxplot_stats(df_clean[quantitative_col])
        
        if not stats:
            st.error("Impossible de calculer les statistiques")
            return None
        
        boxplot_data = [[stats['min'], stats['Q1'], stats['median'], 
                        stats['Q3'], stats['max']]]
        
        scatter_data = [[0, outlier] for outlier in stats['outliers']] if show_outliers else []
        
        option = {
            "title": {
                "text": title,
                "left": "center",
                "textStyle": {"fontSize": 16, "fontWeight": "bold"}
            },
            "tooltip": {
                "trigger": "item",
                "axisPointer": {"type": "shadow"}
            },
            "grid": {
                "left": "10%",
                "right": "10%",
                "bottom": "15%",
                "top": "15%"
            },
            "xAxis": {
                "type": "category",
                "data": [quantitative_col],
                "boundaryGap": True,
                "nameGap": 30,
                "splitArea": {"show": False},
                "splitLine": {"show": False}
            },
            "yAxis": {
                "type": "value",
                "name": y_axis_label,
                "splitArea": {"show": True}
            },
            "series": [
                {
                    "name": "Boxplot",
                    "type": "boxplot",
                    "data": boxplot_data,
                    "itemStyle": {
                        "color": colors[0],
                        "borderColor": "#000"
                    },
                    "tooltip": {
                        "formatter": """function(param) {
                            return [
                                'Variable: ' + param.name,
                                'Maximum: ' + param.data[5],
                                'Q3: ' + param.data[4],
                                'Médiane: ' + param.data[3],
                                'Q1: ' + param.data[2],
                                'Minimum: ' + param.data[1]
                            ].join('<br/>');
                        }"""
                    }
                }
            ]
        }
        
        # Ajouter les outliers si demandé
        if show_outliers and scatter_data:
            option["series"].append({
                "name": "Outliers",
                "type": "scatter",
                "data": scatter_data,
                "itemStyle": {
                    "color": colors[1] if len(colors) > 1 else "#ee6666",
                    "opacity": 0.6
                },
                "symbolSize": 6
            })
    
    st_echarts(options=option, width=width, height=height)



def create_choropleth_map(gdf, geometry_col='geometry', value_col='nombre_questionnaire', 
                         label_col='arrondissement', zoom_start=10, colormap='YlOrRd', 
                         num_classes=5, title="Carte choroplèthe", 
                         legend_name="Nombre de questionnaires", popup_cols=None, 
                         tooltip_format=None, width=800, height=600):
    """
    Crée une carte choroplèthe avec labels personnalisés
    """

    # Vérification des colonnes
    required_cols = [geometry_col, value_col, label_col]
    missing_cols = [col for col in required_cols if col not in gdf.columns]
    if missing_cols:
        st.error(f"Colonnes manquantes : {missing_cols}")
        return None

    # Nettoyage des données
    gdf_clean = gdf.dropna(subset=required_cols)

    if gdf_clean.empty:
        st.error("Aucune donnée valide après nettoyage.")
        return None

    # Conversion en GeoDataFrame
    try:
        gdf_clean = gpd.GeoDataFrame(gdf_clean, geometry=geometry_col)
    except Exception as e:
        st.error(f"Erreur lors de la conversion en GeoDataFrame : {e}")
        return None

    # Vérification et définition du CRS
    if gdf_clean.crs is None:
        st.warning("CRS non défini. Utilisation de EPSG:4326 par défaut.")
        gdf_clean.set_crs(epsg=4326, inplace=True)
    else:
        gdf_clean = gdf_clean.to_crs(epsg=4326)

    # Création de la carte de base
    m = folium.Map(zoom_start=zoom_start, tiles='OpenStreetMap')

    # Palette de couleurs
    color_palettes = {
        'YlOrRd': ['#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026', '#800026'],
        'Blues': ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b'],
        'Greens': ["#eb2315", "#e63e0b", "#dd9308", "#bfe005", "#4fd810", '#41ab5d', '#238b45', '#006d2c', '#00441b'],
        'Reds': ['#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#a50f15', '#67000d'],
        'Purples': ['#fcfbfd', '#efedf5', '#dadaeb', '#bcbddc', '#9e9ac8', '#807dba', '#6a51a3', '#54278f', '#3f007d'],
        'Oranges': ['#fff5eb', '#fee6ce', '#fdd0a2', '#fdae6b', '#fd8d3c', '#f16913', '#d94801', '#a63603', '#7f2704']
    }

    colors = color_palettes.get(colormap, color_palettes['Greens'])

    # Création de la colormap
    min_val = gdf_clean[value_col].min()
    max_val = gdf_clean[value_col].max()
    colormap_obj = cm.LinearColormap(colors=colors[:num_classes], vmin=min_val, vmax=max_val, caption=legend_name)

    # Fonction couleur
    def get_color(value):
        if pd.isna(value):
            return '#808080'  # gris pour valeurs manquantes
        return colormap_obj(value)

    all_bounds = []

    # Ajout des polygones
    for idx, row in gdf_clean.iterrows():
        geom = row[geometry_col]

        # Préparation du popup
        if popup_cols:
            popup_text = "<br>".join([f"<b>{col}:</b> {row[col]}" for col in popup_cols if col in gdf_clean.columns])
        else:
            popup_text = f"<b>{label_col}:</b> {row[label_col]}<br><b>{legend_name}:</b> {row[value_col]}"
        
        # Tooltip
        tooltip_text = tooltip_format.format(**row) if tooltip_format else f"{row[label_col]}"

        # Bounds
        if hasattr(geom, 'bounds'):
            bounds = geom.bounds
            all_bounds.append([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

        # Ajout GeoJson
        folium.GeoJson(
            geom,
            style_function=lambda x, color=get_color(row[value_col]): {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7,
                'dashArray': '3, 3'
            },
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=folium.Tooltip(tooltip_text)
        ).add_to(m)

        # Ajout du label au centroïde
        try:
            centroid = geom.centroid
            folium.Marker(
                location=[centroid.y, centroid.x],
                icon=folium.DivIcon(
                    html=f'<div style="font-size: 19px; color: black; font-weight: bold; text-align: left; text-shadow: 1px 1px 1px white;">{row[label_col]}</div>',
                    icon_size=(40, 20),
                    icon_anchor=(20, 10)
                )
            ).add_to(m)
        except Exception as e:
            st.warning(f"Impossible d’ajouter le label pour {row[label_col]} : {e}")

    # Ajustement de la vue
    if all_bounds:
        try:
            min_lat = min([b[0][0] for b in all_bounds])
            min_lon = min([b[0][1] for b in all_bounds])
            max_lat = max([b[1][0] for b in all_bounds])
            max_lon = max([b[1][1] for b in all_bounds])
            m.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])
        except Exception as e:
            st.warning(f"Erreur lors de l'ajustement de la vue : {e}")

    # Ajout de la légende et du titre
    colormap_obj.add_to(m)
    title_html = f'''
    <h3 align="center" style="font-size:20px; margin-top:0px;"><b>{title}</b></h3>
    '''
    m.get_root().html.add_child(folium.Element(title_html))

    folium_static(m, width=width, height=height)
    return m

    