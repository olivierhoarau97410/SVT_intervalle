import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import random
from scipy import stats
import plotly.graph_objects as go

# Configuration responsive
st.set_page_config(
    page_title="Savoir calculer la fréquence d'un caractère avec une confiance de 95%", 
    layout="centered"
)

# --- ENJEUX DE L'APP ---
st.title("Échantillonner pour compter c'est tout un art 🐠")
st.info("""
**On veut comprendre comment on peut déterminer la proportion d'un caractère parmi d'autres, 
en étant sûr à 95 % et avec **une seule campagne de mesures** ou **échantillonnage.**
""")

st.divider()

# --- PRÉSENTATION DU DOCUMENT ---
st.markdown("### ACTIVITÉ 1 : Deux phénotypes de l'épervier strié (*Paracirrhites arcatus*)")
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
boat_x, boat_y = img_width - 150, -15
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


# Instructions pédagogiques
st.info("""
💡 **Procédez à 10 captures pour commencer et observez le graphique sous le tableau de mesures.**

💡💡 **Augmentez progressivement le nombre de captures et observez les changements graphiques.**
""")

# Deux colonnes pour les deux zones
col_sup, col_prof = st.columns(2)

# --- ZONE SUPERFICIELLE ---
with col_sup:
    st.markdown("### ⬆️ Eaux superficielles")
    st.write(f"On cherche la proportion de formes sombres🐟 / claires 🐠")
    
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
    st.markdown("### ⬇️ Eaux profondes")
    st.write(f"On cherche la proportion de formes sombres 🐟/claires 🐠")
    
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
    **La question à se poser quand on observe le graphique :**
    
    Les fréquences de poissons 🐟 sombres / 🐠 clairs, à la surface et en profondeur sont-elles différentes ? 
    
    **Et surtout : EN SUIS-JE CERTAIN.E ? 🤔**
    """)
    
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
            n_total = (i + 1) * 5
            f_moyen = df_sup.loc[:i, 'freq_sombres'].mean()
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

# --- ACTIVITÉ 2 : GRAPHIQUE EN CLOCHE ---
st.subheader("💡 ACTIVITÉ 2 : Comprendre l'influence de la taille de l'échantillon")

st.write("""
La précision de notre estimation dépend de la taille de l'échantillon. 
Plus n est grand, plus notre intervalle de confiance est étroit (= plus précis).

**Déplacez le curseur pour voir comment la courbe en cloche se resserre quand l'effectif augmente !**
""")

n_simu = st.slider(
    "🎚️ Taille de l'échantillon (n) :", 
    min_value=5, 
    max_value=500, 
    value=5,
    step=5
)

# Utiliser f du premier échantillon disponible (superficiel ou profond) ou valeur par défaut
f_simu = 0.5
if st.session_state.echantillons_superficiel:
    f_simu = st.session_state.echantillons_superficiel[0]['freq_sombres']
elif st.session_state.echantillons_profond:
    f_simu = st.session_state.echantillons_profond[0]['freq_sombres']

# Calculer l'intervalle de confiance
marge_simu = 1.96 * np.sqrt((f_simu * (1 - f_simu)) / n_simu)
ic_min_simu = max(0, f_simu - marge_simu)
ic_max_simu = min(1, f_simu + marge_simu)
amplitude = ic_max_simu - ic_min_simu

# Créer la courbe en cloche (distribution normale)
# Générer les points pour la courbe normale
x_values = np.linspace(0, 1, 1000)
# Écart-type de la distribution
std_dev = np.sqrt((f_simu * (1 - f_simu)) / n_simu)
# Fonction de densité normale
y_values = stats.norm.pdf(x_values, f_simu, std_dev)

# Normaliser pour que le pic soit à 1
y_values = y_values / y_values.max()

fig_cloche = go.Figure()

# Tracer la courbe en cloche complète (en gris clair avec remplissage)
fig_cloche.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines',
    line=dict(color='#888888', width=3),
    name='Distribution',
    fill='tozeroy',
    fillcolor='rgba(200, 200, 200, 0.3)',
    showlegend=True
))

# Ajouter une ligne verticale pour la fréquence observée (ligne rouge pointillée)
fig_cloche.add_trace(go.Scatter(
    x=[f_simu, f_simu],
    y=[0, 1],
    mode='lines',
    line=dict(color='red', width=3, dash='dash'),
    name=f'f observée = {f_simu:.2f}',
    showlegend=True
))

# Position verticale pour la ligne d'intervalle (20% de la hauteur max)
y_ligne_ic = 0.2

# LIGNE HORIZONTALE BORNÉE pour l'intervalle de confiance à 95%
fig_cloche.add_trace(go.Scatter(
    x=[ic_min_simu, ic_max_simu],
    y=[y_ligne_ic, y_ligne_ic],
    mode='lines+markers',
    line=dict(color='#4169E1', width=4),
    marker=dict(size=12, symbol='line-ns', line=dict(width=3, color='#4169E1')),
    name='IC 95%',
    showlegend=True,
    hovertemplate='IC 95%: [%{x:.3f}]<extra></extra>'
))

# Annotations pour les limites de l'IC avec flèches
fig_cloche.add_annotation(
    x=ic_min_simu,
    y=y_ligne_ic,
    text=f"<b>{ic_min_simu:.3f}</b>",
    showarrow=True,
    arrowhead=2,
    arrowcolor="#4169E1",
    ax=0,
    ay=-50,
    font=dict(size=13, color="#4169E1", family="Arial Black"),
    bgcolor="white",
    bordercolor="#4169E1",
    borderwidth=2
)

fig_cloche.add_annotation(
    x=ic_max_simu,
    y=y_ligne_ic,
    text=f"<b>{ic_max_simu:.3f}</b>",
    showarrow=True,
    arrowhead=2,
    arrowcolor="#4169E1",
    ax=0,
    ay=-50,
    font=dict(size=13, color="#4169E1", family="Arial Black"),
    bgcolor="white",
    bordercolor="#4169E1",
    borderwidth=2
)

# Annotation pour indiquer "Intervalle de confiance 95%"
fig_cloche.add_annotation(
    x=(ic_min_simu + ic_max_simu) / 2,
    y=y_ligne_ic,
    text="<b>IC 95%</b>",
    showarrow=False,
    yshift=20,
    font=dict(size=14, color="#4169E1", family="Arial Black"),
    bgcolor="rgba(255,255,255,0.8)",
    bordercolor="#4169E1",
    borderwidth=2
)

fig_cloche.update_layout(
    title=f"Distribution de probabilité de la fréquence (n={n_simu})",
    xaxis_title="Fréquence de poissons sombres",
    yaxis_title="Densité de probabilité (normalisée)",
    yaxis=dict(range=[0, 1.1]),
    xaxis=dict(range=[0, 1]),
    height=450,
    showlegend=True,
    hovermode='x'
)

st.plotly_chart(fig_cloche, use_container_width=True)

# Afficher les métriques
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Taille échantillon (n)", n_simu)
with col2:
    st.metric("Amplitude IC 95%", f"{amplitude*100:.1f}%")
with col3:
    precision = "Haute 🎯" if amplitude < 0.1 else "Moyenne 📊" if amplitude < 0.3 else "Faible 📉"
    st.metric("Précision", precision)

if n_simu < 50:
    st.warning("⚠️ **Effectif faible** : La courbe est très étalée, l'intervalle est large. L'estimation est **peu précise**.")
elif n_simu < 200:
    st.info("📊 **Effectif moyen** : La courbe se resserre, l'intervalle est plus étroit. L'estimation est **moyennement précise**.")
else:
    st.success("✅ **Effectif élevé** : La courbe est très resserrée, l'intervalle est étroit. L'estimation est **très précise** !")

st.info("""
**💡 Observation clé** : 
- Avec un **petit n** → courbe **large** → grande incertitude 📉
- Avec un **grand n** → courbe **étroite** → faible incertitude 🎯
- Le pic est toujours à la fréquence observée, mais la **certitude augmente** avec n !
""")

st.divider()

# --- QUIZ INTERACTIF ---
st.subheader("🎯 Quiz : Avez-vous bien compris ?")

st.write("Répondez à ces 3 questions pour débloquer les points clés à retenir ! 🎈")

# Initialiser le score dans session state
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_reponses' not in st.session_state:
    st.session_state.quiz_reponses = [None, None, None]
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = [False, False, False]

# Question 1
st.markdown("### Question 1 : Que représente la zone bleue sur le graphique en cloche ?")
q1_options = [
    "La probabilité que la fréquence observée soit exacte",
    "L'intervalle de confiance à 95% où se trouve la vraie fréquence",
    "La marge d'erreur maximale possible",
    "La zone où on est sûr à 100% de trouver la vraie valeur"
]
q1_reponse = st.radio("", q1_options, key="q1", index=None)

if q1_reponse and not st.session_state.quiz_submitted[0]:
    if q1_reponse == q1_options[1]:  # Bonne réponse
        st.success("✅ Bravo ! La zone bleue représente bien l'intervalle de confiance à 95%.")
        st.session_state.quiz_reponses[0] = True
        st.session_state.quiz_submitted[0] = True
    else:
        st.error("❌ Pas tout à fait... Rejouez avec le curseur et observez comment la zone bleue évolue !")
        st.session_state.quiz_reponses[0] = False

# Question 2
st.markdown("### Question 2 : Que se passe-t-il quand on augmente la taille de l'échantillon (n) ?")
q2_options = [
    "La courbe s'élargit",
    "La courbe se resserre",
    "La fréquence observée change",
    "L'intervalle de confiance reste identique"
]
q2_reponse = st.radio("", q2_options, key="q2", index=None)

if q2_reponse and not st.session_state.quiz_submitted[1]:
    if q2_reponse == q2_options[1]:  # Bonne réponse
        st.success("✅ Exact ! Plus n augmente, plus la courbe se resserre (devient étroite).")
        st.session_state.quiz_reponses[1] = True
        st.session_state.quiz_submitted[1] = True
    else:
        st.error("❌ Essayez de déplacer le curseur de gauche à droite et observez bien ce qui se passe !")
        st.session_state.quiz_reponses[1] = False

# Question 3
st.markdown("### Question 3 : Avec un échantillon de n=5 poissons, quelle est la précision de notre estimation ?")
q3_options = [
    "Très précise, on peut être certain de la vraie fréquence",
    "Moyennement précise, l'intervalle est assez étroit",
    "Peu précise, l'intervalle est très large",
    "Impossible à déterminer sans faire plus de captures"
]
q3_reponse = st.radio("", q3_options, key="q3", index=None)

if q3_reponse and not st.session_state.quiz_submitted[2]:
    if q3_reponse == q3_options[2]:  # Bonne réponse
        st.success("✅ Parfait ! Avec n=5, l'intervalle est énorme (très large), donc peu précis.")
        st.session_state.quiz_reponses[2] = True
        st.session_state.quiz_submitted[2] = True
    else:
        st.error("❌ Remettez le curseur à n=5 et regardez la largeur de la zone bleue...")
        st.session_state.quiz_reponses[2] = False

# Vérifier si toutes les réponses sont correctes
if all(st.session_state.quiz_reponses) and all(st.session_state.quiz_submitted):
    st.balloons()
    st.success("🎉🎈 BRAVO ! Vous avez tout compris ! Les points clés sont maintenant débloqués ci-dessous ! 🎈🎉")

# Bouton pour réinitialiser le quiz
if st.button("🔄 Réessayer le quiz"):
    st.session_state.quiz_score = 0
    st.session_state.quiz_reponses = [None, None, None]
    st.session_state.quiz_submitted = [False, False, False]
    st.rerun()

# --- CONCLUSION PÉDAGOGIQUE ---
st.divider()

# Afficher la conclusion seulement si le quiz est réussi
if all(st.session_state.quiz_reponses) and all(st.session_state.quiz_submitted):
    st.subheader("🎯 Points clés à retenir (débloqués ! 🔓)")
    
    st.success("""
    **Points clés à retenir :**
    1. Un échantillon permet d'estimer une proportion dans une population
    2. L'intervalle de confiance à 95% nous donne une marge d'erreur
    3. Plus l'échantillon est grand (n ↑), plus l'estimation est précise (courbe se resserre)
    4. Avec un seul échantillon, on peut avoir 95% de confiance dans notre estimation mais TOUJOURS avec une marge d'erreur +/- grande
    5. Le "prix à payer" 💰 : il faut capturer beaucoup de poissons pour être très précis !
    """)
else:
    st.subheader("🎯 Points clés à retenir")
    st.warning("🔒 **Répondez correctement aux 3 questions du quiz pour débloquer les points clés !**")