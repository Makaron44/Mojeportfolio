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
        /* Styl przycisków (wszystkich, w tym Powiększ) */
        .stButton button {
            width: 100%;
            border-radius: 10px;
            border: 1px solid #444;
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
    """Wczytuje zdjęcie, konwertuje do RGB i dodaje tło, aby było kwadratowe (do miniaturki)."""
    image = Image.open(image_path)
    
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    
    width, height = image.size
    nowy_wymiar = max(width, height)
    nowe_zdjecie = Image.new("RGB", (nowy_wymiar, nowy_wymiar), kolor_tla)
    pozycja_x = (nowy_wymiar - width) // 2
    pozycja_y = (nowy_wymiar - height) // 2
    nowe_zdjecie.paste(image, (pozycja_x, pozycja_y))
    return nowe_zdjecie

# --- NOWOŚĆ: OKNO DIALOGOWE (LIGHTBOX) ---
@st.dialog("Podgląd pracy")
def pokaz_duze_zdjecie(sciezka_do_pliku, nazwa_pliku):
    """Wyświetla duże zdjęcie w oknie modalnym z opcją pobrania."""
    try:
        # Wczytujemy oryginał bez tła
        img = Image.open(sciezka_do_pliku)
        st.image(img, use_container_width=True)
        
        # Dodajemy przycisk pobierania pod dużym zdjęciem
        with open(sciezka_do_pliku, "rb") as file:
            st.download_button(
                label="📥 Pobierz grafikę",
                data=file,
                file_name=nazwa_pliku,
                mime="image/webp"
            )
    except Exception as e:
        st.error(f"Nie udało się wczytać oryginału: {e}")

# --- INICJALIZACJA SESJI ---
if 'strona_galerii' not in st.session_state:
    st.session_state.strona_galerii = 0

# --- POBIERANIE PLIKÓW ---
folder_zdjec = "images"

if not os.path.exists(folder_zdjec):
    os.makedirs(folder_zdjec)

rozszerzenia = ('.webp', '.png', '.jpg', '.jpeg', '.JPG', '.PNG', '.WEBP')
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
    Kliknij **Powiększ**, aby zobaczyć detale.
    """)

st.divider()

# --- LOGIKA GALERII ---
if not pliki:
    st.warning(f"Folder '{folder_zdjec}' jest pusty lub nie istnieje. Dodaj zdjęcia .webp na GitHub!")
else:
    liczba_stron = math.ceil(len(pliki) / ile_na_strone)
    
    if st.session_state.strona_galerii >= liczba_stron:
        st.session_state.strona_galerii = 0

    start_index = st.session_state.strona_galerii * ile_na_strone
    end_index = start_index + ile_na_strone
    pliki_na_teraz = pliki[start_index:end_index]

    # --- FUNKCJA NAWIGACJI ---
    def pokaz_nawigacje(miejsce):
        col_prev, col_info, col_next = st.columns([1, 2, 1])
        
        with col_prev:
            if st.session_state.strona_galerii > 0:
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

    # 1. NAWIGACJA GÓRNA
    pokaz_nawigacje("gora")
    
    st.write("")

    # --- WYŚWIETLANIE ZDJĘĆ Z PRZYCISKIEM ---
    cols = st.columns(ile_kolumn)
    
    for index, plik in enumerate(pliki_na_teraz):
        sciezka = os.path.join(folder_zdjec, plik)
        try:
            # Tworzymy kwadratową miniaturkę do siatki
            img_square = dopasuj_z_tlem(sciezka)
            
            with cols[index % ile_kolumn]:
                # Wyświetlamy miniaturkę
                st.image(img_square, use_container_width=True)
                
                # PRZYCISK: Otwiera okno dialogowe
                # Unikalny klucz zapobiega błędom Streamlit
                if st.button("🔍 Powiększ", key=f"zoom_{index}_{plik}"):
                    pokaz_duze_zdjecie(sciezka, plik)
                
        except Exception as e:
            st.error(f"Nie udało się wczytać: {plik}")

    st.divider()

    # 2. NAWIGACJA DOLNA
    pokaz_nawigacje("dol")
