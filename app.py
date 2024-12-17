import streamlit as st

def seo_analysis(url):
    st.title("Analyse SEO de l'URL")
    
    # Récupérer le contenu de la page
    html, status_code, headers = fetch_page(url)
    if html is None:
        st.error(f"Impossible de récupérer la page {url}")
        return
    
    # Afficher le statut de la page
    st.subheader(f"Code de statut HTTP : {status_code}")
    
    # Extraire les meta données
    soup = BeautifulSoup(html, 'html.parser')
    meta_data = extract_meta_data(soup)
    st.subheader("Meta Tags")
    st.write(f"Title: {meta_data['title']}")
    st.write(f"Description: {meta_data['description']}")
    st.write(f"Robots: {meta_data['robots']}")
    st.write(f"Canonical: {meta_data['canonical']}")
    
    # Vérifier si la page est indexée
    indexed = check_if_indexed(url)
    st.write(f"Indexée sur Google : {'Oui' if indexed else 'Non'}")
    
    # Extraire les liens internes et externes
    links = extract_links(soup, url)
    st.subheader("Liens internes et externes")
    st.write(f"Liens internes : {len(links['internal'])}")
    st.write(f"Liens externes : {len(links['external'])}")
    
    # Vérifier la validité des liens
    link_status = check_link_status(links['internal'] + links['external'])
    st.subheader("Statut des liens")
    for link, status in link_status.items():
        st.write(f"{link}: {status if status else 'Erreur'}")
    
    # Analyser les images
    images = extract_images(soup, url)
    st.subheader("Images")
    for img in images:
        st.write(f"Image: {img['src']}, Taille: {img['size']:.2f} Ko, Alt: {img['alt']}")
    
# Interface Streamlit
if __name__ == "__main__":
    url = st.text_input("Entrez l'URL de la page à analyser", "")
    if url:
        seo_analysis(url)
