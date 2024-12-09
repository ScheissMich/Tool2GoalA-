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
                "Erfahrungen": ["Beginner", "Intermediate", "Pro"],
            },
            "goals": ["Beitrag schreiben", "Daten analysieren"],
            "tools": [
                {
                    "name": "ChatGPT",
                    "filters": {"Lizenz": ["Kostenlos", "Freemium"], "Erfahrungen": ["Beginner", "Intermediate"]},
                    "goals": ["Beitrag schreiben"],
                    "link": "https://chat.openai.com",
                    "tooltip": "Generiere kreative Texte mit KI.",
                },
                {
                    "name": "RowsAI",
                    "filters": {"Lizenz": ["Kostenlos", "Abonnement"], "Erfahrungen": ["Intermediate"]},
                    "goals": ["Beitrag schreiben", "Daten analysieren"],
                    "link": "https://rows.com",
                    "tooltip": "Automatisiere Datenanalyse.",
                },
            ],
        }

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Load data
data = load_data()

# Ensure "Erfahrungen" exists in filters
if "Erfahrungen" not in data["filters"]:
    data["filters"]["Erfahrungen"] = ["Beginner", "Intermediate", "Pro"]
    save_data(data)  # Save the updated structure

# Streamlit App
st.set_page_config(page_title="Tools-Matrix", layout="wide")
st.title("Dynamische Tools-Matrix")

# Tabs for Matrix and Admin Panel
tab1, tab2 = st.tabs(["Matrix", "Admin"])

# --- Matrix Tab ---
with tab1:
    st.header("Matrix der Tools nach Filtern")

    # Sidebar Filters
    st.write("**Filter auswählen:**")
    selected_license = st.selectbox("Lizenz", ["Alle"] + data["filters"].get("Lizenz", []))
    selected_experience = st.selectbox("Erfahrungen", ["Alle"] + data["filters"].get("Erfahrungen", []))

    # Filter Tools
    filtered_tools = [
        tool for tool in data["tools"]
        if (selected_license == "Alle" or selected_license in tool["filters"].get("Lizenz", []))
        and (selected_experience == "Alle" or selected_experience in tool["filters"].get("Erfahrungen", []))
    ]

    # Prepare Matrix Rows
    matrix = []
    for tool in filtered_tools:
        row = {
            "Tool": f"<a href='{tool['link']}' title='{tool['tooltip']}'>{tool['name']}</a>",
            "Lizenz": ", ".join(tool["filters"].get("Lizenz", [])),
            "Erfahrungen": ", ".join(tool["filters"].get("Erfahrungen", [])),
        }
        for goal in data["goals"]:
            row[goal] = f"<a href='{tool['link']}'>{goal}</a>" if goal in tool["goals"] else "-"
        matrix.append(row)

    # Create DataFrame for Matrix Display
    df_matrix = pd.DataFrame(matrix)
    columns = ["Tool", "Lizenz", "Erfahrungen"] + data["goals"]
    df_matrix = df_matrix[columns]

    # Styling for merged cells
    st.write(
        """<style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid black;
                text-align: center;
                padding: 8px;
            }
            th {
                background-color: #f2f2f2;
            }
            .merged-cell {
                text-align: center;
                font-weight: bold;
                vertical-align: middle;
            }
        </style>""",
        unsafe_allow_html=True,
    )
    st.write(df_matrix.to_html(escape=False, index=False), unsafe_allow_html=True)

# --- Admin Tab ---
with tab2:
    st.header("Admin-Panel")

    # Manage Filters
    st.subheader("Filter verwalten")
    for filter_name, filter_values in data["filters"].items():
        st.write(f"**{filter_name}**: {', '.join(filter_values)}")
        new_filter_value = st.text_input(f"Neuen Wert zu {filter_name} hinzufügen")
        if st.button(f"Hinzufügen zu {filter_name}") and new_filter_value:
            data["filters"][filter_name].append(new_filter_value)
            save_data(data)
            st.success(f"Wert '{new_filter_value}' wurde zu {filter_name} hinzugefügt!")
            st.experimental_rerun()

    # Manage Tools
    st.subheader("Tools verwalten")
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
