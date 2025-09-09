"""
Help and documentation components for GradeFlow application.
"""
import streamlit as st
from config import VALID_GENDERS, MIN_SCORE, MAX_SCORE


def display_welcome_section():
    """Display welcome section when no file is uploaded"""
    st.info("👆 Please upload a CSV or Excel file to get started")
    
    # Instructions and help
    col1, col2 = st.columns(2)
    
    with col1:
        display_usage_instructions()
    
    with col2:
        display_setup_instructions()


def display_usage_instructions():
    """Display how to use GradeFlow instructions"""
    with st.expander("📖 How to use GradeFlow"):
        st.markdown(f"""
        ### Required File Format:
        Your file must contain these columns:
        - **Roll No**: Student roll number/ID
        - **Name**: Student full name  
        - **Gender**: {', '.join(VALID_GENDERS)}
        - **Total**: Total score ({MIN_SCORE}-{MAX_SCORE})
        
        ### Features:
        - ✅ Automatic data validation
        - 📊 Statistical analysis and visualizations
        - 🎯 Grade assignment (A+ to F)
        - 🧹 Data cleaning tools
        - 📥 Excel export with multiple sheets
        - 👥 Performance analytics by gender
        - 🔍 Advanced filtering options
        
        ### Tips:
        - Download sample data to see the correct format
        - Ensure scores are between {MIN_SCORE}-{MAX_SCORE}
        - Remove any header rows or formatting before upload
        - Use consistent gender values
        """)


def display_setup_instructions():
    """Display setup and installation instructions"""
    with st.expander("🚀 Setup Instructions"):
        st.markdown("""
        ### Installation:
        ```bash
        pip install -r requirements.txt
        ```
        
        ### Required packages:
        - streamlit
        - pandas  
        - numpy
        - openpyxl
        
        ### Run the application:
        ```bash
        streamlit run app.py
        ```
        
        ### Configuration:
        Edit `config.py` to customize:
        - Grade scales
        - Required columns
        - Validation rules
        - Display settings
        """)
