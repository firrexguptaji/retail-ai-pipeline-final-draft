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
* Performs **health & readiness checks**

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
* **Centralized logging** → easier debugging
* **External model + output storage (volumes)** → Docker-friendly

---

# 🐳 Docker Deployment (NEW)

### 🔹 Run the system

```bash
cd docker
docker-compose up --build
```

---

### 🔹 Access UI

```
http://localhost:5000
```

---

### 🔹 Service Ports

| Service  | Port |
| -------- | ---- |
| Gateway  | 5000 |
| Detector | 8001 |
| Grouping | 8002 |

---

### 🔹 Internal Communication

* Detector → `http://detector:8001`
* Grouping → `http://grouping:8002`

---

### 🔹 Volumes

| Local    | Container |
| -------- | --------- |
| models/  | /models   |
| outputs/ | /outputs  |

---

# 🚀 How to Run (Local)

### 🔹 1. Create Virtual Environment

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
pip install -r requirements/requirements-base.txt
pip install -r requirements/requirements-detector.txt
pip install -r requirements/requirements-grouping.txt
```

---

### 🔹 3. Start services

```bash
python run_all.py
```

---

### 🔹 4. Open UI

```
http://127.0.0.1:5000
```

---

## ❤️ Health & Readiness

| Endpoint  | Purpose                           |
| --------- | --------------------------------- |
| `/health` | Service is alive                  |
| `/ready`  | Service is ready to serve traffic |

---

## 🧪 API Flow

1. Upload image → Gateway
2. Gateway → Detector
3. Gateway → Grouping
4. Final response returned

---

### Example Response

```json
{
  "request_id": "...",
  "output_image": "/outputs/result_xxx.jpg",
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
├── common/
│   └── logger.py
│
├── models/
├── outputs/
├── requirements/
├── docker/
│   └── docker-compose.yml
│
├── notebooks/
├── docs/
├── run_all.py
└── README.md
```

---

## 📊 Logging

* Centralized logging via `common/logger.py`
* Each service logs independently

Example:

```
gateway  → request received
detector → detection completed
grouping → clustering completed
```

---

## 📊 Notebook (Model Development)

The notebook (`notebooks/model.ipynb`) was used during experimentation.

### 🔄 Transition to Production

| Notebook         | Production         |
| ---------------- | ------------------ |
| Inline code      | Microservices      |
| Hardcoded values | Config-driven      |
| Sequential flow  | API-based pipeline |

---

## ⚡ Features

* End-to-end ML pipeline
* Microservice architecture
* Dockerized deployment
* Config-driven design
* Centralized logging
* Health & readiness checks

---

## ⚡ Scalability

* Services can scale independently
* Detector can be replicated for heavy workloads
* Gateway remains lightweight

---

## 🔮 Future Improvements

* Fine-tuned embeddings
* Better clustering (DBSCAN / metric learning)
* Kubernetes deployment
* Async processing pipeline

---

## 🏁 Conclusion

This project demonstrates the transition from:

```
Notebook → Production-ready ML system
```

Combining:

* Machine Learning
* Backend Engineering
* System Design
* DevOps (Docker)

---

## 👤 Author

Aman Gupta

