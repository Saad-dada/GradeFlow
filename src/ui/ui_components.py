"""
UI components and styling for GradeFlow application.
"""
import streamlit as st
import pandas as pd
from config import GRADE_SCALE


def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            color: #1e3a8a;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 0.25rem;
            padding: 0.75rem;
            margin: 0.5rem 0;
        }
        /* Fix metric text visibility */
        .stMetric {
            background-color: #f8f9fa !important;
            border: 1px solid #dee2e6 !important;
            padding: 1rem !important;
            border-radius: 0.375rem !important;
            text-align: center !important;
        }
        .stMetric > div {
            color: #212529 !important;
        }
        .stMetric label {
            color: #495057 !important;
            font-weight: 600 !important;
        }
        .stMetric [data-testid="metric-value"] {
            color: #212529 !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
        }
        .stMetric [data-testid="metric-delta"] {
            color: #6c757d !important;
            font-size: 0.9rem !important;
        }
        /* Ensure all text in metrics is visible */
        [data-testid="metric-container"] {
            background-color: #ffffff !important;
            border: 1px solid #e9ecef !important;
            border-radius: 0.5rem !important;
            padding: 1rem !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        }
        [data-testid="metric-container"] * {
            color: #212529 !important;
        }
    </style>
    """, unsafe_allow_html=True)


def display_metric_card(title, value, delta=None, help_text=""):
    """Custom metric display with better visibility"""
    delta_color = "gray"
    if delta:
        try:
            # Extract numeric value from delta string, handling percentages
            delta_text = delta.split()[0]
            if delta_text.endswith('%'):
                delta_value = float(delta_text[:-1])
            else:
                delta_value = float(delta_text)
            
            delta_color = "green" if delta_value > 0 else "red" if delta_value < 0 else "gray"
        except (ValueError, IndexError):
            delta_color = "gray"
    
    delta_html = f'<p style="color: {delta_color}; font-size: 0.8rem; margin: 0;">{delta}</p>' if delta else ""
    
    st.markdown(f"""
    <div style="
        background-color: #ffffff;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    ">
        <h4 style="color: #495057; margin: 0; font-size: 0.9rem;">{title}</h4>
        <h2 style="color: #212529; margin: 0.5rem 0; font-weight: bold;">{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)
    
    if help_text:
        st.caption(help_text)


def display_grade_scale():
    """Display the current grade scale"""
    grade_df = pd.DataFrame([
        {'Grade': grade, 'Range': f"{range_val[0]}-{range_val[1]}"} 
        for grade, range_val in GRADE_SCALE.items()
    ])
    return grade_df


def create_sample_data():
    """Create sample data for download"""
    sample_data = pd.DataFrame({
        'Roll No': ['2021001', '2021002', '2021003', '2021004', '2021005', '2021006', '2021007', '2021008'],
        'Name': ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Eva Brown', 'Frank Miller', 'Grace Lee', 'Henry Clark'],
        'Gender': ['Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male'],
        'Total': [85, 92, 78, 67, 94, 32, 28, 35]
    })
    # Randomize the order of students
    sample_data = sample_data.sample(frac=1).reset_index(drop=True)
    return sample_data
