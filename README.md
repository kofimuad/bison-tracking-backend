# 🐃 Real-time Bison Tracking Backend System

This repository contains the backend infrastructure for a real-time bison tracking system. It is designed to ingest detection data from a separate Computer Vision (CV) inference script, persist the data in a MongoDB database, and expose live statistics via a fast and efficient **FastAPI** web API.

## ✨ Features

  * **Asynchronous Data Ingestion:** A dedicated ingestor script fetches live bison count statistics (FPS, total detections, confidence, etc.) from the CV model's local server.
  * **Persistent Storage:** Data is stored in a MongoDB database for historical tracking and analysis.
  * **High-Performance API:** Built with **FastAPI** for asynchronous, high-speed access to the latest tracking metrics.
  * **Modular Design:** Code is organized into routers, models, and database connection modules for clarity and maintainability.

## ⚙️ Prerequisites

To run this system, you need the following installed:

1.  **Python 3.8+**
2.  **MongoDB Server:** A running instance of the MongoDB database (locally or remotely).
3.  **The Provided Inference Script:** The `rtsp_bison_tracker_2.py` file must be accessible and configured to run.
4.  **FFmpeg:** Required by the inference script for HLS streaming (optional, but recommended).

## 🚀 Getting Started

Follow these steps to get the entire system up and running.

### 1\. Project Setup

First, clone the repository and set up your Python environment:

```bash
# Clone the repository
git clone [YOUR_REPO_URL]
cd bison-tracking-backend

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate
```

### 2\. Install Dependencies

Install all necessary Python packages for the FastAPI app and the ingestor:

```bash
pip install -r requirements.txt
```

### 3\. Configure Environment Variables

Create a file named **`.env`** in the root directory and add your MongoDB connection details.

```bash
# .env file
MONGO_DETAILS="[Connection_String]"
```

### 4\. Run the Program (Three Steps)

This system requires three separate processes to be running concurrently:

#### A. Start the Computer Vision Inference Script

This script generates the real-time data and exposes it via its own local HTTP endpoint (`http://localhost:8080/stats`).

1.  Open **Terminal 1**.
2.  Navigate to the inference script directory:
    ```bash
    cd inference_script/
    ```
3.  Run the script (ensure you have its required dependencies, like `opencv-python` and `ultralytics`):
    ```bash
    python rtsp_bison_tracker_2.py
    ```
    *Leave this terminal running.*

#### B. Start the Data Ingestor

This Python script is responsible for periodically fetching data from the inference script's `/stats` endpoint and writing it to your MongoDB.

1.  Open **Terminal 2**.
2.  Navigate back to the root directory:
    ```bash
    cd ..
    ```
3.  Run the ingestor script:
    ```bash
    python ingestor.py
    ```
    *Leave this terminal running.* You should see messages like "Saved stats for frame: \[number]".

#### C. Start the FastAPI Web API

This is your main backend application that serves the data to the frontend. It runs using the Uvicorn ASGI server.

1.  Open **Terminal 3**.
2.  Run the FastAPI application:
    ```bash
    uvicorn main:app --reload --port 5000
    ```

The API is now running at `http://127.0.0.1:5000`.

## 🧭 API Endpoints

The system exposes the following API endpoints under the **`/api/v1`** prefix:

| Method | Endpoint | Description | Response Model |
| :--- | :--- | :--- | :--- |
| `GET` | `/latest_stats` | Retrieves the **single most recent** bison tracking record from the database. | `BisonStats` |
| `GET` | `/all_stats` | Retrieves **all** historical tracking records from the database. | `List[BisonStats]` |

### Example Request (Latest Stats)

You can test the API by navigating to the interactive **Swagger UI** documentation at:

👉 **`http://127.0.0.1:5000/docs`**

Or by directly calling the endpoint in your browser:

```
http://127.0.0.1:5000/latest_stats
```

### Example JSON Response

```json
{
  "total_frames": 1250,
  "total_detections": 35,
  "max_bison_in_frame": 7,
  "avg_confidence": 0.945,
  "fps": 23.8,
  "timestamp": "2025-09-25T08:30:00.123Z",
  "_id": "65134c4f9f8c6d3b4d8d1f2a"
}
```

## 🛑 Stopping the System

To shut down the entire system gracefully, go to each of the three terminals and press **`Ctrl + C`**.