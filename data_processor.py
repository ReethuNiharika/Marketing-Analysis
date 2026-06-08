"""
================================================================================
MODULE: data_processor.py
DESCRIPTION: Marketing data processing and unification module
AUTHOR: Marketing Analytics Team
VERSION: 2.0.0
================================================================================

This module handles loading, cleaning, and unifying marketing data from
Facebook, Google, and TikTok advertising platforms.
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')


class MarketingDataProcessor:
    """
    Main class for processing marketing data from multiple platforms.
    
    Attributes:
        facebook_path (str): Path to Facebook CSV file
        google_path (str): Path to Google CSV file
        tiktok_path (str): Path to TikTok CSV file
        unified_df (DataFrame): Combined data from all platforms
    """
    
    def __init__(self, 
                 facebook_path='01_facebook_ads.csv',
                 google_path='02_google_ads.csv',
                 tiktok_path='03_tiktok_ads.csv'):
        """
        Initialize the data processor with file paths.
        
        Args:
            facebook_path: Path to Facebook ads CSV file
            google_path: Path to Google ads CSV file
            tiktok_path: Path to TikTok ads CSV file
        """
        self.facebook_path = facebook_path
        self.google_path = google_path
        self.tiktok_path = tiktok_path
        
        # Data storage
        self.facebook_df = None
        self.google_df = None
        self.tiktok_df = None
        self.unified_df = None
        
    def load_data(self):
        """
        Load all CSV files from the current directory.
        
        Returns:
            tuple: (facebook_df, google_df, tiktok_df) DataFrames for each platform
            
        Raises:
            FileNotFoundError: If any required CSV file is missing
        """
        print("Loading data files...")
        print(f"Current directory: {os.getcwd()}")
        
        # Check for missing files
        missing_files = []
        for path, name in [(self.facebook_path, 'Facebook'),
                           (self.google_path, 'Google'),
                           (self.tiktok_path, 'TikTok')]:
            if not os.path.exists(path):
                missing_files.append(f"{name} ({path})")
        
        if missing_files:
            print(f"ERROR: Missing files: {', '.join(missing_files)}")
            print("\nPlease ensure the following files are in the current directory:")
            print("   - 01_facebook_ads.csv")
            print("   - 02_google_ads.csv")
            print("   - 03_tiktok_ads.csv")
            raise FileNotFoundError(f"Missing files: {missing_files}")
        
        # Load CSV files
        self.facebook_df = pd.read_csv(self.facebook_path)
        self.google_df = pd.read_csv(self.google_path)
        self.tiktok_df = pd.read_csv(self.tiktok_path)
        
        # Convert date columns to datetime
        self.facebook_df['date'] = pd.to_datetime(self.facebook_df['date'])
        self.google_df['date'] = pd.to_datetime(self.google_df['date'])
        self.tiktok_df['date'] = pd.to_datetime(self.tiktok_df['date'])
        
        print(f"Facebook: {len(self.facebook_df)} rows loaded")
        print(f"Google: {len(self.google_df)} rows loaded")
        print(f"TikTok: {len(self.tiktok_df)} rows loaded")
        
        return self.facebook_df, self.google_df, self.tiktok_df
    
    def clean_data(self):
        """
        Clean and standardize data across all platforms.
        
        This method:
        1. Renames columns for consistency (spend -> cost)
        2. Adds missing columns to each platform
        3. Calculates derived metrics (CTR, CPC)
        4. Handles null values
        
        Returns:
            bool: True if cleaning was successful
        """
        print("\nCleaning data...")
        
        # Facebook: Rename 'spend' column to 'cost' for consistency
        if 'spend' in self.facebook_df.columns:
            self.facebook_df = self.facebook_df.rename(columns={'spend': 'cost'})
        
        # Add missing columns to Facebook data
        self.facebook_df['conversion_value'] = 0
        self.facebook_df['ctr'] = (self.facebook_df['clicks'] / 
                                    self.facebook_df['impressions'] * 100).round(2)
        self.facebook_df['avg_cpc'] = (self.facebook_df['cost'] / 
                                        self.facebook_df['clicks']).round(2)
        
        # Add missing columns to Google data
        self.google_df['video_views'] = 0
        self.google_df['likes'] = 0
        self.google_df['shares'] = 0
        self.google_df['comments'] = 0
        
        # Add missing columns to TikTok data
        self.tiktok_df['engagement_rate'] = 0
        self.tiktok_df['reach'] = 0
        self.tiktok_df['frequency'] = 0
        self.tiktok_df['conversion_value'] = 0
        self.tiktok_df['ctr'] = (self.tiktok_df['clicks'] / 
                                  self.tiktok_df['impressions'] * 100).round(2)
        self.tiktok_df['avg_cpc'] = (self.tiktok_df['cost'] / 
                                      self.tiktok_df['clicks']).round(2)
        
        # Fill any remaining null values with zeros
        for df in [self.facebook_df, self.google_df, self.tiktok_df]:
            df.fillna(0, inplace=True)
        
        print("Data cleaning complete")
        return True
    
    def create_unified_table(self):
        """
        Create a unified table combining data from all platforms.
        
        This method standardizes column names and structure across platforms,
        then concatenates them into a single DataFrame.
        
        Returns:
            DataFrame: Unified marketing data
        """
        print("\nCreating unified table...")
        
        # Standardize Facebook data structure
        facebook_unified = self.facebook_df[[
            'date', 'campaign_id', 'campaign_name', 'ad_set_id', 'ad_set_name',
            'impressions', 'clicks', 'cost', 'conversions', 'video_views',
            'reach', 'frequency', 'ctr', 'avg_cpc'
        ]].copy()
        facebook_unified['platform'] = 'Facebook'
        facebook_unified['conversion_value'] = 0
        facebook_unified['video_watch_25'] = 0
        facebook_unified['video_watch_50'] = 0
        facebook_unified['video_watch_75'] = 0
        facebook_unified['video_watch_100'] = 0
        facebook_unified['likes'] = 0
        facebook_unified['shares'] = 0
        facebook_unified['comments'] = 0
        
        # Standardize Google data structure
        google_unified = self.google_df[[
            'date', 'campaign_id', 'campaign_name', 'ad_group_id', 'ad_group_name',
            'impressions', 'clicks', 'cost', 'conversions', 'video_views'
        ]].copy()
        google_unified['platform'] = 'Google'
        google_unified['conversion_value'] = self.google_df['conversion_value']
        google_unified['reach'] = 0
        google_unified['frequency'] = 0
        google_unified['ctr'] = self.google_df['ctr']
        google_unified['avg_cpc'] = self.google_df['avg_cpc']
        google_unified['video_watch_25'] = 0
        google_unified['video_watch_50'] = 0
        google_unified['video_watch_75'] = 0
        google_unified['video_watch_100'] = 0
        google_unified['likes'] = 0
        google_unified['shares'] = 0
        google_unified['comments'] = 0
        
        # Standardize TikTok data structure
        tiktok_unified = self.tiktok_df[[
            'date', 'campaign_id', 'campaign_name', 'adgroup_id', 'adgroup_name',
            'impressions', 'clicks', 'cost', 'conversions', 'video_views'
        ]].copy()
        tiktok_unified['platform'] = 'TikTok'
        tiktok_unified['conversion_value'] = 0
        tiktok_unified['reach'] = 0
        tiktok_unified['frequency'] = 0
        tiktok_unified['ctr'] = self.tiktok_df['ctr']
        tiktok_unified['avg_cpc'] = self.tiktok_df['avg_cpc']
        tiktok_unified['video_watch_25'] = self.tiktok_df['video_watch_25']
        tiktok_unified['video_watch_50'] = self.tiktok_df['video_watch_50']
        tiktok_unified['video_watch_75'] = self.tiktok_df['video_watch_75']
        tiktok_unified['video_watch_100'] = self.tiktok_df['video_watch_100']
        tiktok_unified['likes'] = self.tiktok_df['likes']
        tiktok_unified['shares'] = self.tiktok_df['shares']
        tiktok_unified['comments'] = self.tiktok_df['comments']
        
        # Rename columns for consistency across platforms
        for df in [facebook_unified, google_unified, tiktok_unified]:
            if 'ad_set_id' in df.columns:
                df.rename(columns={
                    'ad_set_id': 'ad_group_id',
                    'ad_set_name': 'ad_group_name'
                }, inplace=True)
            if 'adgroup_id' in df.columns:
                df.rename(columns={
                    'adgroup_id': 'ad_group_id',
                    'adgroup_name': 'ad_group_name'
                }, inplace=True)
        
        # Combine all platform data into one DataFrame
        self.unified_df = pd.concat([facebook_unified, google_unified, tiktok_unified], 
                                    ignore_index=True)
        
        # Calculate additional performance metrics
        self.unified_df['ctr'] = (self.unified_df['clicks'] / 
                                   self.unified_df['impressions'] * 100).round(2)
        self.unified_df['cpc'] = (self.unified_df['cost'] / 
                                   self.unified_df['clicks'].replace(0, np.nan)).round(2)
        self.unified_df['cpa'] = (self.unified_df['cost'] / 
                                   self.unified_df['conversions'].replace(0, np.nan)).round(2)
        self.unified_df['conversion_rate'] = (self.unified_df['conversions'] / 
                                               self.unified_df['clicks'].replace(0, np.nan) * 100).round(2)
        
        print(f"Unified table created: {len(self.unified_df)} rows")
        return self.unified_df
    
    def create_daily_summary(self):
        """
        Create daily performance summary aggregated by date and platform.
        
        Returns:
            DataFrame: Daily summary with metrics like impressions, clicks, cost, conversions
        """
        print("\nCreating daily summary...")
        
        daily_summary = self.unified_df.groupby(['date', 'platform']).agg({
            'impressions': 'sum',
            'clicks': 'sum',
            'cost': 'sum',
            'conversions': 'sum',
            'video_views': 'sum'
        }).reset_index()
        
        # Calculate derived metrics for each day
        daily_summary['ctr'] = (daily_summary['clicks'] / 
                                 daily_summary['impressions'] * 100).round(2)
        daily_summary['cpc'] = (daily_summary['cost'] / 
                                 daily_summary['clicks'].replace(0, np.nan)).round(2)
        daily_summary['cpa'] = (daily_summary['cost'] / 
                                 daily_summary['conversions'].replace(0, np.nan)).round(2)
        
        # Calculate day-over-day changes
        daily_summary = daily_summary.sort_values(['platform', 'date'])
        daily_summary['prev_day_cost'] = daily_summary.groupby('platform')['cost'].shift(1)
        daily_summary['cost_dod_change'] = ((daily_summary['cost'] - daily_summary['prev_day_cost']) / 
                                             daily_summary['prev_day_cost'] * 100).round(2)
        
        print("Daily summary created")
        return daily_summary
    
    def create_campaign_performance(self):
        """
        Create campaign-level performance summary.
        
        Returns:
            DataFrame: Campaign performance metrics aggregated by campaign
        """
        print("\nCreating campaign performance...")
        
        campaign_perf = self.unified_df.groupby(['platform', 'campaign_name']).agg({
            'impressions': 'sum',
            'clicks': 'sum',
            'cost': 'sum',
            'conversions': 'sum',
            'video_views': 'sum'
        }).reset_index()
        
        # Calculate performance metrics for each campaign
        campaign_perf['ctr'] = (campaign_perf['clicks'] / 
                                 campaign_perf['impressions'] * 100).round(2)
        campaign_perf['cpc'] = (campaign_perf['cost'] / 
                                 campaign_perf['clicks'].replace(0, np.nan)).round(2)
        campaign_perf['cpa'] = (campaign_perf['cost'] / 
                                 campaign_perf['conversions'].replace(0, np.nan)).round(2)
        campaign_perf['conversion_rate'] = (campaign_perf['conversions'] / 
                                             campaign_perf['clicks'].replace(0, np.nan) * 100).round(2)
        
        print("Campaign performance created")
        return campaign_perf
    
    def create_tiktok_engagement_analysis(self):
        """
        Create TikTok-specific engagement analysis.
        
        Returns:
            DataFrame: TikTok metrics including watch rates and engagement
        """
        print("\nCreating TikTok engagement analysis...")
        
        tiktok_analysis = self.tiktok_df.copy()
        
        # Calculate video retention rates at different watch points
        tiktok_analysis['watch_25_rate'] = (tiktok_analysis['video_watch_25'] / 
                                             tiktok_analysis['video_views'] * 100).round(2)
        tiktok_analysis['watch_50_rate'] = (tiktok_analysis['video_watch_50'] / 
                                             tiktok_analysis['video_views'] * 100).round(2)
        tiktok_analysis['watch_75_rate'] = (tiktok_analysis['video_watch_75'] / 
                                             tiktok_analysis['video_views'] * 100).round(2)
        tiktok_analysis['completion_rate'] = (tiktok_analysis['video_watch_100'] / 
                                               tiktok_analysis['video_views'] * 100).round(2)
        
        # Calculate social engagement metrics
        tiktok_analysis['total_engagement'] = (tiktok_analysis['likes'] + 
                                                tiktok_analysis['shares'] + 
                                                tiktok_analysis['comments'])
        tiktok_analysis['engagement_rate'] = (tiktok_analysis['total_engagement'] / 
                                               tiktok_analysis['video_views'] * 100).round(2)
        
        print("TikTok analysis created")
        return tiktok_analysis
    
    def create_google_roas_analysis(self):
        """
        Create Google-specific ROAS (Return on Ad Spend) analysis.
        
        Returns:
            DataFrame: Google metrics including ROAS and CPA
        """
        print("\nCreating Google ROAS analysis...")
        
        google_roas = self.google_df.copy()
        google_roas['roas'] = (google_roas['conversion_value'] / 
                                google_roas['cost']).round(2)
        google_roas['cpa'] = (google_roas['cost'] / 
                               google_roas['conversions'].replace(0, np.nan)).round(2)
        
        print("Google ROAS analysis created")
        return google_roas
    
    def run_all(self):
        """
        Execute the complete data processing pipeline.
        
        This method runs all processing steps in order:
        1. Load raw data
        2. Clean and standardize
        3. Create unified table
        4. Generate all derived datasets
        
        Returns:
            dict: Dictionary containing all processed DataFrames
        """
        print("=" * 50)
        print("STARTING DATA PROCESSING PIPELINE")
        print("=" * 50)
        
        # Execute processing steps in sequence
        self.load_data()
        self.clean_data()
        self.create_unified_table()
        
        # Create derived datasets
        self.daily_summary = self.create_daily_summary()
        self.campaign_performance = self.create_campaign_performance()
        self.tiktok_analysis = self.create_tiktok_engagement_analysis()
        self.google_roas = self.create_google_roas_analysis()
        
        print("\n" + "=" * 50)
        print("DATA PROCESSING COMPLETE")
        print("=" * 50)
        
        # Return all processed data
        return {
            'unified': self.unified_df,
            'daily_summary': self.daily_summary,
            'campaign_performance': self.campaign_performance,
            'tiktok_analysis': self.tiktok_analysis,
            'google_roas': self.google_roas,
            'facebook': self.facebook_df,
            'google': self.google_df,
            'tiktok': self.tiktok_df
        }
    
    def get_key_metrics(self):
        """
        Calculate high-level key metrics for dashboard display.
        
        Returns:
            dict: Dictionary containing key performance indicators
        """
        unified = self.unified_df
        
        # Calculate overall metrics
        total_spend = unified['cost'].sum()
        total_impressions = unified['impressions'].sum()
        total_clicks = unified['clicks'].sum()
        total_conversions = unified['conversions'].sum()
        
        # Calculate rate metrics (with division by zero protection)
        overall_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        overall_cpa = (total_spend / total_conversions) if total_conversions > 0 else 0
        
        # Calculate platform-level metrics
        platform_metrics = unified.groupby('platform').agg({
            'cost': 'sum',
            'impressions': 'sum',
            'clicks': 'sum',
            'conversions': 'sum',
            'video_views': 'sum'
        }).round(2).to_dict()
        
        # Calculate CPA per platform
        platform_cpa = {}
        for platform in unified['platform'].unique():
            platform_data = unified[unified['platform'] == platform]
            cpa = (platform_data['cost'].sum() / 
                   platform_data['conversions'].sum()) if platform_data['conversions'].sum() > 0 else 0
            platform_cpa[platform] = round(cpa, 2)
        
        metrics = {
            'total_spend': total_spend,
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_conversions': total_conversions,
            'total_video_views': unified['video_views'].sum(),
            'overall_ctr': overall_ctr,
            'overall_cpa': overall_cpa,
            'platform_metrics': platform_metrics,
            'platform_cpa': platform_cpa
        }
        
        return metrics


# ============================================================================
# Script Execution
# ============================================================================
if __name__ == "__main__":
    # Run the processor when script is executed directly
    processor = MarketingDataProcessor()
    results = processor.run_all()
    
    # Display key metrics summary
    print("\nKEY METRICS SUMMARY")
    print("-" * 30)
    metrics = processor.get_key_metrics()
    print(f"Total Spend: ${metrics['total_spend']:,.2f}")
    print(f"Total Conversions: {metrics['total_conversions']:,.0f}")
    print(f"Overall CPA: ${metrics['overall_cpa']:.2f}")
    print(f"Platform CPAs: {metrics['platform_cpa']}")