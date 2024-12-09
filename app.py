import streamlit as st
import pandas as pd
import json
import os

# File for data storage
DATA_FILE = "matrix_with_inline_filters.json"

# Load and save data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    else:
        return {
            "filters": {
                "Lizenz": ["Kostenlos", "Freemium", "Abonnement"],
                "Zielgruppe": ["Beginner", "Intermediate", "Pro"],
            },
            "goals": ["Blogposts schreiben", "Social-Media-Content erstellen", "Daten analysieren"],
            "tools": [
                {
                    "name": "ChatGPT",
                    "filters": {"Lizenz": ["Kostenlos", "Freemium"], "Zielgruppe": ["Beginner", "Intermediate"]},
                    "goals": ["Blogposts schreiben", "Social-Media-Content erstellen"],
                    "link": "https://chat.openai.com",
                    "tooltip": "Generiere kreative Texte mit KI.",
                },
                {
                    "name": "Canva",
                    "filters": {"Lizenz": ["Kostenlos", "Freemium"], "Zielgruppe": ["Beginner"]},
                    "goals": ["Social-Media-Content erstellen"],
                    "link": "https://www.canva.com",
                    "tooltip": "Erstelle einfache Designs für Social Media.",
                },
                {
                    "name": "Google Sheets",
                    "filters": {"Lizenz": ["Kostenlos"], "Zielgruppe": ["Beginner", "Intermediate"]},
                    "goals": ["Daten analysieren"],
                    "link": "https://sheets.google.com",
                    "tooltip": "Kostenlose Tabellenkalkulation für Datenanalyse.",
                },
            ],
        }

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Load data
data = load_data()

# Streamlit App
st.set_page_config(page_title="Tools-Matrix", layout="wide")
st.title("Tools-Matrix mit Filtern und Zielen")

# Prepare Matrix Rows
matrix = []
for category, attributes in data["filters"].items():
    for attribute in attributes:
        row = [f"{category}: {attribute}"]
        for goal in data["goals"]:
            tools = [
                f"<a href='{tool['link']}' title='{tool['tooltip']}'>{tool['name']}</a>"
                for tool in data["tools"]
                if attribute in tool["filters"].get(category, []) and goal in tool["goals"]
            ]
            row.append(", ".join(tools) if tools else "-")
        matrix.append(row)

# Create DataFrame for Matrix Display
df_matrix = pd.DataFrame(matrix, columns=["Filter"] + data["goals"])

# Styling to match the uploaded table
st.write(
    """<style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            text-align: left;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>""",
    unsafe_allow_html=True,
)
st.write(df_matrix.to_html(escape=False, index=False), unsafe_allow_html=True)

# Tool Management Section
st.header("Tools verwalten")
with st.expander("Neues Tool hinzufügen"):
    new_tool_name = st.text_input("Tool-Name")
    new_tool_link = st.text_input("Tool-Link (URL)")
    new_tool_tooltip = st.text_input("Kurzbeschreibung")
    new_tool_filters = {category: st.multiselect(f"{category}-Filter", attributes) for category, attributes in data["filters"].items()}
    new_tool_goals = st.multiselect("Ziele", data["goals"])
    if st.button("Tool hinzufügen"):
        if new_tool_name:
            data["tools"].append({
                "name": new_tool_name,
                "filters": new_tool_filters,
                "goals": new_tool_goals,
                "link": new_tool_link,
                "tooltip": new_tool_tooltip,
            })
            save_data(data)
            st.success(f"Neues Tool '{new_tool_name}' wurde hinzugefügt!")
            st.experimental_rerun()

st.write("**Existierende Tools:**")
for tool in data["tools"]:
    with st.expander(f"{tool['name']}"):
        tool["link"] = st.text_input(f"Link ({tool['name']})", value=tool["link"])
        tool["tooltip"] = st.text_input(f"Kurzbeschreibung ({tool['name']})", value=tool["tooltip"])
        tool["filters"] = {category: st.multiselect(f"{category}-Filter ({tool['name']})", attributes, default=tool["filters"].get(category, [])) for category, attributes in data["filters"].items()}
        tool["goals"] = st.multiselect(f"Ziele ({tool['name']})", data["goals"], default=tool["goals"])
        if st.button(f"Speichern ({tool['name']})"):
            save_data(data)
            st.success(f"{tool['name']} wurde aktualisiert!")
        if st.button(f"Löschen ({tool['name']})"):
            data["tools"].remove(tool)
            save_data(data)
            st.warning(f"{tool['name']} wurde gelöscht!")
            st.experimental_rerun()
