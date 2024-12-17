import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import datetime
from urllib.parse import urlparse


# Fonction pour récupérer le contenu de la page et son code de statut
def fetch_page(url):
    try:
        # Effectuer une requête GET pour récupérer le contenu de la page
        response = requests.get(url, timeout=10)  # Timeout de 10 secondes
        # Vérifier si la requête a été réussie
        if response.status_code == 200:
            return response.text, response.status_code, response.headers
        else:
            return None, response.status_code, response.headers
    except requests.exceptions.RequestException as e:
        # En cas d'erreur, retourner None et l'erreur
        return None, None, str(e)


# Fonction pour analyser le contenu SEO d'une page
def seo_analysis(url):
    html, status_code, headers = fetch_page(url)
    
    if html is None:
        # Si la récupération de la page échoue, afficher un message d'erreur
        st.error(f"Erreur lors de la récupération de l'URL: {status_code or 'Inconnue'}")
        st.text(f"Message d'erreur: {headers}")  # Afficher l'erreur détaillée
        return

    # Afficher le statut HTTP
    st.write("Code de statut HTTP:", status_code)

    # Parsing du HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Extraction des balises meta
    meta_tags = soup.find_all('meta')
    for tag in meta_tags:
        if tag.get('name') == 'description':
            st.write(f"Meta description: {tag.get('content')}")
        elif tag.get('property') == 'og:title':
            st.write(f"OG Title: {tag.get('content')}")
        elif tag.get('property') == 'og:image':
            st.write(f"OG Image: {tag.get('content')}")

    # Analyse de la balise <title>
    title_tag = soup.find('title')
    if title_tag:
        st.write(f"Title: {title_tag.text}")

    # Analyse des liens sortants (outgoing links)
    outgoing_links = soup.find_all('a', href=True)
    for link in outgoing_links:
        href = link['href']
        if href.startswith('http'):
            # Vérifier si l'URL est valide (2xx)
            try:
                response = requests.head(href, timeout=5)
                if response.status_code == 200:
                    link.style = "color: green;"
                elif 300 <= response.status_code < 400:
                    link.style = "color: yellow;"
                elif 400 <= response.status_code < 500:
                    link.style = "color: red;"
                elif 500 <= response.status_code < 600:
                    link.style = "color: purple;"
                # Afficher les informations de lien
                st.write(f"Link to: {href} Status: {response.status_code}")
            except requests.exceptions.RequestException:
                st.write(f"Link to: {href} Error: Cannot fetch")
    
    # Analyse des images
    images = soup.find_all('img')
    for img in images:
        img_url = img.get('src')
        if img_url and img_url.startswith('http'):
            try:
                img_response = requests.head(img_url, timeout=5)
                if img_response.status_code == 200:
                    st.write(f"Image URL: {img_url} Status: OK")
                else:
                    st.write(f"Image URL: {img_url} Error: {img_response.status_code}")
            except requests.exceptions.RequestException:
                st.write(f"Image URL: {img_url} Error: Cannot fetch")

    # Vérification de robots.txt
    parsed_url = urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    try:
        robots_response = requests.get(robots_url)
        if robots_response.status_code == 200:
            st.write("robots.txt trouvé et accessible.")
            st.text(robots_response.text)
        else:
            st.write("robots.txt non trouvé.")
    except requests.exceptions.RequestException:
        st.write("Erreur lors de la récupération du robots.txt.")

    # Ajouter un lien vers les outils externes SEO
    st.write("Vérifier l'URL dans ces outils SEO :")
    st.markdown(f"[Schema Markup Validator](https://search.google.com/structured-data/testing-tool/u/0/) | [Rich Result Testing Tool](https://search.google.com/test/rich-results) | [Google Search Console Performance](https://search.google.com/search-console/performance) | [PageSpeed Insights](https://developers.google.com/speed/pagespeed/insights/)")

# Interface utilisateur avec Streamlit
st.title('SEO Analysis Tool')

url = st.text_input('Entrez une URL à analyser :')

if url:
    seo_analysis(url)
