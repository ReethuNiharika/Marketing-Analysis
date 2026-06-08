"""
================================================================================
MODULE: run_dashboard.py
DESCRIPTION: Launcher script for the Marketing Analytics Dashboard
USAGE: python run_dashboard.py
================================================================================

This script checks for required dependencies, verifies data files,
and launches the Streamlit dashboard application.
"""

import subprocess
import sys
import os


def check_requirements():
    """
    Check if required Python packages are installed.
    If missing, attempt to install them automatically.
    
    Returns:
        bool: True if all requirements are satisfied
    """
    required_packages = ['streamlit', 'pandas', 'plotly', 'numpy']
    missing_packages = []
    
    print("\nChecking Python packages...")
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  [OK] {package}")
        except ImportError:
            print(f"  [MISSING] {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("Packages installed successfully")
        except Exception as error:
            print(f"Error installing packages: {error}")
            return False
    
    return True


def verify_data_files():
    """
    Verify that all required CSV files exist in the current directory.
    
    Returns:
        tuple: (found_files, missing_files) lists of file names
    """
    required_files = [
        '01_facebook_ads.csv',
        '02_google_ads.csv',
        '03_tiktok_ads.csv'
    ]
    
    found_files = []
    missing_files = []
    
    print("\nVerifying data files...")
    print(f"Current directory: {os.getcwd()}")
    print("-" * 50)
    
    for file_name in required_files:
        if os.path.exists(file_name):
            file_size = os.path.getsize(file_name)
            print(f"  [FOUND] {file_name} ({file_size:,} bytes)")
            found_files.append(file_name)
        else:
            print(f"  [MISSING] {file_name}")
            missing_files.append(file_name)
    
    return found_files, missing_files


def update_data_processor_paths():
    """
    Update data_processor.py to look for CSV files in the current directory
    instead of a 'data' subfolder.
    
    Returns:
        bool: True if update was successful or not needed
    """
    processor_path = 'data_processor.py'
    
    if not os.path.exists(processor_path):
        print(f"\nWarning: {processor_path} not found!")
        print("Make sure data_processor.py is in the same directory")
        return False
    
    # Read the current content
    with open(processor_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if paths need updating (look for 'data/' references)
    if "data/" in content and "'data/'" not in content:
        # Replace paths to look in current directory instead of data folder
        content = content.replace("'data/01_facebook_ads.csv'", "'01_facebook_ads.csv'")
        content = content.replace("'data/02_google_ads.csv'", "'02_google_ads.csv'")
        content = content.replace("'data/03_tiktok_ads.csv'", "'03_tiktok_ads.csv'")
        content = content.replace('"data/01_facebook_ads.csv"', '"01_facebook_ads.csv"')
        content = content.replace('"data/02_google_ads.csv"', '"02_google_ads.csv"')
        content = content.replace('"data/03_tiktok_ads.csv"', '"03_tiktok_ads.csv"')
        
        with open(processor_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print("Updated data_processor.py to look in current directory")
    
    return True


def show_help_message():
    """
    Display helpful message about required files and setup.
    """
    print("\n" + "=" * 60)
    print("DATA FILES REQUIRED")
    print("=" * 60)
    print("""
Please place your CSV files in the SAME directory as this script:

    Required folder structure:
    
    YourFolder/
    ├── run_dashboard.py      (this file)
    ├── app.py                (dashboard file)
    ├── data_processor.py     (data processing file)
    ├── 01_facebook_ads.csv   (your data)
    ├── 02_google_ads.csv     (your data)
    └── 03_tiktok_ads.csv     (your data)

If you don't have the CSV files:
    1. Download them from the assignment
    2. Place them in this folder
    3. Run this script again
""")


def verify_application_files():
    """
    Verify that required application files exist.
    
    Returns:
        bool: True if all required files exist
    """
    app_exists = os.path.exists('app.py')
    processor_exists = os.path.exists('data_processor.py')
    
    print("\nVerifying application files...")
    print(f"  app.py: {'[FOUND]' if app_exists else '[MISSING]'}")
    print(f"  data_processor.py: {'[FOUND]' if processor_exists else '[MISSING]'}")
    
    if not app_exists:
        print("\nError: app.py not found in current directory!")
        print("Please make sure app.py is in the same folder as this script.")
        return False
    
    if not processor_exists:
        print("\nError: data_processor.py not found in current directory!")
        print("Please make sure data_processor.py is in the same folder as this script.")
        return False
    
    return True


def launch_dashboard():
    """
    Launch the Streamlit dashboard application.
    """
    print("\n" + "=" * 60)
    print("LAUNCHING DASHBOARD")
    print("=" * 60)
    print("\nStreamlit server starting...")
    print("The dashboard will open in your default web browser.")
    print("Press Ctrl+C to stop the server when done.\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n\nDashboard stopped by user.")
    except Exception as error:
        print(f"\nError launching dashboard: {error}")
        print("\nTry running manually: streamlit run app.py")


def main():
    """
    Main execution function.
    Orchestrates all pre-launch checks and starts the dashboard.
    """
    print("=" * 60)
    print("MARKETING ANALYTICS DASHBOARD LAUNCHER")
    print("=" * 60)
    
    # Step 1: Check Python packages
    print("\nChecking Python packages...")
    if not check_requirements():
        print("\nFailed to install required packages. Please install manually.")
        sys.exit(1)
    
    # Step 2: Update data processor paths
    print("\nConfiguring data processor...")
    update_data_processor_paths()
    
    # Step 3: Verify data files exist
    found_files, missing_files = verify_data_files()
    
    if missing_files:
        show_help_message()
        
        # Ask if user wants to continue anyway
        print("\n" + "-" * 50)
        user_response = input("Continue anyway? (y/n): ").lower().strip()
        if user_response != 'y':
            print("\nExiting. Please add the required CSV files.")
            sys.exit(1)
        else:
            print("\nContinuing without all CSV files - dashboard may show errors!")
    else:
        print(f"\nAll {len(found_files)} CSV files found!")
    
    # Step 4: Verify application files exist
    if not verify_application_files():
        sys.exit(1)
    
    # Step 5: Launch the dashboard
    launch_dashboard()


if __name__ == "__main__":
    main()
