# 🎥 YouTube Data Pipeline on GCP 🚀
### 📌 Overview
This project processes **real-time YouTube comments** and **video insights** using:
✅ **Pub/Sub** → Streams YouTube comments.  
✅ **Dataflow (Apache Beam)** → Processes batch & real-time data.  
✅ **BigQuery** → Stores structured data.  
✅ **Google Sheets** → Creates live dashboards.  

---

## **🔹 Architecture Diagram**
![Architecture Diagram](architecture_diagram.png)

---

## **🔹 Data Pipeline Workflow**
1. **Fetch YouTube Data**:
   - `fetch_youtube_data.py` retrieves video stats (views, likes, comments).
   - Saves data to a CSV file (`youtube_videos.csv`).
2. **Upload to GCS & Load to BigQuery**:
   - `upload_to_gcs.py` uploads the CSV to Google Cloud Storage.
   - `load_to_bigquery.py` moves data from **GCS → BigQuery**.
3. **Stream YouTube Comments in Real-time**:
   - `publish_youtube_comments.py` fetches live comments and pushes them to Pub/Sub.
   - `dataflow_streaming.py` processes comments and writes them to **BigQuery**.

---

## **🔹 Google Sheets Dashboard**
📊 **Live YouTube Dashboard** → [View Here](your-google-sheets-link)

---

## **🔹 How to Run This Project**
### ✅ **1. Clone this repository**
```bash
git clone https://github.com/your-username/youtube-data-pipeline-gcp.git
cd youtube-data-pipeline-gcp

✅ 2.Install Dependencies

pip install apache-beam[gcp] google-cloud-bigquery google-cloud-storage google-cloud-pubsub googleapiclient pandas
✅ 3. Fetch YouTube Video Data

python fetch_youtube_data.py
✅ 4. Upload CSV to Google Cloud Storage

python upload_to_gcs.py
✅ 5. Load CSV from GCS to BigQuery

python load_to_bigquery.py
✅ 6. Stream YouTube Comments in Real-Time

python publish_youtube_comments.py
python dataflow_streaming.py
