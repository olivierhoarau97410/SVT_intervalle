import streamlit as st
import numpy as np

# Configuration responsive
st.set_page_config(page_title="Savoir calculer la fréquence d'un caractère avec une confiance de 95%", layout="centered")

# --- ENJEUX DE L'APP ---
st.title("🔬 Échantillonnage et Biodiversité")
st.info("""
**On veut comprendre comment on peut déterminer la proportion d'un caractère parmi d'autres, 
en étant sûr à 95 % et avec un seul échantillon, pris une seule fois.**
""")

st.divider()

# --- PRÉSENTATION DU DOCUMENT ---
# Texte du document (Capture 3)
st.markdown("### Document 1 : Deux phénotypes de l'épervier strié (*Paracirrhites arcatus*) ")
st.write("""
*L’épervier strié est un poisson qui vit dans les récifs coralliens. Il existe sous deux phénotypes : 
sombre et clair. Un recensement des formes claires et sombres a été effectué le long de 
cinquante-quatre transects, de la surface jusqu’au fond du lagon.*
""")

# Affichage de l'image (Doc 1 - Capture 1)
# Assure-toi d'avoir l'image dans ton dossier Cursor
# st.image("epervier_strié.jpg", caption="Phénotypes de l'épervier strié")

# --- DONNÉES ET CALCULS ---
st.subheader("📊 Données de l'étude")

# Tableau des données
data = {
    "Zone": ["Eaux superficielles (< 5 m)", "Eaux profondes (> 5 m)"],
    "Sombres": [538, 20],
    "Clairs": [310, 238]
}

# Sélection de la zone pour l'élève
zone = st.radio("Choisissez la population à analyser :", data["Zone"])

# Extraction des valeurs selon la zone
if zone == "Eaux superficielles (< 5 m)":
    sombres = 538
    clairs = 310
else:
    sombres = 20
    clairs = 238

n = sombres + clairs
f = sombres / n

# Formule du Document 2 (Capture 1)
st.latex(r"IC = \left[ f - 1,96 \sqrt{\frac{f(1-f)}{n}} \ ; \ f + 1,96 \sqrt{\frac{f(1-f)}{n}} \right]")

# Calcul de l'IC
marge = 1.96 * np.sqrt((f * (1 - f)) / n)
ic_min = f - marge
ic_max = f + marge

# --- RÉSULTATS ---
col1, col2 = st.columns(2)
with col1:
    st.metric("Taille échantillon (n)", n)
    st.metric("Fréquence observée (f)", f"{f:.3f}")

with col2:
    st.write("**Résultat de l'estimation :**")
    st.success(f"Proportion $p$ comprise entre **{ic_min:.3f}** et **{ic_max:.3f}**")
    st.write(f"Soit entre **{ic_min*100:.1f} %** et **{ic_max*100:.1f} %**.")

st.divider()

# --- INTERACTIVITÉ SUR LA TAILLE DE L'ÉCHANTILLON (Question 3) ---
st.subheader("💡 Comprendre l'influence de la taille de l'échantillon")
n_simu = st.slider("Modifiez la taille de l'échantillon (n) pour voir l'effet sur la précision :", 
                   min_value=50, max_value=2000, value=n)

# Recalcul de la marge avec n variable
marge_simu = 1.96 * np.sqrt((f * (1 - f)) / n_simu)
st.write(f"Amplitude de l'intervalle de confiance : **{marge_simu * 2 * 100:.2f} %**")

if n_simu > n:
    st.write("✅ **Plus n est grand**, plus l'intervalle est petit : l'estimation est **plus précise**.")
else:
    st.write("⚠️ **Plus n est petit**, plus l'intervalle est large : l'estimation est **moins précise**.")