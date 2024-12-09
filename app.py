import streamlit as st
import pandas as pd
import json

# Set page configuration
st.set_page_config(
    page_title="KI-Tools Matrix",
    layout="wide",
)

# Load data (mock data as JSON for this example)
data = {
    "goals": ["Texte schreiben", "Daten analysieren", "Bilder bearbeiten"],
    "tools": ["ChatGPT", "DataRobot", "DALL-E"],
    "scenarios": {
        ("Texte schreiben", "ChatGPT"): "Nutze ChatGPT, um Blogposts schnell zu erstellen.",
        ("Daten analysieren", "DataRobot"): "Automatisiere deine Datenanalysen mit DataRobot.",
        ("Bilder bearbeiten", "DALL-E"): "Erstelle kreative Bildbearbeitungen mit DALL-E."
    },
    "filters": {
        "Funktionalität": ["Textgenerierung", "Datenanalyse", "Bildbearbeitung"],
        "Kostenmodell": ["Kostenlos", "Freemium", "Abonnement"],
        "Zielgruppe": ["Freelancer", "Teams", "Unternehmen"],
        "Plattform": ["Web-basiert", "Desktop", "Mobile"]
    }
}

# Sidebar filters
st.sidebar.header("Filter")
selected_functionality = st.sidebar.multiselect("Funktionalität", data["filters"]["Funktionalität"])
selected_cost = st.sidebar.multiselect("Kostenmodell", data["filters"]["Kostenmodell"])
selected_audience = st.sidebar.multiselect("Zielgruppe", data["filters"]["Zielgruppe"])
selected_platform = st.sidebar.multiselect("Plattform", data["filters"]["Plattform"])

# Header
st.title("Interaktive Matrix: KI-Tools und Problemstellungen")

# Create matrix structure
st.markdown("### Matrix der Tools und Problemstellungen")
matrix = pd.DataFrame(index=data["goals"], columns=data["tools"])

for goal, tool in data["scenarios"]:
    matrix.loc[goal, tool] = f"**{data['scenarios'][(goal, tool)]}**"

# Render matrix
st.table(matrix.fillna("Keine Szenarien"))

# Clickable details
st.markdown("### Details zu einem Szenario")
clicked_goal = st.selectbox("Wähle ein Ziel", data["goals"])
clicked_tool = st.selectbox("Wähle ein Tool", data["tools"])

if (clicked_goal, clicked_tool) in data["scenarios"]:
    st.subheader(f"Szenario: {clicked_goal} + {clicked_tool}")
    st.write(data["scenarios"][(clicked_goal, clicked_tool)])
    st.write("**Verknüpfte Ressourcen:** [Mehr erfahren](https://example.com)")

# Admin Functions (optional - simulate adding/editing scenarios)
st.sidebar.subheader("Admin-Funktionen")
if st.sidebar.checkbox("Szenarien bearbeiten"):
    new_goal = st.sidebar.text_input("Neues Ziel")
    new_tool = st.sidebar.text_input("Neues Tool")
    new_scenario = st.sidebar.text_area("Neue Beschreibung")
    if st.sidebar.button("Hinzufügen"):
        data["goals"].append(new_goal)
        data["tools"].append(new_tool)
        data["scenarios"][(new_goal, new_tool)] = new_scenario
        st.sidebar.success("Szenario hinzugefügt!")
