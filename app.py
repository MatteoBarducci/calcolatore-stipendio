import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configurazione della pagina
st.set_page_config(page_title="Calcolatore Netto", page_icon="💸")
st.title("Calcolatore Stipendio 💸")

# Recupero della chiave API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Chiave API mancante. Configura i secrets su Streamlit.")

# Istruzioni fisse
prompt = """
Sei un esperto contabile. Analizza queste foto della timesheet o del roster.
Calcola lo stipendio netto seguendo rigidamente queste regole:
- Sheraton (M04 HIGA Level 3 Casual): Base $26.70. Feriale $33.375, Sab $40.05, Dom $46.725.
- Peninsula (Level 2 Adult Casual): Base $25.85. Feriale $32.3125, Sab $38.775, Dom $45.2375. Aggiungi Overnight shift ($4.22/h) se il turno è prima delle 7:00 AM.
- Sottrai 0.5h di pausa non pagata per OGNI singolo turno giornaliero che supera le 6 ore.
- Overtime: Oltre le 76 ore nel fortnight, scatta l'overtime sulle ore finali.
Fornisci il dettaglio ore diviso per fasce, il lordo totale, e infine mostra in grassetto due calcoli del netto finale: uno con tassazione al 15% e uno al 30%. Non usare formule matematiche complesse nel testo, dai solo i risultati puliti.
"""

# Caricatore multiplo di immagini
uploaded_files = st.file_uploader("Carica le foto delle Timesheet o del Roster", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    images = []
    # Mostra le anteprime di tutte le immagini caricate
    for uploaded_file in uploaded_files:
        img = Image.open(uploaded_file)
        st.image(img, caption=uploaded_file.name, use_column_width=True)
        images.append(img)

    if st.button("Calcola Stipendio", use_container_width=True):
        with st.spinner("Analisi dei turni in corso..."):
            try:
                # Modello aggiornato a Pro per evitare l'errore 404 e migliorare la lettura
                model = genai.GenerativeModel('gemini-1.5-pro-latest')
                # Unisce il prompt testuale a tutte le immagini caricate
                contenuto_da_inviare = [prompt] + images
                
                response = model.generate_content(contenuto_da_inviare)
                st.success("Calcolo completato!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Errore durante il calcolo: {e}")
              
