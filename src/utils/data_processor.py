"""
Data processing utilities for GradeFlow application.
"""
import pandas as pd
import io
from datetime import datetime
from config import MIN_SCORE, MAX_SCORE, EXCEL_ENGINE, EXPORT_DATE_FORMAT


class DataProcessor:
    @staticmethod
    def read_uploaded_file(uploaded_file):
        """Read uploaded CSV or Excel file"""
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        else:
            return pd.read_excel(uploaded_file)
    
    @staticmethod
    def clean_data(df):
        """Clean data by removing duplicates and invalid entries"""
        original_count = len(df)
        
        # Remove duplicates
        cleaned_df = df.drop_duplicates()
        
        # Remove rows with invalid scores
        if 'Total' in cleaned_df.columns:
            cleaned_df = cleaned_df[
                (cleaned_df['Total'] >= MIN_SCORE) & 
                (cleaned_df['Total'] <= MAX_SCORE) & 
                cleaned_df['Total'].notna()
            ]
        
        removed_count = original_count - len(cleaned_df)
        return cleaned_df, removed_count
    
    @staticmethod
    def create_excel_report(df, stats):
        """Create comprehensive Excel report with multiple sheets"""
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine=EXCEL_ENGINE) as writer:
            # Main results sheet
            df.to_excel(writer, sheet_name='Student_Results', index=False)
            
            # Statistics sheet
            stats_df = pd.DataFrame([stats])
            stats_df.to_excel(writer, sheet_name='Statistics', index=False)
            
            # Grade distribution sheet
            if 'Grade' in df.columns:
                grade_dist_df = df['Grade'].value_counts().reset_index()
                grade_dist_df.columns = ['Grade', 'Count']
                grade_dist_df.to_excel(writer, sheet_name='Grade_Distribution', index=False)
        
        return output.getvalue()
    
    @staticmethod
    def get_report_filename():
        """Generate filename for Excel report"""
        return f"gradeflow_report_{datetime.now().strftime(EXPORT_DATE_FORMAT)}.xlsx"
    
    @staticmethod
    def filter_dataframe(df, grade_filter=None, gender_filter=None, score_range=None):
        """Apply filters to dataframe"""
        filtered_df = df.copy()
        
        if grade_filter and 'Grade' in df.columns:
            filtered_df = filtered_df[filtered_df['Grade'].isin(grade_filter)]
        
        if gender_filter and 'Gender' in df.columns:
            filtered_df = filtered_df[filtered_df['Gender'].isin(gender_filter)]
        
        if score_range and 'Total' in df.columns:
            min_score, max_score = score_range
            filtered_df = filtered_df[
                (filtered_df['Total'] >= min_score) & 
                (filtered_df['Total'] <= max_score)
            ]
        
        return filtered_df
