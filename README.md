# 🎨 Moje Portfolio AI

Witaj w moim cyfrowym portfolio! Ten projekt to galeria obrazów wygenerowanych przy użyciu sztucznej inteligencji (**Gemini**, **Midjourney**), przedstawiająca eksperymenty z moją podobizną, stylem i kompozycją.

Aplikacja została napisana w języku **Python** i wykorzystuje bibliotekę **Streamlit** do dynamicznego wyświetlania prac.

## 🚀 Jak to działa?

To nie jest zwykła galeria statyczna. Projekt wykorzystuje **automatyzację w Pythonie**:

1.  **Format WebP:** Wszystkie grafiki są automatycznie konwertowane z ciężkich plików PNG/JPG na ultralekki format `.webp` (redukcja rozmiaru o ~95% bez utraty jakości).
2.  **Responsywność:** Galeria automatycznie dopasowuje układ kolumn do urządzenia (komputer/telefon).
3.  **Lazy Loading & Cache:** Aplikacja wykorzystuje cache Streamlit, aby zdjęcia ładowały się błyskawicznie.

## 🛠️ Użyte technologie

* **Python 3.x** - logika aplikacji i skrypty optymalizacyjne.
* **Streamlit** - silnik frontendowy.
* **Pillow (PIL)** - przetwarzanie obrazu (zmiana rozmiaru, konwersja, kadrowanie).
* **Git & GitHub** - kontrola wersji i hosting.

## 📂 Struktura projektu

* `app.py` - Główny kod aplikacji (interfejs, nawigacja).
* `optymalizuj.py` - Mój autorski skrypt do masowej kompresji zdjęć.
* `images/` - Folder z gotowymi, zoptymalizowanymi pracami.

---
*Autor: Maciej Ratajczak*
