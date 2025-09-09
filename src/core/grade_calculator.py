"""
Grade calculation module for GradeFlow application.
"""
import pandas as pd
from config import GRADE_SCALE, PASSING_SCORE


class GradeCalculator:
    @staticmethod
    def assign_grades(scores):
        """Assign letter grades based on config grade scale"""
        grades = []
        for score in scores:
            if pd.isna(score):
                grades.append('N/A')
                continue
            
            grade = 'F'
            for letter, (min_score, max_score) in GRADE_SCALE.items():
                if min_score <= score <= max_score:
                    grade = letter
                    break
            grades.append(grade)
        return grades
    
    @staticmethod
    def calculate_statistics(df):
        """Calculate comprehensive statistics"""
        if 'Total' not in df.columns:
            return {}
        
        stats = {
            'total_students': len(df),
            'mean_score': df['Total'].mean(),
            'median_score': df['Total'].median(),
            'std_score': df['Total'].std(),
            'min_score': df['Total'].min(),
            'max_score': df['Total'].max(),
            'pass_rate': (df['Total'] >= PASSING_SCORE).sum() / len(df) * 100,
        }
        
        # Grade distribution
        grades = GradeCalculator.assign_grades(df['Total'])
        grade_counts = pd.Series(grades).value_counts()
        stats['grade_distribution'] = grade_counts.to_dict()
        
        return stats
