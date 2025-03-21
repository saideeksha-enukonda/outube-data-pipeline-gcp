from google.cloud import storage

# Replace with your GCS bucket name
GCS_BUCKET_NAME = "youtube-bucket-data"
LOCAL_FILE_PATH = "youtube_videos.csv"
GCS_FILE_PATH = "raw_data/youtube_videos.csv"

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to Google Cloud Storage (GCS)"""
    
    # Initialize GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the file
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}.")

# Run the upload function
upload_to_gcs(GCS_BUCKET_NAME, LOCAL_FILE_PATH, GCS_FILE_PATH)
