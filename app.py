
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Crime Dashboard", layout="wide")

st.title("🚔 India Crime Data Analysis Dashboard")

BASE_PATH = ""

datasets = {
    "Property Stolen": "data/10_Property_stolen_and_recovered.csv",
    "Rape Victims": "data/20_Victims_of_rape.csv",
    "Police Complaints": "data/25_Complaints_against_police.csv",
    "Trial of Violent Crimes": "data/28_Trial_of_violent_crimes_by_courts.csv",
    "Trial Period": "data/29_Period_of_trials_by_courts.csv",
    "Auto Theft": "data/30_Auto_theft.csv",
    "Serious Fraud": "data/31_Serious_fraud.csv",
    "Murder Victims": "data/32_Murder_victim_age_sex.csv",
    "Attempt to Murder": "data/33_CH_not_murder_victim_age_sex.csv",
    "Human Rights Violation": "data/35_Human_rights_violation_by_police.csv",
    "Police Housing": "data/36_Police_housing.csv",
    "Kidnapping Purpose": "data/39_Specific_purpose_of_kidnapping_and_abduction.csv",
    "Custodial Death (Remanded)": "data/40_01_Custodial_death_person_remanded.csv",
    "Custodial Death (Not Remanded)": "data/40_02_Custodial_death_person_not_remanded.csv",
    "Custodial Death (Production)": "data/40_03_Custodial_death_during_production.csv",
    "Custodial Death (Hospital)": "data/40_04_Custodial_death_during_hospitalization_or_treatment.csv",
    "Custodial Death (Others)": "data/40_05_Custodial_death_others.csv",
    "Crime Against Women": "data/42_Cases_under_crime_against_women.csv",
    "Arrests (Women Crime)": "data/43_Arrests_under_crime_against_women.csv"
}

# SELECT DATASET
option = st.selectbox("Select Dataset", list(datasets.keys()))

# LOAD FUNCTION
def load_data(file):
    try:
        df = pd.read_csv(file, encoding='utf-8-sig', on_bad_lines='skip')

        # 🔥 YAHI INSERT KARNA THA
        df.columns = df.columns.str.replace('ï»¿', '')
        df.columns = df.columns.str.strip()

        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

df = load_data(datasets[option])

# SHOW DATA
if df is not None:

    st.subheader("📊 Dataset Preview")
    st.write(df.head())

    st.subheader("📌 Columns")
    st.write(list(df.columns))

    # COLUMN SELECT
st.subheader("📈 Visualization")

if df is not None:

    if 'Year' in df.columns:

        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df = df.dropna(subset=['Year'])

        numeric_cols = df.select_dtypes(include='number').columns

        if len(numeric_cols) > 0:
            col = st.selectbox("Select Numeric Column", numeric_cols)

            plt.figure(figsize=(8,4))
            sns.lineplot(x=df['Year'], y=df[col])
            plt.title(f"{col} over Years")

            st.pyplot(plt)

        else:
            st.warning("No numeric columns available")

    else:
        col = st.selectbox("Select Column", df.columns)

        if df[col].dtype == 'object':
            st.bar_chart(df[col].value_counts())
        else:
            st.line_chart(df[col])

else:
    st.error("Dataset not loaded")
  
st.subheader("📊 State vs Total Crime (Bar Graph)")

if df is not None and 'Area_Name' in df.columns:

    numeric_cols = df.select_dtypes(include='number').columns

    state_data = df.groupby('Area_Name')[numeric_cols].sum()
    state_data['Total_Crime'] = state_data.sum(axis=1)

    top_states = state_data.sort_values('Total_Crime', ascending=False).head(10)

    plt.figure(figsize=(10,5))
    top_states['Total_Crime'].plot(kind='bar')

    plt.xticks(rotation=45)
    st.pyplot(plt)

else:
    st.warning("Area_Name column not found or data not loaded")


st.subheader("📊 State vs Selected Crime Type")

if df is not None and 'Area_Name' in df.columns:

    numeric_cols = df.select_dtypes(include='number').columns

    crime_col = st.selectbox("Select Crime Type", numeric_cols)

    state_data = df.groupby('Area_Name')[crime_col].sum().sort_values(ascending=False).head(10)

    plt.figure(figsize=(10,5))
    state_data.plot(kind='bar')

    plt.title(f"Top States for {crime_col}")
    plt.xticks(rotation=45)

    st.pyplot(plt)

else:
    st.warning("Area_Name column not found or data not loaded")
# 🔥 HEATMAP (ALWAYS SHOW)
st.subheader("🔥 Correlation Heatmap")

if df is not None:
    try:
        corr = df.corr(numeric_only=True)

        fig, ax = plt.subplots(figsize=(8,5))
        sns.heatmap(corr, annot=True, ax=ax)

        st.pyplot(fig)

    except:
        st.warning("Heatmap not possible")
else:
    st.warning("No data available for heatmap")
