import pandas as pd
import streamlit as st

# Constants
DATA_FILE = "gym_exercise_dataset.csv"

# Load and preprocess data
@st.cache_data
def load_and_preprocess_data(file_path):
    """Load and clean the exercise dataset."""
    # Load dataset
    data = pd.read_csv(file_path)
    
    # Clean column names
    data.columns = data.columns.str.strip()  # Remove trailing spaces
    
    # Dynamically rename 'Difficulty' column
    for col in data.columns:
        if 'Difficulty' in col:
            data.rename(columns={col: 'Difficulty'}, inplace=True)
            break
    
    return data

# Recommend exercises based on user inputs
def get_exercise_recommendations(data, main_muscle, equipment):
    """Filter exercises based on main muscle and equipment."""
    filtered_data = data[
        (data['Main_muscle'].str.contains(main_muscle, na=False)) &
        (data['Equipment'].str.contains(equipment, na=False))
    ]
    return filtered_data[['Exercise Name', 'Equipment', 'Main_muscle', 'Difficulty', 'Preparation', 'Execution']].drop_duplicates()

# Main App Function
def main():
    """Streamlit app for recommending exercises."""
    st.title("🏋️ AI-Powered Exercise Recommender")

    # Load Data
    exercise_data = load_and_preprocess_data(DATA_FILE)

    # User Inputs
    st.sidebar.header("Customize Your Workout")
    main_muscle = st.sidebar.selectbox("🎯 Select Main Muscle Group", 
                                      exercise_data['Main_muscle'].dropna().unique())
    equipment = st.sidebar.selectbox("🛠️ Select Equipment", 
                                     exercise_data['Equipment'].dropna().unique())

    # Show Recommendations
    if st.sidebar.button("💡 Get Exercises"):
        recommendations = get_exercise_recommendations(exercise_data, main_muscle, equipment)
        if not recommendations.empty:
            st.subheader("✅ Recommended Exercises:")
            for _, row in recommendations.iterrows():
                st.write(f"**Exercise Name:** {row['Exercise Name']}")
                st.write(f"**Equipment:** {row['Equipment']}")
                st.write(f"**Main Muscle:** {row['Main_muscle']}")
                st.write(f"**Difficulty:** {row['Difficulty']}")
                st.markdown("**Preparation:**")
                st.text(row['Preparation'])
                st.markdown("**Execution:**")
                st.text(row['Execution'])
                st.markdown("---")  # Separator for readability
        else:
            st.warning("⚠️ No exercises found. Try adjusting your inputs!")

# Run the app
if __name__ == "__main__":
    main()
