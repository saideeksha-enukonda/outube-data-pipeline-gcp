import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions

# GCP Configuration
PROJECT_ID = "youtube-data-project-454318"
REGION = "us-east1"  # Use a different region with available resources
SUBSCRIPTION = "projects/youtube-data-project-454318/subscriptions/youtube-comments-sub"
BIGQUERY_TABLE = "youtube_data.comments"

class ParsePubSubMessage(beam.DoFn):
    def process(self, element):
        """Parses Pub/Sub messages and prepares data for BigQuery."""
        message = json.loads(element.decode("utf-8"))
        return [{
            "video_id": message["video_id"],
            "author": message["author"],
            "comment": message["comment"],
            "timestamp": message["timestamp"]
        }]

def run():
    """Runs the Dataflow pipeline to process YouTube comments in real-time."""
    
    pipeline_options = PipelineOptions(
        streaming=True,  # Enable real-time streaming
        project=PROJECT_ID,
        region=REGION,
        runner="DataflowRunner",
        temp_location="gs://youtube-bucket-datatemp/temp/",
        staging_location="gs://youtube-bucket-datatemp/staging/",
        machine_type="n1-standard-1",  # Use a smaller worker machine type
        num_workers=1,  # Limit the number of workers to reduce resource exhaustion
        max_num_workers=2,  # Allow scaling up to only 2 workers
    )

    with beam.Pipeline(options=pipeline_options) as pipeline:
        (
            pipeline
            | "ReadFromPubSub" >> beam.io.ReadFromPubSub(subscription=SUBSCRIPTION)
            | "ParseMessage" >> beam.ParDo(ParsePubSubMessage())
            | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
                BIGQUERY_TABLE,
                schema="video_id:STRING, author:STRING, comment:STRING, timestamp:TIMESTAMP",
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )

if __name__ == "__main__":
    run()
