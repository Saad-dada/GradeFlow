"""
Analytics and visualization components for GradeFlow application.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import GRADE_SCALE, PASSING_SCORE


class Analytics:
    @staticmethod
    def display_key_metrics(stats):
        """Display key performance metrics"""
        # Import here to avoid circular imports
        from src.ui.ui_components import display_metric_card
        
        st.subheader("📊 Key Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            display_metric_card(
                "👥 Total Students",
                stats['total_students'],
                help_text="Total number of students in the dataset"
            )
        
        with col2:
            avg_delta = f"{stats['mean_score'] - 50:.1f} from 50%"
            display_metric_card(
                "📈 Average Score",
                f"{stats['mean_score']:.1f}",
                delta=avg_delta,
                help_text="Mean score of all students"
            )
        
        with col3:
            pass_delta = f"{stats['pass_rate'] - 80:.1f}% from 80%"
            display_metric_card(
                "✅ Pass Rate",
                f"{stats['pass_rate']:.1f}%",
                delta=pass_delta,
                help_text=f"Percentage of students scoring ≥{PASSING_SCORE}%"
            )
        
        with col4:
            display_metric_card(
                "📊 Std Deviation",
                f"{stats['std_score']:.1f}",
                help_text="Standard deviation of scores"
            )
    
    @staticmethod
    def display_charts(df):
        """Display comprehensive charts including pie charts and heatmaps"""
        # Create tabs for different chart types
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Bar Charts", "🥧 Pie Charts", "🔥 Heatmaps", "📈 Distribution"])
        
        with tab1:
            Analytics.display_bar_charts(df)
        
        with tab2:
            Analytics.display_pie_charts(df)
        
        with tab3:
            Analytics.display_heatmaps(df)
        
        with tab4:
            Analytics.display_distribution_charts(df)
    
    @staticmethod
    def display_bar_charts(df):
        """Display traditional bar charts"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Grade Distribution")
            if 'Grade' in df.columns:
                grade_counts = df['Grade'].value_counts().reindex(GRADE_SCALE.keys(), fill_value=0)
                st.bar_chart(grade_counts)
        
        with col2:
            st.subheader("📊 Score Statistics")
            score_stats = df['Total'].describe().round(2)
            st.dataframe(score_stats, use_container_width=True)
    
    @staticmethod
    def display_pie_charts(df):
        """Display pie charts for grade and gender distribution"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🥧 Grade Distribution")
            if 'Grade' in df.columns:
                grade_counts = df['Grade'].value_counts()
                
                # Create interactive pie chart with Plotly
                fig_grade = px.pie(
                    values=grade_counts.values,
                    names=grade_counts.index,
                    title="Grade Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_grade.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
                )
                fig_grade.update_layout(
                    showlegend=True,
                    height=400,
                    font=dict(size=12)
                )
                st.plotly_chart(fig_grade, use_container_width=True)
        
        with col2:
            st.subheader("👥 Gender Distribution")
            if 'Gender' in df.columns:
                gender_counts = df['Gender'].value_counts()
                
                # Create gender pie chart
                fig_gender = px.pie(
                    values=gender_counts.values,
                    names=gender_counts.index,
                    title="Gender Distribution",
                    color_discrete_sequence=['#FF6B9D', '#4ECDC4']
                )
                fig_gender.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
                )
                fig_gender.update_layout(
                    showlegend=True,
                    height=400,
                    font=dict(size=12)
                )
                st.plotly_chart(fig_gender, use_container_width=True)
    
    @staticmethod
    def display_heatmaps(df):
        """Display heatmaps for performance analysis"""
        if 'Gender' in df.columns and 'Grade' in df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔥 Grade-Gender Heatmap")
                
                # Create cross-tabulation for heatmap
                grade_gender_crosstab = pd.crosstab(df['Grade'], df['Gender'])
                
                # Create heatmap with Plotly
                fig_heatmap = px.imshow(
                    grade_gender_crosstab.values,
                    labels=dict(x="Gender", y="Grade", color="Count"),
                    x=grade_gender_crosstab.columns,
                    y=grade_gender_crosstab.index,
                    color_continuous_scale='YlOrRd',
                    aspect="auto",
                    title="Grade Distribution by Gender"
                )
                
                # Add text annotations
                for i, row in enumerate(grade_gender_crosstab.index):
                    for j, col in enumerate(grade_gender_crosstab.columns):
                        fig_heatmap.add_annotation(
                            x=j, y=i,
                            text=str(grade_gender_crosstab.loc[row, col]),
                            showarrow=False,
                            font=dict(color="white" if grade_gender_crosstab.loc[row, col] > grade_gender_crosstab.values.max()/2 else "black")
                        )
                
                fig_heatmap.update_layout(height=400)
                st.plotly_chart(fig_heatmap, use_container_width=True)
            
            with col2:
                st.subheader("📊 Performance Correlation")
                
                # Create score range categories for better visualization
                df_copy = df.copy()
                df_copy['Score_Range'] = pd.cut(
                    df_copy['Total'], 
                    bins=[0, 40, 60, 80, 100], 
                    labels=['0-40', '41-60', '61-80', '81-100']
                )
                
                # Create heatmap for score ranges vs gender
                score_gender_crosstab = pd.crosstab(df_copy['Score_Range'], df_copy['Gender'])
                
                fig_score_heatmap = px.imshow(
                    score_gender_crosstab.values,
                    labels=dict(x="Gender", y="Score Range", color="Count"),
                    x=score_gender_crosstab.columns,
                    y=score_gender_crosstab.index,
                    color_continuous_scale='Blues',
                    aspect="auto",
                    title="Score Distribution by Gender"
                )
                
                # Add text annotations
                for i, row in enumerate(score_gender_crosstab.index):
                    for j, col in enumerate(score_gender_crosstab.columns):
                        fig_score_heatmap.add_annotation(
                            x=j, y=i,
                            text=str(score_gender_crosstab.loc[row, col]),
                            showarrow=False,
                            font=dict(color="white" if score_gender_crosstab.loc[row, col] > score_gender_crosstab.values.max()/2 else "black")
                        )
                
                fig_score_heatmap.update_layout(height=400)
                st.plotly_chart(fig_score_heatmap, use_container_width=True)
    
    @staticmethod
    def display_distribution_charts(df):
        """Display distribution and statistical charts"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Score Distribution")
            if 'Total' in df.columns:
                # Histogram with distribution curve
                fig_hist = px.histogram(
                    df, 
                    x='Total',
                    nbins=20,
                    title="Score Distribution",
                    labels={'Total': 'Score', 'count': 'Frequency'},
                    color_discrete_sequence=['#1f77b4']
                )
                fig_hist.update_layout(
                    showlegend=False,
                    height=400,
                    xaxis_title="Score",
                    yaxis_title="Number of Students"
                )
                st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            st.subheader("📊 Box Plot Analysis")
            if 'Total' in df.columns and 'Gender' in df.columns:
                # Box plot for score distribution by gender
                fig_box = px.box(
                    df,
                    x='Gender',
                    y='Total',
                    title="Score Distribution by Gender",
                    color='Gender',
                    color_discrete_sequence=['#FF6B9D', '#4ECDC4']
                )
                fig_box.update_layout(
                    showlegend=False,
                    height=400,
                    xaxis_title="Gender",
                    yaxis_title="Score"
                )
                st.plotly_chart(fig_box, use_container_width=True)
    
    @staticmethod
    def display_gender_analysis(df):
        """Display performance analysis by gender with enhanced visualizations"""
        if 'Gender' in df.columns:
            st.subheader("👥 Performance Analysis by Gender")
            
            # Statistical table
            gender_analysis = df.groupby('Gender').agg({
                'Total': ['count', 'mean', 'std', 'min', 'max']
            }).round(2)
            gender_analysis.columns = ['Count', 'Mean', 'Std Dev', 'Min', 'Max']
            st.dataframe(gender_analysis, use_container_width=True)
            
            # Interactive charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Pass rate by gender
                gender_pass_rate = df.groupby('Gender').apply(
                    lambda x: (x['Total'] >= PASSING_SCORE).sum() / len(x) * 100
                ).round(1)
                
                fig_pass_rate = px.bar(
                    x=gender_pass_rate.index,
                    y=gender_pass_rate.values,
                    title="Pass Rate by Gender",
                    labels={'x': 'Gender', 'y': 'Pass Rate (%)'},
                    color=gender_pass_rate.values,
                    color_continuous_scale='RdYlGn'
                )
                fig_pass_rate.update_layout(
                    showlegend=False,
                    height=350,
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_pass_rate, use_container_width=True)
            
            with col2:
                # Average score by gender
                avg_scores = df.groupby('Gender')['Total'].mean()
                
                fig_avg = px.bar(
                    x=avg_scores.index,
                    y=avg_scores.values,
                    title="Average Score by Gender",
                    labels={'x': 'Gender', 'y': 'Average Score'},
                    color=avg_scores.values,
                    color_continuous_scale='Viridis'
                )
                fig_avg.update_layout(
                    showlegend=False,
                    height=350,
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_avg, use_container_width=True)
    
    @staticmethod
    def create_filter_controls(df):
        """Create filter controls and return filtered dataframe"""
        col1, col2, col3 = st.columns(3)
        
        filters = {}
        
        with col1:
            if 'Grade' in df.columns:
                grade_options = sorted(df['Grade'].unique())
                filters['grade_filter'] = st.multiselect(
                    "🎯 Filter by Grade", 
                    options=grade_options,
                    default=grade_options,
                    help="Select grades to display"
                )
        
        with col2:
            if 'Gender' in df.columns:
                gender_options = df['Gender'].unique()
                filters['gender_filter'] = st.multiselect(
                    "👥 Filter by Gender",
                    options=gender_options,
                    default=gender_options,
                    help="Select genders to display"
                )
        
        with col3:
            if 'Total' in df.columns:
                filters['score_range'] = st.slider(
                    "📊 Score Range",
                    min_value=int(df['Total'].min()),
                    max_value=int(df['Total'].max()),
                    value=(int(df['Total'].min()), int(df['Total'].max())),
                    help="Filter by score range"
                )
        
        return filters
