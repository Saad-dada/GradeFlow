"""
GradeFlow - Professional Student Grade Management & Analytics System
Main application file with modular architecture
"""
import streamlit as st
import pandas as pd
from config import *

# Import modules from organized folder structure
from src.core.validators import DataValidator
from src.core.grade_calculator import GradeCalculator
from src.core.analytics import Analytics
from src.ui.ui_components import apply_custom_css
from src.ui.sidebar import render_sidebar
from src.ui.help_components import display_welcome_section
from src.utils.data_processor import DataProcessor

# Page configuration
st.set_page_config(
    page_title=APP_TITLE, 
    page_icon=APP_ICON, 
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_INITIAL_STATE
)

# Apply custom CSS
apply_custom_css()

def main():
    # Main application header
    st.markdown(f'<h1 class="main-header">{APP_ICON} GradeFlow</h1>', unsafe_allow_html=True)
    st.markdown("**Professional Student Grade Management & Analytics System**")

    # Sidebar configuration
    render_sidebar()

    # File upload section
    render_file_upload_section()


def render_file_upload_section():
    """Render file upload section"""
    st.header("📁 Data Upload")
    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Upload student result file", 
            type=ALLOWED_FILE_TYPES,
            help=f"Supported formats: {', '.join(ALLOWED_FILE_TYPES)}. Required columns: {', '.join(REQUIRED_COLUMNS)}"
        )

    with col2:
        if uploaded_file:
            file_info = {
                "Filename": uploaded_file.name,
                "Size": f"{uploaded_file.size / 1024:.1f} KB",
                "Type": uploaded_file.type
            }
            st.json(file_info)

    if uploaded_file is not None:
        process_uploaded_file(uploaded_file)
    else:
        display_welcome_section()


def process_uploaded_file(uploaded_file):
    """Process uploaded file and display analysis"""
    with st.spinner("Processing file..."):
        try:
            # Read file using DataProcessor
            processor = DataProcessor()
            df = processor.read_uploaded_file(uploaded_file)
            
            st.success("✅ File uploaded successfully!")

            # Validate data
            validator = DataValidator()
            issues = validator.validate_data(df)

            # Display validation results
            display_validation_results(issues)

            # Only proceed with analysis if no critical errors
            if issues['severity'] != 'error':
                perform_data_analysis(df, processor)

        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.info("💡 Please check your file format and try again.")
            
            # Show detailed error in expander for debugging
            with st.expander("🔍 Technical Details"):
                st.exception(e)


def display_validation_results(issues):
    """Display data validation results"""
    st.header("🧹 Data Validation")
    
    if issues['severity'] == 'error':
        st.error("❌ Critical issues found - please fix before proceeding")
    elif issues['severity'] == 'warning':
        st.warning("⚠️ Some issues detected - review recommended")
    else:
        st.success("✅ Data validation passed!")

    # Show all validation summary in a single container for better alignment
    with st.container():
        st.subheader("📋 Validation Summary")
        # Missing columns
        if issues['missing_columns']:
            st.error(f"❌ Missing columns: {', '.join(issues['missing_columns'])}")
        else:
            st.success("✅ All required columns present")
        
        # Missing values
        if issues['missing_values']:
            st.warning("⚠️ Missing values detected:")
            for col, count in issues['missing_values'].items():
                st.write(f"  • {col}: {count} missing")
        else:
            st.success("✅ No missing values")

        # Duplicates
        if issues['duplicates'] > 0:
            st.warning(f"⚠️ {issues['duplicates']} duplicate rows found")
        else:
            st.success("✅ No duplicate rows")
        
        # Invalid data
        if issues['invalid_genders']:
            st.warning(f"⚠️ {len(issues['invalid_genders'])} invalid gender entries")
        
        if issues['invalid_totals']:
            st.warning(f"⚠️ {len(issues['invalid_totals'])} invalid total scores")


def perform_data_analysis(df, processor):
    """Perform complete data analysis and display results"""
    # Add grade column
    if 'Total' in df.columns:
        calculator = GradeCalculator()
        df['Grade'] = calculator.assign_grades(df['Total'])
    
    # Display statistics
    st.header("📊 Statistical Analysis")
    
    if 'Total' in df.columns:
        stats = calculator.calculate_statistics(df)
        
        # Use Analytics class for displaying metrics and charts
        analytics = Analytics()
        analytics.display_key_metrics(stats)
        analytics.display_charts(df)
        analytics.display_gender_analysis(df)
    
    # Data management tools
    render_data_management_section(df, processor, stats)
    
    # Enhanced data preview with filtering
    render_data_preview_section(df)


def render_data_management_section(df, processor, stats):
    """Render data management tools section"""
    st.header("🔧 Data Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧹 Clean Data", help="Remove duplicates and invalid entries"):
            cleaned_df, removed_count = processor.clean_data(df)
            if removed_count > 0:
                st.success(f"✅ Cleaned! Removed {removed_count} problematic rows")
                st.session_state.cleaned_df = cleaned_df
            else:
                st.info("ℹ️ No data needed cleaning!")
    
    with col2:
        # Export functionality
        if 'Total' in df.columns:
            report_data = processor.create_excel_report(df, stats)
            filename = processor.get_report_filename()
            
            st.download_button(
                label="📊 Download Excel Report",
                data=report_data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download comprehensive Excel report with multiple sheets"
            )
    
    with col3:
        if st.button("🔄 Reset Analysis", help="Clear all filters and start fresh"):
            st.rerun()


def render_data_preview_section(df):
    """Render data preview with filtering section"""
    st.header("📋 Data Preview & Filtering")
    
    # Use cleaned data if available
    display_df = st.session_state.get('cleaned_df', df)
    
    # Create filter controls using Analytics class
    analytics = Analytics()
    filters = analytics.create_filter_controls(display_df)
    
    # Apply filters using DataProcessor
    processor = DataProcessor()
    df_filtered = processor.filter_dataframe(
        display_df,
        grade_filter=filters.get('grade_filter'),
        gender_filter=filters.get('gender_filter'),
        score_range=filters.get('score_range')
    )
    
    # Display filtered data with enhanced formatting
    if not df_filtered.empty:
        st.dataframe(
            df_filtered, 
            use_container_width=True, 
            height=DATAFRAME_HEIGHT,
            hide_index=True
        )
        
        # Summary info with color coding
        if len(df_filtered) == len(display_df):
            st.success(f"✅ Showing all {len(df_filtered)} students")
        else:
            st.info(f"📊 Showing {len(df_filtered)} of {len(display_df)} students (filtered)")
    else:
        st.warning("⚠️ No data matches your filter criteria")


if __name__ == "__main__":
    main()
