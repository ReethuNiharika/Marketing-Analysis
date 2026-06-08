"""
run_dashboard.py
Script to launch the dashboard - CSV files in same directory
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if all required packages are installed"""
    required = ['streamlit', 'pandas', 'plotly', 'numpy']
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

def check_csv_files():
    """Check if CSV files exist in current directory"""
    required_files = ['01_facebook_ads.csv', '02_google_ads.csv', '03_tiktok_ads.csv']
    missing_files = []
    found_files = []
    
    print("\n📁 Checking for CSV files in current directory...")
    print(f"   Current directory: {os.getcwd()}")
    print()
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ Found: {file} ({size:,} bytes)")
            found_files.append(file)
        else:
            print(f"   ❌ Missing: {file}")
            missing_files.append(file)
    
    return found_files, missing_files

def update_data_processor_paths():
    """Update data_processor.py to look in current directory"""
    processor_path = 'data_processor.py'
    
    if not os.path.exists(processor_path):
        print(f"\n⚠️ Warning: {processor_path} not found!")
        print("   Make sure data_processor.py is in the same directory")
        return False
    
    # Read the current content
    with open(processor_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if paths need updating
    if "data/" in content and "'data/'" not in content:
        # Replace paths to look in current directory instead of data folder
        content = content.replace("'data/01_facebook_ads.csv'", "'01_facebook_ads.csv'")
        content = content.replace("'data/02_google_ads.csv'", "'02_google_ads.csv'")
        content = content.replace("'data/03_tiktok_ads.csv'", "'03_tiktok_ads.csv'")
        content = content.replace('"data/01_facebook_ads.csv"', '"01_facebook_ads.csv"')
        content = content.replace('"data/02_google_ads.csv"', '"02_google_ads.csv"')
        content = content.replace('"data/03_tiktok_ads.csv"', '"03_tiktok_ads.csv"')
        
        with open(processor_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("   ✅ Updated data_processor.py to look in current directory")
    
    return True

def create_sample_data_warning():
    """Create a helpful message about sample data"""
    print("\n" + "=" * 60)
    print("📌 IMPORTANT: Data Files Required")
    print("=" * 60)
    print("""
Please place your CSV files in the SAME directory as this script:
    
    📁 Your folder should look like this:
    
    ├── run_dashboard.py      (this file)
    ├── app.py                (dashboard file)
    ├── data_processor.py     (data processing file)
    ├── 01_facebook_ads.csv   (your data)
    ├── 02_google_ads.csv     (your data)
    └── 03_tiktok_ads.csv     (your data)

If you don't have the CSV files, make sure to:
    1. Download them from the assignment
    2. Place them in this folder
    3. Run this script again
""")

def main():
    print("=" * 60)
    print("🚀 MARKETING ANALYTICS DASHBOARD LAUNCHER")
    print("=" * 60)
    
    # Check requirements
    print("\n📦 Checking Python packages...")
    check_requirements()
    
    # Update data processor paths
    print("\n🔧 Configuring data processor...")
    update_data_processor_paths()
    
    # Check for CSV files
    found_files, missing_files = check_csv_files()
    
    if missing_files:
        create_sample_data_warning()
        
        # Ask if user wants to continue anyway (maybe they have the files elsewhere)
        print("\n" + "-" * 60)
        response = input("Do you want to continue anyway? (y/n): ").lower().strip()
        if response != 'y':
            print("\n❌ Exiting. Please add the CSV files and try again.")
            sys.exit(1)
        else:
            print("\n⚠️ Continuing without all CSV files - dashboard may show errors!")
    else:
        print(f"\n✅ All {len(found_files)} CSV files found!")
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print("\n❌ Error: app.py not found in current directory!")
        print("   Please make sure app.py is in the same folder as this script.")
        sys.exit(1)
    
    # Check if data_processor.py exists
    if not os.path.exists('data_processor.py'):
        print("\n❌ Error: data_processor.py not found in current directory!")
        print("   Please make sure data_processor.py is in the same folder as this script.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All checks passed! Launching dashboard...")
    print("=" * 60)
    print("\n🌐 Dashboard will open in your browser shortly...")
    print("   Press Ctrl+C to stop the dashboard\n")
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py", 
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")
        print("\nTry running manually: streamlit run app.py")

if __name__ == "__main__":
    main()