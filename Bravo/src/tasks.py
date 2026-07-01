def run_extraction(**context):
    print("[STEP 1] Starting extraction...")
    output_path = "data/raw/landing.json"
    
    ti = context["ti"]
    ti.xcom_push(key="raw_file_location", value=output_path)
    print("[STEP 3] Pushed file path to Airflow memory.")


def run_validation(**context):
    print("[STEP 1] Starting validation...")
    
    ti = context["ti"]
    
    input_path = ti.xcom_pull(task_ids="one", key="raw_file_location")
    print(f"[STEP 2] Pulled file path from Airflow memory: {input_path}")
    
    if input_path is None:
        print("[ERROR] Could not find the file path from the extraction step!")
        return

    print(f"[STEP 3] Ready to process file at: {input_path}")