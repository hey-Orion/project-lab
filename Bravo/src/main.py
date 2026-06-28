# src/tasks.py

def run_extraction(**context):
    print("🚀 [INFRASTRUCTURE] Fetching raw data stream...")
    output_path = "data/raw/landing.json"
    
    ti = context["ti"]

    ti.xcom_push(key="raw_file_location", value=output_path)
    print(f"💾 [XCOM] Pushed raw asset lineage link: {output_path}")

def run_validation(**context):
    ti = context["ti"]

    input_path = ti.xcom_pull(task_ids="ingest_raw_stream", key="raw_file_location")
    
    print(f"🛡️ [XCOM] Pulled raw asset lineage link: {input_path}")
    print(f"📊 [INFRASTRUCTURE] Processing inputs found at {input_path}...")