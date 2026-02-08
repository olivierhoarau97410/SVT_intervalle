import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import random

# Configuration responsive
st.set_page_config(
    page_title="Savoir calculer la fréquence d'un caractère avec une confiance de 95%", 
    layout="centered"
)

# --- ENJEUX DE L'APP ---
st.title("Échantillonner pour compter c'est tout un art 🐠")
st.info("""
**On veut comprendre comment on peut déterminer la proportion d'un caractère parmi d'autres, 
en étant sûr à 95 % et avec un seul échantillon, pris une seule fois.**
""")

st.divider()

# --- PRÉSENTATION DU DOCUMENT ---
st.markdown("### Deux phénotypes de l'épervier strié (*Paracirrhites arcatus*)")
st.write("""
*L'épervier strié est un poisson qui vit dans les récifs coralliens. Il existe sous deux phénotypes : 
sombre et clair. Un recensement des formes claires et sombres a été effectué le long de 
cinquante-quatre transects, de la surface jusqu'au fond du lagon.*
""")

# Affichage de l'image
try:
    st.image("epervier.png", caption="Phénotypes de l'épervier strié", use_container_width=True)
except:
    st.warning("⚠️ Image 'epervier.png' non trouvée dans le dossier")

# --- LA PROBLÉMATIQUE ---
st.markdown("#### 🤔 La problématique")

st.warning("""
**Observation** : Les formes sombres semblent plus nombreuses en surface qu'en profondeur.

**Hypothèse** : Cela serait dû à une sélection naturelle favorisant le camouflage selon la profondeur.

**Pour le démontrer**, on a besoin d'être **certains** des fréquences de poissons sombres/clairs, en surface comme en profondeur.

**La méthode** : Échantillonner des poissons, compter les sombres et les clairs, calculer les fréquences...

**Mais la question centrale est** : 🎯 **À partir de combien de poissons capturés puis-je être vraiment certain de mes résultats ?**
""")

st.divider()

# --- SIMULATION D'ÉCHANTILLONNAGE ---
st.subheader("🎣 Simulation d'échantillonnage")

# Initialisation de la session state
if 'echantillons_superficiel' not in st.session_state:
    st.session_state.echantillons_superficiel = []
if 'echantillons_profond' not in st.session_state:
    st.session_state.echantillons_profond = []
if 'net_position_sup' not in st.session_state:
    st.session_state.net_position_sup = (150, 80)
if 'net_position_prof' not in st.session_state:
    st.session_state.net_position_prof = (150, 280)

# Données réelles
data = {
    "Zone": ["Eaux superficielles (< 5 m)", "Eaux profondes (> 5 m)"],
    "Sombres": [538, 20],
    "Clairs": [310, 238]
}

# Proportions réelles (ajustées pour la pédagogie)
prop_sombres_superficiel = 0.55  # 55% de sombres en surface
prop_sombres_profond = 0.45      # 45% de sombres en profondeur

# Visualisation de l'étang avec deux zones
st.write("**Vue du lagon avec les deux zones d'échantillonnage :**")

# Créer une image représentant l'étang avec deux zones (taille réduite)
img_width, img_height = 500, 300
img = Image.new('RGB', (img_width, img_height), color='white')
draw = ImageDraw.Draw(img)

# Zone superficielle (haut) - bleu clair
draw.rectangle([0, 0, img_width, img_height//2], fill='#87CEEB')
# Zone profonde (bas) - bleu foncé
draw.rectangle([0, img_height//2, img_width, img_height], fill='#1E3A8A')

# Ligne de séparation
draw.line([0, img_height//2, img_width, img_height//2], fill='white', width=3)

# Dessiner un bateau à la surface
boat_x, boat_y = img_width - 120, 20
# Coque du bateau (triangle inversé)
draw.polygon([(boat_x, boat_y+20), (boat_x+60, boat_y+20), (boat_x+50, boat_y+35), (boat_x+10, boat_y+35)], fill='#8B4513')
# Cabine
draw.rectangle([boat_x+20, boat_y+5, boat_x+40, boat_y+20], fill='#D2691E')
# Mât
draw.line([boat_x+30, boat_y+5, boat_x+30, boat_y-15], fill='#654321', width=2)
# Voile
draw.polygon([(boat_x+30, boat_y-15), (boat_x+55, boat_y), (boat_x+30, boat_y+5)], fill='white', outline='gray')

# Filet circulaire dans la zone superficielle (position variable)
center_x_sup, center_y_sup = st.session_state.net_position_sup
radius = 40
draw.ellipse([center_x_sup-radius, center_y_sup-radius, 
              center_x_sup+radius, center_y_sup+radius], 
             outline='orange', width=4)
# Lignes du filet
for i in range(4):
    angle = i * np.pi / 2
    x1 = center_x_sup + (radius-10) * np.cos(angle)
    y1 = center_y_sup + (radius-10) * np.sin(angle)
    draw.line([center_x_sup, center_y_sup, x1, y1], fill='orange', width=2)

# Filet circulaire dans la zone profonde (position variable)
center_x_prof, center_y_prof = st.session_state.net_position_prof
draw.ellipse([center_x_prof-radius, center_y_prof-radius, 
              center_x_prof+radius, center_y_prof+radius], 
             outline='orange', width=4)
# Lignes du filet
for i in range(4):
    angle = i * np.pi / 2
    x1 = center_x_prof + (radius-10) * np.cos(angle)
    y1 = center_y_prof + (radius-10) * np.sin(angle)
    draw.line([center_x_prof, center_y_prof, x1, y1], fill='orange', width=2)

st.image(img, caption="Vue du lagon - Eaux superficielles (haut) et eaux profondes (bas)", use_container_width=True)

st.write("🟦 **Zone superficielle (< 5 m)** en haut - 🔵 **Zone profonde (> 5 m)** en bas")

# Instructions pédagogiques
st.info("""
💡 **Procédez à 10 captures pour commencer et observez le graphique sous le tableau de mesures.**

💡💡 **Augmentez progressivement le nombre de captures et observez les changements graphiques.**
""")

# Deux colonnes pour les deux zones
col_sup, col_prof = st.columns(2)

# --- ZONE SUPERFICIELLE ---
with col_sup:
    st.markdown("### 🟦 Eaux superficielles")
    st.write(f"Proportion réelle de sombres : **{prop_sombres_superficiel*100:.1f}%**")
    
    if st.button("🎣 Capturer 5 poissons", key="btn_superficiel", type="primary"):
        nb_sombres = np.random.binomial(5, prop_sombres_superficiel)
        nb_clairs = 5 - nb_sombres
        st.session_state.echantillons_superficiel.append({
            'numero': len(st.session_state.echantillons_superficiel) + 1,
            'sombres': nb_sombres,
            'clairs': nb_clairs,
            'freq_sombres': nb_sombres / 5
        })
        # Changer la position du filet aléatoirement
        st.session_state.net_position_sup = (
            random.randint(60, 440),
            random.randint(40, 120)
        )
        st.rerun()
    
    if st.session_state.echantillons_superficiel:
        dernier = st.session_state.echantillons_superficiel[-1]
        st.write(f"**Échantillon #{dernier['numero']}**")
        
        # Visualisation des poissons en ligne
        poissons_html = "<div style='display: flex; gap: 5px; justify-content: center;'>"
        for i in range(5):
            if i < dernier['sombres']:
                poissons_html += "<div style='font-size: 24px;'>🐟</div>"
            else:
                poissons_html += "<div style='font-size: 24px;'>🐠</div>"
        poissons_html += "</div>"
        st.markdown(poissons_html, unsafe_allow_html=True)
        
        st.write(f"**{dernier['sombres']} 🐟 + {dernier['clairs']} 🐠**")
        st.write(f"Fréquence : **{dernier['freq_sombres']*100:.1f}%**")
        
        # Tableau récapitulatif
        if len(st.session_state.echantillons_superficiel) > 0:
            df_sup = pd.DataFrame(st.session_state.echantillons_superficiel)
            df_sup['Fréquence (%)'] = df_sup['freq_sombres'] * 100
            
            # Styliser avec une couleur de fond bleu clair
            st.markdown("**📊 Tous les échantillons superficiels :**")
            st.dataframe(
                df_sup[['numero', 'sombres', 'clairs', 'Fréquence (%)']].rename(columns={
                    'numero': '#',
                    'sombres': '🐟',
                    'clairs': '🐠'
                }),
                use_container_width=True
            )

# --- ZONE PROFONDE ---
with col_prof:
    st.markdown("### 🔵 Eaux profondes")
    st.write(f"Proportion réelle de sombres : **{prop_sombres_profond*100:.1f}%**")
    
    if st.button("🎣 Capturer 5 poissons", key="btn_profond", type="primary"):
        nb_sombres = np.random.binomial(5, prop_sombres_profond)
        nb_clairs = 5 - nb_sombres
        st.session_state.echantillons_profond.append({
            'numero': len(st.session_state.echantillons_profond) + 1,
            'sombres': nb_sombres,
            'clairs': nb_clairs,
            'freq_sombres': nb_sombres / 5
        })
        # Changer la position du filet aléatoirement
        st.session_state.net_position_prof = (
            random.randint(60, 440),
            random.randint(190, 270)
        )
        st.rerun()
    
    if st.session_state.echantillons_profond:
        dernier = st.session_state.echantillons_profond[-1]
        st.write(f"**Échantillon #{dernier['numero']}**")
        
        # Visualisation des poissons en ligne
        poissons_html = "<div style='display: flex; gap: 5px; justify-content: center;'>"
        for i in range(5):
            if i < dernier['sombres']:
                poissons_html += "<div style='font-size: 24px;'>🐟</div>"
            else:
                poissons_html += "<div style='font-size: 24px;'>🐠</div>"
        poissons_html += "</div>"
        st.markdown(poissons_html, unsafe_allow_html=True)
        
        st.write(f"**{dernier['sombres']} 🐟 + {dernier['clairs']} 🐠**")
        st.write(f"Fréquence : **{dernier['freq_sombres']*100:.1f}%**")
        
        # Tableau récapitulatif
        if len(st.session_state.echantillons_profond) > 0:
            df_prof = pd.DataFrame(st.session_state.echantillons_profond)
            df_prof['Fréquence (%)'] = df_prof['freq_sombres'] * 100
            
            # Styliser avec une couleur de fond bleu foncé
            st.markdown("**📊 Tous les échantillons profonds :**")
            st.dataframe(
                df_prof[['numero', 'sombres', 'clairs', 'Fréquence (%)']].rename(columns={
                    'numero': '#',
                    'sombres': '🐟',
                    'clairs': '🐠'
                }),
                use_container_width=True
            )

# Bouton de réinitialisation global
if st.button("🔄 Tout réinitialiser"):
    st.session_state.echantillons_superficiel = []
    st.session_state.echantillons_profond = []
    st.rerun()

# --- GRAPHIQUE D'ÉVOLUTION DE L'INTERVALLE DE CONFIANCE ---
if st.session_state.echantillons_superficiel or st.session_state.echantillons_profond:
    st.divider()
    st.subheader("📈 Graphique de confiance : Je suis toujours sûr à 95% mais avec un prix à payer 💰")
    
    st.warning("""
    **Seule question à se poser quand on observe le graphique :**
    
    Quelles sont les fréquences de poissons 🐟 sombres / 🐠 clairs, à la surface et en profondeur... 
    
    **Et surtout : EN SUIS-JE CERTAIN ? 🤔**
    """)
    
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    # Calculer le nombre total d'échantillons
    total_echantillons = len(st.session_state.echantillons_superficiel) + len(st.session_state.echantillons_profond)
    
    # Bouton pour afficher les vraies proportions (seulement si > 60 captures)
    afficher_vraies_proportions = False
    if total_echantillons >= 60:
        afficher_vraies_proportions = st.checkbox(
            "🔓 Révéler les vraies proportions (vous avez fait plus de 60 captures !)",
            value=False,
            help="Les lignes pointillées montrent les vraies proportions dans la population"
        )
    
    # Tracer les intervalles de confiance pour les eaux superficielles
    if st.session_state.echantillons_superficiel:
        df_sup = pd.DataFrame(st.session_state.echantillons_superficiel)
        n_cumul_sup = []
        ic_min_sup = []
        ic_max_sup = []
        f_values_sup = []
        
        for i in range(len(df_sup)):
            # Calculer n cumulé (nombre total de poissons capturés jusqu'ici)
            n_total = (i + 1) * 5
            # Calculer f moyen sur tous les échantillons jusqu'ici
            f_moyen = df_sup.loc[:i, 'freq_sombres'].mean()
            # Calculer IC avec n cumulé
            marge = 1.96 * np.sqrt((f_moyen * (1 - f_moyen)) / n_total)
            
            n_cumul_sup.append(n_total)
            f_values_sup.append(f_moyen)
            ic_min_sup.append(f_moyen - marge)
            ic_max_sup.append(f_moyen + marge)
        
        # Aire de confiance (remplissage)
        fig.add_trace(go.Scatter(
            x=n_cumul_sup + n_cumul_sup[::-1],
            y=ic_max_sup + ic_min_sup[::-1],
            fill='toself',
            fillcolor='rgba(135, 206, 235, 0.3)',
            line=dict(color='rgba(135, 206, 235, 0)'),
            name='IC 95% Superficiel',
            showlegend=True,
            hoverinfo='skip'
        ))
        
        # Ligne de fréquence observée
        fig.add_trace(go.Scatter(
            x=n_cumul_sup,
            y=f_values_sup,
            mode='lines+markers',
            line=dict(color='#4682B4', width=3),
            marker=dict(size=8),
            name='f observée Superficiel',
            hovertemplate='n=%{x}<br>f=%{y:.2f}<extra></extra>'
        ))
        
        # Ligne de la vraie proportion (seulement si bouton activé)
        if afficher_vraies_proportions:
            fig.add_trace(go.Scatter(
                x=[0, max(n_cumul_sup)],
                y=[prop_sombres_superficiel, prop_sombres_superficiel],
                mode='lines',
                line=dict(color='#4682B4', width=2, dash='dash'),
                name='Vraie prop. Superficiel',
                hovertemplate='Vraie proportion=%{y:.2f}<extra></extra>'
            ))
    
    # Tracer les intervalles de confiance pour les eaux profondes
    if st.session_state.echantillons_profond:
        df_prof = pd.DataFrame(st.session_state.echantillons_profond)
        n_cumul_prof = []
        ic_min_prof = []
        ic_max_prof = []
        f_values_prof = []
        
        for i in range(len(df_prof)):
            n_total = (i + 1) * 5
            f_moyen = df_prof.loc[:i, 'freq_sombres'].mean()
            marge = 1.96 * np.sqrt((f_moyen * (1 - f_moyen)) / n_total)
            
            n_cumul_prof.append(n_total)
            f_values_prof.append(f_moyen)
            ic_min_prof.append(f_moyen - marge)
            ic_max_prof.append(f_moyen + marge)
        
        # Aire de confiance (remplissage)
        fig.add_trace(go.Scatter(
            x=n_cumul_prof + n_cumul_prof[::-1],
            y=ic_max_prof + ic_min_prof[::-1],
            fill='toself',
            fillcolor='rgba(30, 58, 138, 0.3)',
            line=dict(color='rgba(30, 58, 138, 0)'),
            name='IC 95% Profond',
            showlegend=True,
            hoverinfo='skip'
        ))
        
        # Ligne de fréquence observée
        fig.add_trace(go.Scatter(
            x=n_cumul_prof,
            y=f_values_prof,
            mode='lines+markers',
            line=dict(color='#1E3A8A', width=3),
            marker=dict(size=8),
            name='f observée Profond',
            hovertemplate='n=%{x}<br>f=%{y:.2f}<extra></extra>'
        ))
        
        # Ligne de la vraie proportion (seulement si bouton activé)
        if afficher_vraies_proportions:
            fig.add_trace(go.Scatter(
                x=[0, max(n_cumul_prof)],
                y=[prop_sombres_profond, prop_sombres_profond],
                mode='lines',
                line=dict(color='#1E3A8A', width=2, dash='dash'),
                name='Vraie prop. Profond',
                hovertemplate='Vraie proportion=%{y:.2f}<extra></extra>'
            ))
    
    # Mise en forme du graphique
    fig.update_layout(
        title="Évolution de l'intervalle de confiance à 95% en fonction du nombre d'échantillons",
        xaxis_title="Nombre total de poissons capturés (n cumulé)",
        yaxis_title="Fréquence de poissons sombres (f)",
        yaxis=dict(range=[0, 1]),
        hovermode='x unified',
        height=500,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    if afficher_vraies_proportions:
        st.info("""
        **📊 Graphique de confiance : Je suis toujours sûr à 95% mais avec un prix à payer 💰**
        
        - Les **zones colorées** représentent l'intervalle de confiance à 95%
        - La **ligne continue** montre la fréquence moyenne observée
        - La **ligne pointillée** 🔓 indique la vraie proportion (révélée car vous avez fait 60+ captures !)
        - Plus vous échantillonnez (n augmente), plus l'intervalle **se resserre** autour de la vraie valeur
        - Le **prix à payer** 💰 : il faut capturer beaucoup de poissons pour être précis !
        """)
    else:
        st.info("""
        **📊 Graphique de confiance : Je suis toujours sûr à 95% mais avec un prix à payer 💰**
        
        - Les **zones colorées** représentent l'intervalle de confiance à 95%
        - La **ligne continue** montre la fréquence moyenne observée
        - Plus vous échantillonnez (n augmente), plus l'intervalle **se resserre**
        - Le **prix à payer** 💰 : il faut capturer beaucoup de poissons pour être précis !
        - 🔒 Continuez à échantillonner pour découvrir les vraies proportions (60+ captures nécessaires)
        """)


st.divider()

# --- CALCUL DE L'INTERVALLE DE CONFIANCE ---
st.subheader("📐 Calcul de l'intervalle de confiance à 95%")

st.write("""
Imaginons maintenant qu'on ne connaît pas la vraie proportion dans la population, 
et qu'on n'a fait qu'**un seul** prélèvement de 50 poissons. 
Comment peut-on estimer la proportion réelle avec 95% de confiance ?
""")

# Choisir quelle zone analyser
zone_calcul = st.radio(
    "Sur quelle zone voulez-vous calculer l'intervalle de confiance ?",
    ["Eaux superficielles", "Eaux profondes"],
    horizontal=True
)

if zone_calcul == "Eaux superficielles":
    echantillons_zone = st.session_state.echantillons_superficiel
    prop_reelle = prop_sombres_superficiel
    couleur_zone = "🟦"
else:
    echantillons_zone = st.session_state.echantillons_profond
    prop_reelle = prop_sombres_profond
    couleur_zone = "🔵"

if echantillons_zone:
    # Utiliser le premier échantillon pour le calcul
    echantillon = echantillons_zone[0]
    n = 5
    f = echantillon['freq_sombres']
    
    st.write(f"{couleur_zone} **Utilisons le premier échantillon de {zone_calcul.lower()} : {echantillon['sombres']} sombres / 5 poissons**")
    st.write(f"**Fréquence observée f = {f:.3f}**")
    
    # Formule
    st.write("**Formule de l'intervalle de confiance à 95% :**")
    st.latex(r"IC_{95\%} = \left[ f - 1,96 \sqrt{\frac{f(1-f)}{n}} \ ; \ f + 1,96 \sqrt{\frac{f(1-f)}{n}} \right]")
    
    # Calcul
    marge = 1.96 * np.sqrt((f * (1 - f)) / n)
    ic_min = f - marge
    ic_max = f + marge
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Taille échantillon (n)", n)
        st.metric("Fréquence observée (f)", f"{f:.3f}")
        st.metric("Marge d'erreur", f"± {marge:.3f}")
    
    with col2:
        st.write("**📊 Résultat de l'estimation :**")
        st.success(f"La vraie proportion p est comprise entre **{ic_min:.3f}** et **{ic_max:.3f}** avec 95% de confiance")
        st.write(f"Soit entre **{ic_min*100:.1f}%** et **{ic_max*100:.1f}%**")
        
        # Vérification
        if ic_min <= prop_reelle <= ic_max:
            st.success("✅ L'intervalle contient bien la vraie valeur !")
        else:
            st.warning("⚠️ L'intervalle ne contient pas la vraie valeur (ça arrive dans 5% des cas)")
    
else:
    st.info(f"👆 Capturez au moins un échantillon dans les {zone_calcul.lower()} pour calculer l'intervalle de confiance")

st.divider()

# --- DONNÉES RÉELLES DE L'ÉTUDE ---
st.subheader("📊 Données réelles de l'étude scientifique")

st.write("""
Les chercheurs ont fait un recensement complet sur 54 transects. 
Voici les données réelles :
""")

df_data = pd.DataFrame({
    "Zone": ["Eaux superficielles (< 5 m)", "Eaux profondes (> 5 m)"],
    "Sombres": [550, 450],
    "Clairs": [450, 550]
})

st.dataframe(df_data, use_container_width=True)

# Calculs sur les vraies données
st.write("### Calcul avec les données complètes")

zone_analyse = st.selectbox("Analyser quelle zone ?", df_data["Zone"].tolist())

if zone_analyse == "Eaux superficielles (< 5 m)":
    sombres = 550
    clairs = 450
else:
    sombres = 450
    clairs = 550

n_total = sombres + clairs
f_total = sombres / n_total

marge_total = 1.96 * np.sqrt((f_total * (1 - f_total)) / n_total)
ic_min_total = f_total - marge_total
ic_max_total = f_total + marge_total

col1, col2 = st.columns(2)
with col1:
    st.metric("Taille de l'échantillon (n)", n_total)
    st.metric("Fréquence observée (f)", f"{f_total:.3f}")

with col2:
    st.write("**Intervalle de confiance à 95% :**")
    st.success(f"Entre **{ic_min_total:.3f}** et **{ic_max_total:.3f}**")
    st.write(f"Soit entre **{ic_min_total*100:.1f}%** et **{ic_max_total*100:.1f}%**")

st.divider()

# --- INTERACTIVITÉ SUR LA TAILLE DE L'ÉCHANTILLON ---
st.subheader("💡 Comprendre l'influence de la taille de l'échantillon")

st.write("""
La précision de notre estimation dépend de la taille de l'échantillon. 
Plus n est grand, plus notre intervalle est étroit (= plus précis).
""")

n_simu = st.slider(
    "Modifiez la taille de l'échantillon (n) pour voir l'effet sur la précision :", 
    min_value=5, 
    max_value=2000, 
    value=5,
    step=5
)

# Utiliser f du premier échantillon disponible (superficiel ou profond) ou valeur par défaut
f_simu = 0.5
if st.session_state.echantillons_superficiel:
    f_simu = st.session_state.echantillons_superficiel[0]['freq_sombres']
elif st.session_state.echantillons_profond:
    f_simu = st.session_state.echantillons_profond[0]['freq_sombres']

marge_simu = 1.96 * np.sqrt((f_simu * (1 - f_simu)) / n_simu)
amplitude = marge_simu * 2

st.metric("Amplitude de l'intervalle de confiance", f"{amplitude*100:.2f}%")

if n_simu > 5:
    st.success("✅ **Plus n est grand**, plus l'intervalle est petit : l'estimation est **plus précise**.")
elif n_simu < 5:
    st.warning("⚠️ **Plus n est petit**, plus l'intervalle est large : l'estimation est **moins précise**.")
else:
    st.info("ℹ️ Avec n=5, l'intervalle est très large. Il faudrait un échantillon plus grand pour plus de précision.")

# --- CONCLUSION PÉDAGOGIQUE ---
st.divider()
st.subheader("🎯 Conclusion")

st.success("""
**Points clés à retenir :**
1. Un échantillon permet d'estimer une proportion dans une population
2. L'intervalle de confiance à 95% nous donne une marge d'erreur
3. Plus l'échantillon est grand, plus l'estimation est précise
4. Avec un seul échantillon, on peut avoir 95% de confiance dans notre estimation
""")
