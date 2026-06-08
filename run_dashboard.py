"""
run_dashboard.py
Script to launch the dashboard
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if all required packages are installed"""
    required = ['streamlit', 'pandas', 'plotly']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"⚠️ Missing packages: {missing}")
        print("Installing missing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
        print("✅ Packages installed!")
    
    return True

def create_data_folder():
    """Create data folder if it doesn't exist"""
    if not os.path.exists('data'):
        os.makedirs('data')
        print("📁 Created 'data' folder")
        print("⚠️ Please place your CSV files in the 'data' folder:")
        print("   - 01_facebook_ads.csv")
        print("   - 02_google_ads.csv")
        print("   - 03_tiktok_ads.csv")
        return False
    return True

def main():
    print("=" * 50)
    print("🚀 MARKETING ANALYTICS DASHBOARD")
    print("=" * 50)
    
    # Check requirements
    check_requirements()
    
    # Check data folder
    if not create_data_folder():
        sys.exit(1)
    
    # Check if CSV files exist
    required_files = ['01_facebook_ads.csv', '02_google_ads.csv', '03_tiktok_ads.csv']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(f'data/{file}'):
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        print("Please add them to the 'data' folder")
        sys.exit(1)
    
    print("\n✅ All files found! Launching dashboard...\n")
    
    # Launch Streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py"
    ])

if __name__ == "__main__":
    main()