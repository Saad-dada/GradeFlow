"""
Sidebar components for GradeFlow application.
"""
import streamlit as st
from config import PASSING_SCORE, MIN_SCORE, MAX_SCORE, ALLOWED_FILE_TYPES


def render_sidebar():
    """Render the complete sidebar with all components"""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Sample data download
        render_sample_data_section()
        
        # Grade scale display
        render_grade_scale_section()
        
        # System info
        render_system_info_section()


def render_sample_data_section():
    """Render sample data download section"""
    from .ui_components import create_sample_data
    
    st.subheader("📥 Sample Data")
    sample_data = create_sample_data()
    
    csv_sample = sample_data.to_csv(index=False)
    st.download_button(
        label="📄 Download Sample CSV",
        data=csv_sample,
        file_name="sample_student_data.csv",
        mime="text/csv"
    )


def render_grade_scale_section():
    """Render grade scale display section"""
    from .ui_components import display_grade_scale
    
    st.subheader("📊 Current Grade Scale")
    grade_df = display_grade_scale()
    st.dataframe(grade_df, hide_index=True)


def render_system_info_section():
    """Render system information section"""
    st.subheader("ℹ️ System Info")
    st.info(f"""
    **Passing Score**: {PASSING_SCORE}%
    **Score Range**: {MIN_SCORE}-{MAX_SCORE}
    **File Types**: {', '.join(ALLOWED_FILE_TYPES)}
    """)
