from google.cloud import bigquery

# Replace with your values
PROJECT_ID = "youtube-data-project-454318"
DATASET_ID = "youtube_data"
TABLE_ID = "videos"
GCS_URI = "gs://youtube-bucket-data/raw_data/youtube_videos.csv"

def load_csv_to_bigquery():
    """Loads CSV data from GCS into a BigQuery table."""
    
    client = bigquery.Client(project=PROJECT_ID)

    # Define BigQuery table schema
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("Video_ID", "STRING"),
            bigquery.SchemaField("Title", "STRING"),
            bigquery.SchemaField("Published_At", "TIMESTAMP"),
            bigquery.SchemaField("Views", "INTEGER"),
            bigquery.SchemaField("Likes", "INTEGER"),
            bigquery.SchemaField("Comments", "INTEGER"),
        ],
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Skip header row
        autodetect=False
    )

    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    # Load data from GCS to BigQuery
    load_job = client.load_table_from_uri(
        GCS_URI, table_ref, job_config=job_config
    )
    load_job.result()  # Waits for the job to complete

    print(f"Data successfully loaded into {table_ref}.")

# Run function
load_csv_to_bigquery()
