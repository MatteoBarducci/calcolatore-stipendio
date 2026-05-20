import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configurazione della pagina per il telefono
st.set_page_config(page_title="Calcolatore Netto", page_icon="💸")
st.title("Calcolatore Stipendio 💸")

# Recupera la chiave API in modo sicuro
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Chiave API mancante. Configura i secrets su Streamlit.")

# Le istruzioni fisse per il modello
prompt = """
Sei un esperto contabile. Analizza questa foto della timesheet o del roster.
Calcola lo stipendio netto seguendo rigidamente queste regole:
- Sheraton (M04 HIGA Level 3 Casual): Base $26.70. Feriale $33.375, Sab $40.05, Dom $46.725.
- Peninsula (Level 2 Adult Casual): Base $25.85. Feriale $32.3125, Sab $38.775, Dom $45.2375. Aggiungi Overnight shift ($4.22/h) se il turno è prima delle 7:00 AM.
- Sottrai 0.5h di pausa non pagata per OGNI singolo turno giornaliero che supera le 6 ore.
- Overtime: Oltre le 76 ore nel fortnight, scatta l'overtime sulle ore finali.
Fornisci il dettaglio ore diviso per fasce, il lordo totale, e infine mostra in grassetto due calcoli del netto finale: uno con tassazione al 15% e uno al 30%. Non usare formule matematiche complesse nel testo, dai solo i risultati puliti.
"""

uploaded_file = st.file_uploader("Carica la foto della Timesheet o del Roster", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Immagine caricata", use_column_width=True)

    if st.button("Calcola Stipendio", use_container_width=True):
        with st.spinner("Analisi dei turni in corso..."):
            try:
                # Usa il modello visivo
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([prompt, image])
                st.success("Calcolo completato!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Errore durante il calcolo: {e}")
              
