# 🧠 Bankruptcy Prediction API

This project is a **Machine Learning API** that predicts the risk of company bankruptcy using financial indicators. It uses a Logistic Regression model and is served using **FastAPI** for real-time predictions.

---

## 📊 Prediction Task: Risk Modeling

We use a supervised classification model to predict whether a company is likely to go bankrupt (`0` = No, `1` = Yes), based on 95 financial features.

---

## 📁 Dataset

**Company Bankruptcy Prediction Dataset**  
Source: Taiwan Economic Journal (1999–2009)  
Each row represents a company with financial ratios and a binary label:  
`Bankrupt?` → `1` (Yes) or `0` (No)

---

## 👤 API Users

| Attribute          | Details                                     |
|--------------------|---------------------------------------------|
| **Target Users**   | Financial analysts, risk modeling systems   |
| **Request Volume** | ~200 requests/day (scalable)                |
| **Requirements**   | Real-time predictions, JSON response        |

---

## ⚙️ How It Works

1. Client sends a POST request to `/predict` with a list of 95 features.
2. FastAPI receives input and validates it with Pydantic.
3. Features are scaled using `StandardScaler`.
4. Logistic Regression model returns:
   - `prediction`: 0 or 1
   - `probability`: bankruptcy likelihood

---

## 🖥️ Run the API Locally

### 1. Clone the repository

```bash
git clone https://github.com/aseemsyed10/Bankruptcy_API.git
cd Bankruptcy_API
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn main:app --reload
```

Then open: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Sample Input for `/predict`

```json
{
  "features": [0.3, 0.2, 0.1, ..., 0.97]  // 95 values
}
```

Response:

```json
{
  "probability": 0.015,
  "prediction": 0
}
```

---


## 🧭 Architecture Diagram

```plaintext
                +-------------------------+
                |       End User          |
                |  (Financial Analyst)    |
                +-----------+-------------+
                            |
                            | JSON POST request
                            v
                  +---------+----------+
                  |      FastAPI       |
                  |  /predict endpoint |
                  +---------+----------+
                            |
            +---------------+-----------------+
            |                                 |
  +---------v---------+             +---------v---------+
  |  Standard Scaler  |             | Logistic Regression|
  +---------+---------+             +---------+---------+
            |                                 |
            +---------------+-----------------+
                            |
                         JSON Response
```

---

## 📂 Project Structure

```
Bankruptcy_API/
├── main.py
├── model.joblib
├── scaler.joblib
├── requirements.txt
└── README.md
```

---

