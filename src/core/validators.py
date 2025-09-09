"""
Data validation module for GradeFlow application.
"""
import pandas as pd
from config import REQUIRED_COLUMNS, VALID_GENDERS, MIN_SCORE, MAX_SCORE


class DataValidator:
    @staticmethod
    def validate_data(df):
        """Comprehensive data validation based on config"""
        issues = {
            'missing_columns': [],
            'missing_values': {},
            'duplicates': 0,
            'invalid_genders': [],
            'invalid_totals': [],
            'severity': 'success'
        }
        
        # Check missing columns
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            issues['missing_columns'] = missing_cols
            issues['severity'] = 'error'
        
        # Check missing values
        missing_values = df.isnull().sum()
        if missing_values.any():
            issues['missing_values'] = missing_values[missing_values > 0].to_dict()
            if issues['severity'] != 'error':
                issues['severity'] = 'warning'
        
        # Check duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            issues['duplicates'] = duplicates
            if issues['severity'] != 'error':
                issues['severity'] = 'warning'
        
        # Check gender values
        if "Gender" in df.columns:
            valid_genders_lower = [g.lower() for g in VALID_GENDERS]
            invalid_genders = df[~df["Gender"].astype(str).str.lower().isin(valid_genders_lower)]
            if not invalid_genders.empty:
                issues['invalid_genders'] = invalid_genders.index.tolist()
                if issues['severity'] != 'error':
                    issues['severity'] = 'warning'
        
        # Check total scores
        if "Total" in df.columns:
            invalid_totals = df[(df["Total"] < MIN_SCORE) | (df["Total"] > MAX_SCORE) | pd.isna(df["Total"])]
            if not invalid_totals.empty:
                issues['invalid_totals'] = invalid_totals.index.tolist()
                if issues['severity'] != 'error':
                    issues['severity'] = 'warning'
        
        return issues
