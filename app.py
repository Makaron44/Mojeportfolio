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

# --- CSS (STYLE) ---
st.markdown("""
    <style>
        /* Odstępy między kolumnami */
        div[data-testid="column"] {
            padding: 5px;
        }
        /* STYL ZDJĘĆ */
        img {
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }
        img:hover {
            transform: scale(1.02);
        }
        /* Styl przycisków nawigacji */
        .stButton button {
            width: 100%;
            border-radius: 10px;
        }
        /* Wyśrodkowanie tekstu numeracji stron */
        .page-number {
            text-align: center; 
            line-height: 2.5em;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# --- FUNKCJA: DOPASOWANIE Z TŁEM (Z CACHE) ---
@st.cache_data
def dopasuj_z_tlem(image_path, kolor_tla=(14, 17, 23)):
    """Wczytuje zdjęcie, konwertuje do RGB i dodaje tło, aby było kwadratowe."""
    image = Image.open(image_path)
    
    # Konwersja do RGB (ważne przy przezroczystych PNG lub WebP)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    
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

# --- POBIERANIE PLIKÓW ---
folder_zdjec = "images"

# Jeśli folder nie istnieje, tworzymy go (żeby nie było błędu na starcie)
if not os.path.exists(folder_zdjec):
    os.makedirs(folder_zdjec)

# Lista akceptowanych rozszerzeń
rozszerzenia = ('.webp', '.png', '.jpg', '.jpeg', '.JPG', '.PNG', '.WEBP')

# Pobieranie plików (zabezpieczenie przed błędami wielkości liter)
pliki = sorted([f for f in os.listdir(folder_zdjec) if f.lower().endswith(rozszerzenia)])

# --- PANEL BOCZNY (USTAWIENIA) ---
with st.sidebar:
    st.header("⚙️ Ustawienia")
    ile_kolumn = st.slider("Liczba kolumn", 1, 5, 3)
    ile_na_strone = st.select_slider("Zdjęć na stronę", options=[3, 6, 9, 12, 15, 20, 50], value=12)
    st.divider()
    st.write(f"📂 Razem prac: **{len(pliki)}**")
    st.info("Autor: Maciej Ratajczak\nTechnologia: Gemini & Python")

# --- GŁÓWNA TREŚĆ ---
st.title("✨ Moje Portfolio AI")

with st.container():
    st.markdown("""
    ### Witaj w mojej cyfrowej galerii! 👋
    Poniżej prezentuję zbiór moich najlepszych grafik wygenerowanych przy użyciu sztucznej inteligencji.
    """)

st.divider()

# --- LOGIKA GALERII ---
if not pliki:
    st.warning(f"Folder '{folder_zdjec}' jest pusty lub nie istnieje. Dodaj zdjęcia .webp na GitHub!")
else:
    liczba_stron = math.ceil(len(pliki) / ile_na_strone)
    
    # Zabezpieczenie: Reset strony, jeśli zmienimy liczbę zdjęć na stronę
    if st.session_state.strona_galerii >= liczba_stron:
        st.session_state.strona_galerii = 0

    start_index = st.session_state.strona_galerii * ile_na_strone
    end_index = start_index + ile_na_strone
    pliki_na_teraz = pliki[start_index:end_index]

    # --- FUNKCJA NAWIGACJI ---
    def pokaz_nawigacje(miejsce):
        """Wyświetla przyciski nawigacji. Argument 'miejsce' to unikalny klucz (np. 'gora', 'dol')."""
        col_prev, col_info, col_next = st.columns([1, 2, 1])
        
        with col_prev:
            if st.session_state.strona_galerii > 0:
                # Klucz (key) musi być unikalny dla każdego przycisku w Streamlit!
                if st.button("⬅️ Poprzednia", key=f"prev_{miejsce}"):
                    st.session_state.strona_galerii -= 1
                    st.rerun()
        
        with col_info:
            st.markdown(f"<div class='page-number'>Strona {st.session_state.strona_galerii + 1} z {liczba_stron}</div>", unsafe_allow_html=True)
        
        with col_next:
            if st.session_state.strona_galerii < liczba_stron - 1:
                if st.button("Następna ➡️", key=f"next_{miejsce}"):
                    st.session_state.strona_galerii += 1
                    st.rerun()

    # 1. NAWIGACJA GÓRNA (Nad zdjęciami)
    pokaz_nawigacje("gora")
    
    st.write("") # Mały odstęp

    # --- WYŚWIETLANIE ZDJĘĆ ---
    cols = st.columns(ile_kolumn)
    
    for index, plik in enumerate(pliki_na_teraz):
        sciezka = os.path.join(folder_zdjec, plik)
        try:
            # Używamy funkcji z cache dla wydajności
            img_square = dopasuj_z_tlem(sciezka)
            
            with cols[index % ile_kolumn]:
                st.image(img_square, use_container_width=True)
                
        except Exception as e:
            st.error(f"Nie udało się wczytać: {plik}")

    st.divider()

    # 2. NAWIGACJA DOLNA (Pod zdjęciami)
    pokaz_nawigacje("dol")