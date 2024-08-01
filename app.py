import streamlit as st
import requests
import json

# API endpoint
API_URL = "https://api.example.com/api/guatemala_laws"  # Replace with the actual API URL

def get_law_info(query, article=None, year=None, category=None):
    params = {
        "query": query,
        "article": article,
        "year": year,
        "category": category
    }
    
    response = requests.get(API_URL, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error al obtener información: {response.status_code}")
        return None

def display_law_info(law_info):
    if law_info and 'law' in law_info:
        law = law_info['law']
        st.subheader(law['name'])
        st.write(f"Decreto: {law['decree']}")
        st.write(f"Última modificación: {law['lastAmendment']}")
        
        if 'article' in law:
            article = law['article']
            st.subheader(f"Artículo {article['number']}: {article['title']}")
            st.write(article['content'])
            if article['relatedArticles']:
                st.write("Artículos relacionados:", ", ".join(map(str, article['relatedArticles'])))
        
        st.write(f"Categoría: {law['category']}")
        st.write(f"En vigor: {'Sí' if law['inForce'] else 'No'}")
        
        if 'metadata' in law_info:
            st.subheader("Metadata")
            st.write(f"Total de artículos: {law_info['metadata']['totalArticles']}")
            st.write(f"Última actualización: {law_info['metadata']['lastUpdate']}")
    else:
        st.warning("No se encontró información para la consulta proporcionada.")

st.title("Consulta de Leyes de Guatemala")

query = st.text_input("Ingrese su consulta sobre leyes guatemaltecas:")
col1, col2, col3 = st.columns(3)
with col1:
    article = st.number_input("Número de artículo (opcional):", min_value=1, value=None)
with col2:
    year = st.number_input("Año (opcional):", min_value=1821, max_value=2100, value=None)
with col3:
    category = st.text_input("Categoría (opcional):")

if st.button("Buscar"):
    if query:
        with st.spinner("Buscando información..."):
            law_info = get_law_info(query, article, year, category)
            display_law_info(law_info)
    else:
        st.warning("Por favor, ingrese una consulta.")

st.sidebar.title("Acerca de")
st.sidebar.info(
    "Esta aplicación permite consultar información sobre las leyes de Guatemala. "
    "Utiliza una API que proporciona acceso a la legislación guatemalteca actual, "
    "incluyendo códigos legales, enmiendas y regulaciones."
)
st.sidebar.title("Instrucciones")
st.sidebar.markdown(
    """
    1. Ingrese su consulta en el campo de texto.
    2. Opcionalmente, puede especificar un número de artículo, año o categoría.
    3. Haga clic en 'Buscar' para obtener la información.
    4. Los resultados se mostrarán debajo del botón de búsqueda.
    """
)
