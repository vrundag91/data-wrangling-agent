import kagglehub
import shutil
import os
import glob

def setup_datasets():
    # Define the datasets we want to download
    # Format: "New Filename" : "Kaggle Dataset Slug"
    datasets = {
        "medical_data.csv": "aamir5659/raw-medical-dataset-for-cleaning-practice",
        "housing_data.csv": "yasserh/housing-prices-dataset",
        "retail_sales.csv": "surajjha101/stores-area-and-sales-data",
        "employee_attrition.csv": "rashikrahmanpritom/heart-attack-analysis-prediction-dataset", 
        "customer_churn.csv": "blastchar/telco-customer-churn"
    }

    # Define directories
    raw_dir = os.path.join("data", "raw")
    clean_dir = os.path.join("data", "clean")
    
    # 1. Cleanup old data to ensure a fresh start
    print("--- Cleaning up old data folders ---")
    if os.path.exists(raw_dir):
        shutil.rmtree(raw_dir)
    if os.path.exists(clean_dir):
        shutil.rmtree(clean_dir)
        
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(clean_dir, exist_ok=True)

    # 2. Download and Move loop
    print(f"--- Downloading {len(datasets)} Datasets ---")
    
    for new_name, slug in datasets.items():
        print(f"\n> Processing: {new_name}")
        try:
            # Download latest version
            path = kagglehub.dataset_download(slug)
            print(f"  Downloaded to cache: {path}")

            # Find the CSV in the downloaded folder
            csv_files = glob.glob(os.path.join(path, "*.csv"))
            
            if csv_files:
                source_file = csv_files[0] # Take the first CSV found
                dest_file = os.path.join(raw_dir, new_name)
                
                # Copy and rename
                shutil.copy(source_file, dest_file)
                print(f"  Success: Moved to {dest_file}")
            else:
                print(f"  Warning: No CSV file found in {slug}")
                
        except Exception as e:
            print(f"  Error downloading {slug}: {e}")

    print("\n--- Setup Complete ---")
    print(f"All raw files are located in: {raw_dir}")

if __name__ == "__main__":
    setup_datasets()