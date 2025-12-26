import streamlit as st
import os
import math
from PIL import Image

# --- KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="Moje Portfolio AI-Makaroni",
    page_icon="🎨",
    layout="wide"
)

# --- CSS (STYLE) ---
st.markdown("""
    <style>
        div[data-testid="column"] {
            padding: 5px;
        }
        img {
            border-radius: 8px;
        }
        /* Styl dla przycisków nawigacji na dole */
        .stButton button {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# --- FUNKCJA: DOPASOWANIE Z TŁEM ---
def dopasuj_z_tlem(image, kolor_tla=(14, 17, 23)):
    width, height = image.size
    nowy_wymiar = max(width, height)
    nowe_zdjecie = Image.new("RGB", (nowy_wymiar, nowy_wymiar), kolor_tla)
    pozycja_x = (nowy_wymiar - width) // 2
    pozycja_y = (nowy_wymiar - height) // 2
    nowe_zdjecie.paste(image, (pozycja_x, pozycja_y))
    return nowe_zdjecie

# --- INICJALIZACJA SESJI (PAMIĘĆ STRONY) ---
# To pozwala zapamiętać, na której stronie galerii jesteś
if 'strona_galerii' not in st.session_state:
    st.session_state.strona_galerii = 0

# --- POBIERANIE PLIKÓW ---
folder_zdjec = "images"
if not os.path.exists(folder_zdjec):
    os.makedirs(folder_zdjec)

# Pobieramy pliki i sortujemy alfabetycznie (lub można po dacie)
pliki = sorted([f for f in os.listdir(folder_zdjec) if f.endswith(('.jpg', '.jpeg', '.png', '.webp'))])

# --- PANEL BOCZNY (USTAWIENIA) ---
with st.sidebar:
    st.header("⚙️ Ustawienia widoku")
    
    # Suwak: Ile kolumn?
    ile_kolumn = st.slider("Liczba kolumn", min_value=1, max_value=5, value=3)
    
    # Suwak: Ile zdjęć na stronę?
    ile_na_strone = st.select_slider("Zdjęć na stronę", options=[3, 6, 9, 12, 15, 20, 50], value=9)
    
    st.divider()
    st.write(f"📂 Razem prac: **{len(pliki)}**")

# --- GŁÓWNA TREŚĆ ---
st.title("Moje Portfolio AI")

if not pliki:
    st.info("Folder 'images' jest pusty. Dodaj swoje prace!")
else:
    # --- LOGIKA STRONICOWANIA ---
    liczba_stron = math.ceil(len(pliki) / ile_na_strone)
    
    # Zabezpieczenie (gdybyśmy zmienili liczbę zdjęć i strona wyszła poza zakres)
    if st.session_state.strona_galerii >= liczba_stron:
        st.session_state.strona_galerii = 0

    start_index = st.session_state.strona_galerii * ile_na_strone
    end_index = start_index + ile_na_strone
    
    # Wycinamy tylko ten fragment listy plików, który chcemy teraz pokazać
    pliki_na_teraz = pliki[start_index:end_index]

    # Informacja o stronie
    st.caption(f"Strona {st.session_state.strona_galerii + 1} z {liczba_stron}")
    
    # Pasek postępu (wizualny bajer)
    postep = (st.session_state.strona_galerii + 1) / liczba_stron
    st.progress(postep)

    # --- WYŚWIETLANIE ZDJĘĆ ---
    cols = st.columns(ile_kolumn)
    
    for index, plik in enumerate(pliki_na_teraz):
        sciezka = os.path.join(folder_zdjec, plik)
        try:
            img = Image.open(sciezka)
            img_square = dopasuj_z_tlem(img)
            
            with cols[index % ile_kolumn]:
                st.image(img_square, use_container_width=True)
                
        except Exception:
            pass

    st.divider()

    # --- PRZYCISKI NAWIGACJI (Poprzednia / Następna) ---
    col_prev, col_info, col_next = st.columns([1, 2, 1])

    with col_prev:
        if st.session_state.strona_galerii > 0:
            if st.button("⬅️ Poprzednia"):
                st.session_state.strona_galerii -= 1
                st.rerun() # Przeładowanie strony

    with col_next:
        if st.session_state.strona_galerii < liczba_stron - 1:
            if st.button("Następna ➡️"):
                st.session_state.strona_galerii += 1

                st.rerun() # Przeładowanie strony
