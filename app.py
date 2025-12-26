import streamlit as st
import os
import math
from PIL import Image

# --- KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="Moje Portfolio AI",
    page_icon="🎨",
    layout="wide"
)

# --- CSS (STYLE - TU ROBIMY MAGIĘ Z ROGAMI) ---
st.markdown("""
    <style>
        /* Odstępy między kolumnami */
        div[data-testid="column"] {
            padding: 5px;
        }
        /* STYL ZDJĘĆ: Zaokrąglone rogi i cień */
        img {
            border-radius: 15px; /* Tu ustawiamy zaokrąglenie (im więcej, tym bardziej okrągłe) */
            box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* Delikatny cień dla głębi */
            transition: transform 0.2s; /* Płynna animacja */
        }
        img:hover {
            transform: scale(1.02); /* Lekkie powiększenie po najechaniu myszką */
        }
        /* Styl przycisków nawigacji */
        .stButton button {
            width: 100%;
            border-radius: 10px;
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

# --- INICJALIZACJA SESJI ---
if 'strona_galerii' not in st.session_state:
    st.session_state.strona_galerii = 0

# --- POBIERANIE PLIKÓW (Z poprawką na DUŻE litery) ---
folder_zdjec = "images"
if not os.path.exists(folder_zdjec):
    os.makedirs(folder_zdjec)

pliki = sorted([f for f in os.listdir(folder_zdjec) if f.endswith(('.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG'))])

# --- PANEL BOCZNY (USTAWIENIA) ---
with st.sidebar:
    st.header("⚙️ Ustawienia")
    ile_kolumn = st.slider("Liczba kolumn", 1, 5, 3)
    ile_na_strone = st.select_slider("Zdjęć na stronę", options=[3, 6, 9, 12, 15, 20, 50], value=9)
    st.divider()
    st.write(f"📂 Razem prac: **{len(pliki)}**")
    st.info("Autor: Twój Nick/Imię\nTechnologia: Gemini & Python")

# --- GŁÓWNA TREŚĆ (NAGŁÓWEK) ---

# Tytuł Główny
st.title("✨ Moje Portfolio AI")

# Sekcja wprowadzająca (O Tobie)
with st.container():
    st.markdown("""
    ### Witaj w mojej cyfrowej galerii! 👋
    Poniżej prezentuję zbiór moich najlepszych grafik wygenerowanych przy użyciu sztucznej inteligencji (**Gemini**, **Midjourney**).
    
    Każdy obraz to wynik eksperymentów z promptami, światłem i kompozycją. Zapraszam do oglądania!
    """)

st.divider()

# --- LOGIKA GALERII ---
if not pliki:
    st.warning("Folder 'images' jest pusty. Dodaj swoje prace na GitHub!")
else:
    liczba_stron = math.ceil(len(pliki) / ile_na_strone)
    
    if st.session_state.strona_galerii >= liczba_stron:
        st.session_state.strona_galerii = 0

    start_index = st.session_state.strona_galerii * ile_na_strone
    end_index = start_index + ile_na_strone
    pliki_na_teraz = pliki[start_index:end_index]

    # Licznik stron
    st.caption(f"Strona {st.session_state.strona_galerii + 1} z {liczba_stron}")
    st.progress((st.session_state.strona_galerii + 1) / liczba_stron)

    # Wyświetlanie
    cols = st.columns(ile_kolumn)
    
    for index, plik in enumerate(pliki_na_teraz):
        sciezka = os.path.join(folder_zdjec, plik)
        try:
            img = Image.open(sciezka)
            img_square = dopasuj_z_tlem(img)
            
            with cols[index % ile_kolumn]:
                st.image(img_square, use_container_width=True)
                # Opcjonalnie: Jeśli jednak chciałbyś mały, dyskretny podpis, odkomentuj linię niżej:
                # st.caption(plik.split('.')[0])
                
        except Exception:
            pass

    st.divider()

    # Nawigacja
    col_prev, col_info, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.session_state.strona_galerii > 0:
            if st.button("⬅️ Poprzednia"):
                st.session_state.strona_galerii -= 1
                st.rerun()
    with col_next:
        if st.session_state.strona_galerii < liczba_stron - 1:
            if st.button("Następna ➡️"):
                st.session_state.strona_galerii += 1
                st.rerun()
