import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import gdown
from streamlit_option_menu import option_menu
import folium
from geopy.geocoders import Nominatim


st.set_page_config(page_title = "Dashboard sur l'état des Lycées en France", page_icon=":bar_chart:",layout="wide")

st.set_option('deprecation.showPyplotGlobalUse', False)


# Code pour le menu de selection
with st.sidebar:
    choose = option_menu("Menu", ["Introduction", "Lycées par région", "Ratio Privé/Public", "Carte", "Résultats par fillière", "Data brutes"],
    	menu_icon="app-indicator", default_index=0,
    	styles={"container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "#6fd1d0", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#d1e2e2"},})


#########################################################################################

# Chargement des données à partir d'un lien - fichier CSV
#path = "https://www.data.gouv.fr/fr/datasets/r/7580d6d2-a7bb-4cbb-a78f-5dbaa1891cc4"
#df_bac = pd.read_csv(path, delimiter=";", low_memory=False)


# Chargement des données en local

def load_data():
    path = "D:/C/PSB/Cours/S2/Business_Intel/data_lycees.csv"
    df_bac = pd.read_csv(path, delimiter=";", low_memory=False)
    return df_bac

df_bac = load_data()


# Reshape sur jeu de données car trop de variables
colonnes_a_garder = [
    'etablissement',
    'annee',
    'ville',
    'commune',
    'academie',
    'departement',
    'secteur_public_pu_prive_pr',
    'effectif_presents_serie_l',
    'effectif_presents_serie_es',
    'effectif_presents_serie_s',
    'effectif_presents_serie_stg',
    'effectif_presents_serie_sti2d',
    'effectif_presents_serie_std2a',
    'effectif_presents_serie_stmg',
    'effectif_presents_serie_sti',
    'effectif_presents_serie_stl',
    'effectif_presents_serie_st2s',
    'effectif_presents_serie_musiq_danse',
    'effectif_presents_serie_hotellerie',
    'effectif_presents_total_series',
    'taux_brut_de_reussite_serie_l',
    'taux_brut_de_reussite_serie_es',
    'taux_brut_de_reussite_serie_s',
    'taux_brut_de_reussite_serie_stg',
    'taux_brut_de_reussite_serie_sti2d',
    'taux_brut_de_reussite_serie_std2a',
    'taux_brut_de_reussite_serie_stmg',
    'taux_brut_de_reussite_serie_sti',
    'taux_brut_de_reussite_serie_stl',
    'taux_brut_de_reussite_serie_st2s',
    'taux_brut_de_reussite_serie_musiq_danse',
    'taux_brut_de_reussite_serie_hotellerie',
    'taux_brut_de_reussite_total_series',
    'taux_mention_brut_serie_l',
    'taux_mention_brut_serie_es',
    'taux_mention_brut_serie_s',
    'taux_mention_brut_serie_sti2d',
    'taux_mention_brut_serie_std2a',
    'taux_mention_brut_serie_stmg',
    'taux_mention_brut_serie_stl',
    'taux_mention_brut_serie_st2s',
    'taux_mention_brut_serie_musiq_danse',
    'taux_mention_brut_serie_hotellerie',
    'taux_mention_brut_toutes_series',
    'effectif_de_seconde',
    'effectif_de_premiere',
    'effectif_de_terminale',
    'libelle_region_2016',
    'code_region_2016',
    'code_departement',
    'libelle_departement'
]

df_bac = df_bac[colonnes_a_garder]

#####################################################################################


# Code pour les filtres

st.sidebar.header("Please Filter Here :")
annees = sorted(df_bac["annee"].unique(), reverse=True)
filtre_annee = st.sidebar.multiselect("Select Year:", options=annees, default=annees[2])
filtre_region = st.sidebar.multiselect("Select Region :", options= sorted(df_bac["libelle_region_2016"].unique(), reverse=False), default=["CENTRE-VAL DE LOIRE"])
filtre_pubpriv = st.sidebar.multiselect("Select Privé or Public :", options= df_bac["secteur_public_pu_prive_pr"].unique(),default=df_bac["secteur_public_pu_prive_pr"].unique())

# Nouveau dataframe avec les filtres
df_selection = df_bac.query(
	"annee == @filtre_annee & libelle_region_2016 == @filtre_region & secteur_public_pu_prive_pr == @filtre_pubpriv")


########################################################################

# Première page Introduction

if choose == 'Introduction':

	st.markdown("<h2 style='font-size: 26px;'> Etat des lieux de l'éducation en France </h2>", unsafe_allow_html=True)
	st.write("Bienvenue à tous sur mon Dashboard. Ici vous trouverez des informations qui vous permettront de mieux comprendre l'état de l'éducation française et plus particulièrement au sein des lycées francais.")

	st.write("Vous pourrez ainsi observer quelle est la région qui compte le plus de lycées, monitorer le ratio entre lycées publics et privés. De la même manière vous pourrez observer les effectifs par filières au bac (S, ES, L, STMG, Hotelerie, ...) ainsi que les top filières et leurs taux de réussite et de mention au bac.")
	st.write("Toutes les pages du dashboard sont connectées à des filtres qui vont venir modifier les graphiques selon la selection choisie par l'utilisateur. Les filtres peuvent s'appliquer sur : la région, l'année et également filtrer les lycées en fonction du type (public ou privé).")
	st.write(":school:")
	st.markdown("---")


	st.markdown("<h3 style='font-size: 26px;'> Quelques mots sur l'auteur,  </h3>", unsafe_allow_html=True)
	st.write("Ysoline Avrain, actuellement en 4e années d'études au sein de PSB x Efrei dans le cursus Msc Data Management.\n")
	st.write("Ce projet est réalisé dans le cadre du cours de Business Intelligence dispensé par M. Mano Matthew")

	data_gouv_url = "https://www.data.gouv.fr/fr/datasets/indicateurs-de-valeur-ajoutee-des-lycees-denseignement-general-et-technologique/"
	st.markdown(f"Vous pouvez retrouver le jeu de données utilisé sur [DataGouv]({data_gouv_url}).")

	st.markdown("---")

	st.markdown("<h3 style='font-size: 26px;'> Retrouvez moi sur...  </h3>", unsafe_allow_html=True)

	linkedin_url = "www.linkedin.com/in/ysoline-avrain"
	st.markdown(f"[Linkedin]({linkedin_url})")




# Seconde page 


if choose == 'Lycées par région':
	
	value_counts = df_selection['libelle_region_2016'].value_counts()
	st.markdown("<h2 style='font-size: 26px;'> Répartition de l'effectif des lycées français par région</h2>", unsafe_allow_html=True)

	# Créer un graphe avec Seaborn
	fig = sns.barplot(x=value_counts.index, y=value_counts.values)

	# Définir les étiquettes des axes et le titre du graphique
	fig.set(xlabel='Régions', ylabel='Nombre de lycées', title='')
	fig.set_xticklabels(fig.get_xticklabels(), rotation=45, horizontalalignment='right')
	sns.despine()
	
	for i, v in enumerate(value_counts.values):
		fig.text(i, v, str(v), horizontalalignment='center', verticalalignment='bottom', fontweight='bold')

	fig.figure.set_size_inches(8, 4)  # Définir la taille en pouces (largeur, hauteur)

	# Afficher le graphique dans Streamlit
	st.pyplot(fig.figure)




# Troisième page 

if choose == 'Ratio Privé/Public':

	col1, col2 = st.columns([2, 1])

	# Diagramme circulaire

	effectif_par_secteur = df_selection['secteur_public_pu_prive_pr'].value_counts()
	with col1:
		st.markdown("<h2 style='font-size: 26px;'> Ratio entre lycée public et privé</h2>", unsafe_allow_html=True)
		labels = effectif_par_secteur.index
		sizes = effectif_par_secteur.values
		colors = ['lightblue', 'lightgreen']

		fig, ax = plt.subplots(figsize=(2,2))
		ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90,textprops={'fontsize': 5},wedgeprops={'width': 0.4})
		ax.axis('equal')

		# Affichage du diagramme circulaire
		st.pyplot(fig)

	###
	with col2:
		st.markdown("<h2 style='font-size: 22px;'>Effectifs sur le total</h2>", unsafe_allow_html=True)
		effectif_par_secteur_tot = df_bac['secteur_public_pu_prive_pr'].value_counts()
		st.write(effectif_par_secteur_tot)
		st.markdown("---")

	with col2:
		st.markdown("<h2 style='font-size: 22px;'>Effectifs sur la sélection</h2>", unsafe_allow_html=True)
		st.write(effectif_par_secteur)


# Quatrième page

elif choose == 'Carte':

	# Transcription des données géographiques	
	geolocator = Nominatim(user_agent="myapp")
	df_selection['Coordinates'] = df_selection['commune'].apply(lambda x: geolocator.geocode(x).point if geolocator.geocode(x) else None)

	# Filtrer les lignes avec des coordonnées géographiques valides
	df_filtered = df_selection.dropna(subset=['Coordinates'])

	# Créer une carte
	m = folium.Map(location=[0, 0], zoom_start=2)

	# Ajouter les marqueurs sur la carte
	for index, row in df_filtered.iterrows():
	    commune = row['commune']
	    latitude, longitude = row['Coordinates'].latitude, row['Coordinates'].longitude
	    folium.Marker([latitude, longitude], popup=commune).add_to(m)

	# Afficher la carte dans Streamlit
	st.title("Ma carte interactive")
	st.markdown("Carte avec des marqueurs basés sur les communes du DataFrame")
	st.write(m)
	# Ne fonctionne pas pour une raison inconnue


# Cinquième page

elif choose == 'Résultats par fillière':


	st.markdown("<h2 style='font-size: 26px;'> Répartition des effectifs par série</h2>", unsafe_allow_html=True)
	
	effectif_dict = {
	    'Nom série': ['L', 'ES', 'S', 'STG', 'STI2D', 'STD2A', 'STMG', 'STI', 'STL', 'ST2S', 'Musique/Danse', 'Hôtellerie'],
	    'Effectif': [
	        df_selection['effectif_presents_serie_l'].sum(),
	        df_selection['effectif_presents_serie_es'].sum(),
	        df_selection['effectif_presents_serie_s'].sum(),
	        df_selection['effectif_presents_serie_stg'].sum(),
	        df_selection['effectif_presents_serie_sti2d'].sum(),
	        df_selection['effectif_presents_serie_std2a'].sum(),
	        df_selection['effectif_presents_serie_stmg'].sum(),
	        df_selection['effectif_presents_serie_sti'].sum(),
	        df_selection['effectif_presents_serie_stl'].sum(),
	        df_selection['effectif_presents_serie_st2s'].sum(),
	        df_selection['effectif_presents_serie_musiq_danse'].sum(),
	        df_selection['effectif_presents_serie_hotellerie'].sum()
	    ]
	}

	# Créer un DataFrame à partir du dictionnaire
	df_effectif_total = pd.DataFrame(effectif_dict)
	df_effectif_total = df_effectif_total.sort_values('Effectif', ascending=False)
	# Créer le graphique avec Seaborn
	plt.figure(figsize=(10, 6))
	ax = sns.barplot(x='Nom série', y='Effectif', data=df_effectif_total)
	plt.xlabel('Série')
	plt.ylabel('Nombre d \'éleves ')
	plt.title('')

	for p in ax.patches:
		ax.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points', fontweight='bold')

	# Afficher le graphique dans Streamlit
	st.pyplot(plt)


###
	st.markdown("---")
###

	# TOP 5

	st.write(":sports_medal: Les tops ")
	col1, col2 = st.columns([1, 1])

##### Top 5 filières réussite au bac 
	with col1:
		reussite_dict = {
		    'Nom série': ['L', 'ES', 'S', 'STG', 'STI2D', 'STD2A', 'STMG', 'STI', 'STL', 'ST2S', 'Musique/Danse', 'Hôtellerie'],
		    'Taux_reussite': [
		        df_selection['taux_brut_de_reussite_serie_l'].mean(),
		        df_selection['taux_brut_de_reussite_serie_es'].mean(),
		        df_selection['taux_brut_de_reussite_serie_s'].mean(),
		        df_selection['taux_brut_de_reussite_serie_stg'].mean(),
		        df_selection['taux_brut_de_reussite_serie_sti2d'].mean(),
		        df_selection['taux_brut_de_reussite_serie_std2a'].mean(),
		        df_selection['taux_brut_de_reussite_serie_stmg'].mean(),
		        df_selection['taux_brut_de_reussite_serie_sti'].mean(),
		        df_selection['taux_brut_de_reussite_serie_stl'].mean(),
		        df_selection['taux_brut_de_reussite_serie_st2s'].mean(),
		        df_selection['taux_brut_de_reussite_serie_musiq_danse'].mean(),
		        df_selection['taux_brut_de_reussite_serie_hotellerie'].mean()
		    ]
		}

		# Créer un DataFrame à partir du dictionnaire
		df_reussite_total = pd.DataFrame(reussite_dict)
		df_reussite_total = df_reussite_total.sort_values('Taux_reussite', ascending=False).head(5)

		# Afficher le top 5 des taux de réussite dans Streamlit
		st.write(" <h2 style='font-size: 28px;'> Top 5 des filières ayant le plus haut taux de réussite au bac </h2>", unsafe_allow_html=True)

		for index, row in df_reussite_total.iterrows():
			st.write(f"**{row['Nom série']}** avec : **{row['Taux_reussite']:.2f}%** de réussite au bac")



##### Top 5 filières mention au bac 
	with col2:
		mention_dict = {
		    'Nom série': ['L', 'ES', 'S', 'STI2D', 'STD2A', 'STMG', 'STI', 'STL', 'ST2S', 'Musique/Danse', 'Hôtellerie'],
		    'Taux_mention': [
		        df_selection['taux_mention_brut_serie_l'].mean(),
		        df_selection['taux_mention_brut_serie_es'].mean(),
		        df_selection['taux_mention_brut_serie_s'].mean(),
		        df_selection['taux_mention_brut_serie_sti2d'].mean(),
		        df_selection['taux_mention_brut_serie_std2a'].mean(),
		        df_selection['taux_mention_brut_serie_stmg'].mean(),
		        df_selection['taux_brut_de_reussite_serie_sti'].mean(),
		        df_selection['taux_mention_brut_serie_stl'].mean(),
		        df_selection['taux_mention_brut_serie_st2s'].mean(),
		        df_selection['taux_mention_brut_serie_musiq_danse'].mean(),
		        df_selection['taux_mention_brut_serie_hotellerie'].mean()
		    ]
		}

		# Créer un DataFrame à partir du dictionnaire
		df_mention_total = pd.DataFrame(mention_dict)
		df_mention_total = df_mention_total.sort_values('Taux_mention', ascending=False).head(5)
		
		# Afficher le top 5 des taux de réussite dans Streamlit
		st.write(" <h2 style='font-size: 28px;'> Top 5 des filières ayant le plus haut taux de mention au bac </h2>", unsafe_allow_html=True)

		for index, row in df_mention_total.iterrows():
			st.write(f"**{row['Nom série']}** avec : **{row['Taux_mention']:.2f}%** de mention au bac")


###
	st.markdown("---")
###

########## Evolution dans le temps 

	st.write(":chart_with_upwards_trend: Les évolutions dans le temps ")

	series_list = [
	    'taux_brut_de_reussite_serie_l',
	    'taux_brut_de_reussite_serie_es',
	    'taux_brut_de_reussite_serie_s',
	    'taux_brut_de_reussite_serie_stg',
	    'taux_brut_de_reussite_serie_sti2d',
	    'taux_brut_de_reussite_serie_std2a',
	    'taux_brut_de_reussite_serie_stmg',
	    'taux_brut_de_reussite_serie_sti',
	    'taux_brut_de_reussite_serie_stl',
	    'taux_brut_de_reussite_serie_st2s',
	    'taux_brut_de_reussite_serie_musiq_danse',
	    'taux_brut_de_reussite_serie_hotellerie',
	    'taux_brut_de_reussite_total_series'
	]

	# Nouveau DataFrame
	df_taux_reussite = pd.DataFrame(columns=['Année', 'Nom de série', 'Taux_réussite'])

	# Calcul du taux de réussite moyen par filière pour chaque année
	for annee in filtre_annee:
	    for series in series_list:
	        taux_moyen = df_selection[df_selection['annee'] == annee][series].mean()
	        nom_serie = series.replace('taux_brut_de_reussite_', '').replace('_serie_', ' ')
	        df_taux_reussite = df_taux_reussite.append({'Année': annee, 'Nom de série': nom_serie, 'Taux_réussite': taux_moyen}, ignore_index=True)



	# Affichage du DataFrame
	st.write(df_taux_reussite)

	st.write(":chart_with_upwards_trend: Représentation graphique de l'évolution du taux de réussite moyen dans le temps ")
	st.line_chart(data=df_taux_reussite, x='Année', y='Taux_réussite', width=0, height=0, use_container_width=True)


# Page annexe pour afficher les datas brutes

elif choose == 'Data brutes':
# Ajoutez votre contenu pour l'onglet 3 ici
	st.write(df_bac)