import os
import sqlite3
import json
from datetime import datetime
import streamlit as st
import pandas as pd
from pydantic import BaseModel, Field
from openai import OpenAI

# ==========================================
# 1. INITIALIZE MOCK MESSY DATA (The ERP)
# ==========================================
def setup_mock_db():
    conn = sqlite3.connect("client_legacy_erp.db")
    cursor = conn.cursor()
    
    # Create a messy industrial asset table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TXT_MCH_DATA (
            SYS_PK INTEGER PRIMARY KEY AUTOINCREMENT,
            TXT_ASST_ID TEXT,
            MCH_DESC_VAL TEXT,
            LOC_CD_01 TEXT,
            NUM_VAL_TMP REAL,
            DT_TM_UTC TEXT
        )
    """)
    
    # Insert a sample row if empty
    cursor.execute("SELECT COUNT(*) FROM TXT_MCH_DATA")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO TXT_MCH_DATA (TXT_ASST_ID, MCH_DESC_VAL, LOC_CD_01, NUM_VAL_TMP, DT_TM_UTC)
            VALUES ('ASST-9902', 'Turbine Bearing 2', 'PLANT-TX-04', 88.4, '2026-06-16T10:00:00Z')
        """)
        conn.commit()
    conn.close()

# ==========================================
# 2. DEFINING THE AI OUTPUT SCHEMA (Pydantic)
# ==========================================
class ColumnMapping(BaseModel):
    source_column: str
    canonical_field: str = Field(description="Must be one of: asset_id, asset_name, location_code, sensor_reading, timestamp_utc. Use 'unmapped' if no match.")
    confidence: float = Field(description="Score between 0.0 and 1.0 based on matching accuracy.")
    reasoning: str = Field(description="A concise reason for this mapping decision.")
    transform_sql: str = Field(description="The SQL select conversion expression needed.")

class TableSchemaMapping(BaseModel):
    table_name: str
    mappings: list[ColumnMapping]

# ==========================================
# 3. AGENT BUSINESS LOGIC
# ==========================================
def inspect_legacy_table(table_name: str) -> list[dict]:
    """Reads database structure and compiles column profiles."""
    conn = sqlite3.connect("client_legacy_erp.db")
    cursor = conn.cursor()
    
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    profiles = []
    for col in columns:
        col_name = col[1]
        col_type = col[2]
        
        # Pull real sample data points safely
        cursor.execute(f"SELECT {col_name} FROM {table_name} WHERE {col_name} IS NOT NULL LIMIT 3")
        samples = [str(r[0]) for r in cursor.fetchall()]
        
        profiles.append({
            "name": col_name,
            "type": col_type,
            "samples": samples
        })
    conn.close()
    return profiles

from google import genai
from google.genai import types

def run_ai_semantic_mapper(table_name: str, profiles: list[dict], api_key: str) -> TableSchemaMapping:
    """Uses Gemini structured output to process the entire table layout concurrently."""
    # Initialize the correct Gemini client with your key
    client = genai.Client(api_key=api_key)
    
    ontology = ["asset_id", "asset_name", "location_code", "sensor_reading", "timestamp_utc"]
    
    prompt = f"""
    You are an AI data bridge engineer. Map this legacy table layout to Tiramai's standard system data fields.
    
    Target Schema Options: {ontology}
    Source Table Name: {table_name}
    Columns to Analyze:
    {json.dumps(profiles, indent=2)}
    """
    
    # Using Gemini's native structured outputs feature with your Pydantic model
    response = client.models.generate_content(
        model='gemini-2.5-flash',  # Ultra-fast and accurate for data tasks
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="You output strict structured table mappings based on raw metadata profiles.",
            response_mime_type="application/json",
            response_schema=TableSchemaMapping,
        ),
    )
    
    # Parse the text response back into your Pydantic object structure
    return TableSchemaMapping.model_validate_json(response.text)
    
    return response.choices[0].message.parsed

# ==========================================
# 4. THE STREAMLIT PRESENTATION LAYER
# ==========================================
st.set_page_config(layout="wide", page_title="Tiramai Schema Bridge Bridge POC")
setup_mock_db()

st.title("Self-Healing Schema Bridge")
st.subheader("Autonomous Integration Adapter Engine")
st.write("---")

# Sidebar configurations
with st.sidebar:
    st.header("Engine Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    target_table = st.selectbox("Detected Legacy Client Tables", ["TXT_MCH_DATA"])

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Client Data Environment")
    if st.checkbox("Show Raw Client Database Layout"):
        conn = sqlite3.connect("client_legacy_erp.db")
        df = pd.read_sql_query(f"SELECT * FROM {target_table}", conn)
        conn.close()
        st.dataframe(df)
        
    st.markdown("#### Structural Discovery Profiles")
    discovered_profiles = inspect_legacy_table(target_table)
    st.json(discovered_profiles)

with col2:
    st.markdown("### Tiramai Adapter Automation Loop")
    
    if st.button(" Process & Generate Connectors"):
        if not api_key:
            st.error("Please add your OpenAI API Key in the left pane to initialize mapping analysis.")
        else:
            with st.spinner("Agent discovering schema definitions and calculating transformations..."):
                # Run the Agentic pipeline steps
                mapping_results = run_ai_semantic_mapper(target_table, discovered_profiles, api_key)
                
                st.success("Mapping Loop Complete! Generation Successful.")
                
                # Present confidence assessments clearly to the user
                st.markdown("#### Mapping Classifications")
                results_table = []
                for m in mapping_results.mappings:
                    results_table.append({
                        "Source Code Column": m.source_column,
                        "Target Object Match": m.canonical_field,
                        "Confidence Rating": f"{m.confidence * 100:.1f}%",
                        "AI Evaluation Context": m.reasoning
                    })
                st.table(results_table)
                
                # Generate Code Blocks dynamically based on structural evaluations
                st.markdown("#### 🛠 Generated Unified Architecture Views")
                
                sql_selects = [f"    {m.transform_sql} AS {m.canonical_field}" for m in mapping_results.mappings if m.canonical_field != "unmapped"]
                generated_sql = f"CREATE OR REPLACE VIEW tiramai_standardized_{target_table} AS \nSELECT\n" + ",\n".join(sql_selects) + f"\nFROM {target_table};"
                
                tab1, tab2 = st.tabs(["Production SQL Adapter View", "Python Type-Safe Bridge Classes"])
                with tab1:
                    st.code(generated_sql, language="sql")
                with tab2:
                    python_dataclass = f"@dataclass\nclass Standardized{target_table}:\n"
                    for m in mapping_results.mappings:
                        if m.canonical_field != "unmapped":
                            python_dataclass += f"    {m.canonical_field}: str  # Maps directly to source element -> {m.source_column}\n"
                    st.code(python_dataclass, language="python")