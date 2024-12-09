import streamlit as st
import pandas as pd  # Korrekt importiert!
import json
import os

# File for data storage
DATA_FILE = "tools_with_dynamic_filters.json"

# Load and save data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    else:
        return {
            "goals": ["Blogposts schreiben", "Social-Media-Content erstellen", "Daten analysieren"],
            "licenses": ["Kostenlos", "Freemium", "Abonnement", "Einmalige Zahlung"],
            "tools": [
                {"name": "ChatGPT", "licenses": ["Kostenlos", "Freemium"], "goals": ["Blogposts schreiben"], "description": "Generiere Blog-Ideen."},
                {"name": "Canva", "licenses": ["Freemium", "Abonnement"], "goals": ["Social-Media-Content erstellen"], "description": "Erstelle Social-Media-Designs."},
                {"name": "Power BI", "licenses": ["Abonnement"], "goals": ["Daten analysieren"], "description": "Analysiere Daten visuell."},
            ],
        }

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Load data
data = load_data()

# Streamlit App
st.set_page_config(page_title="Dynamische Matrix", layout="wide")
st.title("Dynamische Matrix: Tools nach Lizenz filtern")

# License filters
st.sidebar.header("Lizenzen auswählen")
selected_licenses = st.sidebar.multiselect("Wähle Lizenzen aus", data["licenses"], default=data["licenses"])

# Filtered tools
filtered_tools = [
    tool for tool in data["tools"] if any(license_ in selected_licenses for license_ in tool["licenses"])
]

# Display the matrix
st.header("Matrix der Tools nach Anwendungsfällen")
matrix_data = [
    [
        ", ".join([
            f"{tool['name']}: {tool['description']}"
            for tool in filtered_tools
            if goal in tool["goals"]
        ]) or "Keine Tools"
        for goal in data["goals"]
    ]
]
df_matrix = pd.DataFrame(matrix_data, index=["Tools"], columns=data["goals"])
st.table(df_matrix)

# Tool Management
st.header("Tools verwalten")
with st.expander("Neues Tool hinzufügen"):
    new_tool_name = st.text_input("Tool-Name")
    new_tool_description = st.text_area("Beschreibung")
    new_tool_licenses = st.multiselect("Lizenzen", data["licenses"])
    new_tool_goals = st.multiselect("Anwendungsfälle", data["goals"])
    if st.button("Tool hinzufügen"):
        if new_tool_name:
            data["tools"].append({
                "name": new_tool_name,
                "description": new_tool_description,
                "licenses": new_tool_licenses,
                "goals": new_tool_goals,
            })
            save_data(data)
            st.success(f"Neues Tool '{new_tool_name}' hinzugefügt!")
            st.experimental_rerun()

st.write("**Existierende Tools:**")
for tool in data["tools"]:
    with st.expander(f"{tool['name']}"):
        tool["description"] = st.text_area(f"Beschreibung ({tool['name']})", value=tool["description"])
        tool["licenses"] = st.multiselect(f"Lizenzen ({tool['name']})", data["licenses"], default=tool["licenses"])
        tool["goals"] = st.multiselect(f"Anwendungsfälle ({tool['name']})", data["goals"], default=tool["goals"])
        if st.button(f"Speichern ({tool['name']})"):
            save_data(data)
            st.success(f"{tool['name']} wurde aktualisiert!")
        if st.button(f"Löschen ({tool['name']})"):
            data["tools"].remove(tool)
            save_data(data)
            st.warning(f"{tool['name']} wurde gelöscht!")
            st.experimental_rerun()
