# 🛒 Retail AI Pipeline – Product Detection & Grouping

## 📌 Overview

This project implements a **production-style AI pipeline** to detect and group similar retail products from shelf images.

It is built using a **microservice architecture** with clear separation of responsibilities:

* **Detector Service** → detects product bounding boxes
* **Grouping Service** → groups visually + spatially similar products
* **Gateway Service** → orchestrates services and provides UI

---

## 🏗️ Architecture

```
Client (UI)
   ↓
Gateway Service (Flask)
   ↓
Detector Service (YOLO)
   ↓
Grouping Service (ResNet + Clustering)
   ↓
Final Output (Image + JSON)
```

---

## ⚙️ Services

### 1️⃣ Gateway Service

* Handles image upload
* Orchestrates detector → grouping
* Returns final JSON + image
* Serves output images

---

### 2️⃣ Detector Service

* Uses **YOLOv8**
* Implements:

  * Sliding window detection
  * Low confidence threshold
  * Area filtering
  * Non-Max Suppression (NMS)
  * Aspect ratio filtering
  * Duplicate removal
* Outputs:

  * Bounding boxes
  * Cropped images

---

### 3️⃣ Grouping Service

* Uses **ResNet18 embeddings**
* Combines:

  * Visual features
  * Spatial features
* Applies:

  * Feature normalization
  * Agglomerative clustering
* Outputs:

  * Group IDs
  * Annotated image

---

## 🧠 Key Design Decisions

* **Microservices** → modular & scalable
* **Sliding window detection** → improves recall
* **Spatial + visual fusion** → better grouping
* **Config-driven system** → no hardcoding
* **Logging** → easier debugging

---

## 🚀 How to Run

### 🔹 1. Create Virtual Environment (Recommended)

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 🔹 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 🔹 3. Start services

#### Option A (recommended)

```bash
python run_all.py
```

#### Option B (manual)

```bash
# Terminal 1
cd detector_service
python app.py

# Terminal 2
cd grouping_service
python app.py

# Terminal 3
cd gateway
python app.py
```

---

### 🔹 4. Open UI

```
http://127.0.0.1:5000
```

---

## 🧪 API Flow

1. Upload image → Gateway
2. Gateway → Detector
3. Gateway → Grouping
4. Final response returned

### Example Response

```json
{
  "request_id": "...",
  "output_image": "outputs/result_xxx.jpg",
  "results": [
    {
      "bbox": [x1, y1, x2, y2],
      "group_id": 0
    }
  ]
}
```

---

## 📂 Project Structure

```
project/
│
├── gateway/
├── detector_service/
├── grouping_service/
├── logs/
├── run_all.py
├── requirements.txt
└── README.md
```

---

## 🔧 Configuration & Tuning

All parameters are configurable via `config.py`.

---

### 🎯 Detector Config

```python
SLICE_SIZE = 512
OVERLAP = 0.4
IOU_THRESHOLD = 0.4
MIN_AREA_RATIO = 0.0005
MAX_AREA_RATIO = 0.03
```

---

### 🎯 Grouping Config

```python
DISTANCE_THRESHOLD = 0.6
SPATIAL_WEIGHT = 0.1
IMAGE_SIZE = 224
CLUSTERING_METRIC = "euclidean"
CLUSTERING_LINKAGE = "average"
```

---

### 🔍 Parameter Insights

* **DISTANCE_THRESHOLD**

  * lower → more groups
  * higher → fewer groups

* **SPATIAL_WEIGHT**

  * 0 → visual only
  * 0.1 → balanced
  * higher → spatial bias

---

### 🧪 Experiments

* Increase `DISTANCE_THRESHOLD` → merge clusters
* Reduce `SPATIAL_WEIGHT` → visual grouping
* Increase `OVERLAP` → better detection

---

### ⚙️ Environment Variables

```bash
DISTANCE_THRESHOLD=0.7
SPATIAL_WEIGHT=0.2
```

---

## ⚡ Features

* End-to-end ML pipeline
* Microservice architecture
* UI + API integration
* Config-driven design
* Logging support

---

## 🔮 Future Improvements

* Fine-tuned embeddings
* Better clustering (DBSCAN)
* Docker deployment
* Scaling services

---

## 🏁 Conclusion

This project demonstrates transition from:

```
Notebook → Production-ready ML system
```

Combining:

* Machine Learning
* Backend Engineering
* System Design

---

## 👤 Author

Aman Gupta
