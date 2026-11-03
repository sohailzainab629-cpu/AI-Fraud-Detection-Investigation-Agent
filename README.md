# FraudGuard AI – Enterprise Fraud Detection & Investigation Agent

An AI-powered fraud detection and investigation system that identifies suspicious credit card transactions using Machine Learning, FastAPI, LangGraph, Groq AI, and React.

## Project Overview

FraudGuard AI is designed to detect potentially fraudulent credit card transactions and generate AI-powered investigation reports.

The system combines a Machine Learning model with an AI investigation agent to classify transactions, assess risk levels, and recommend appropriate actions. High-risk transactions are automatically sent for human review.

## Key Features

- Credit card fraud detection using Random Forest.
- Data cleaning and exploratory data analysis (EDA).
- Feature engineering using Hour and Amount_log.
- SMOTE for handling imbalanced data.
- Fraud probability prediction.
- Low, Medium, and High risk classification.
- AI-generated investigation reports using LangGraph and Groq.
- Human review workflow with Approve and Reject decisions.
- Interactive React dashboard.
- Fraud analytics and review statistics.
- FastAPI REST API integration.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas & NumPy | Data processing |
| Scikit-learn | Machine Learning |
| Imbalanced-learn | SMOTE |
| Matplotlib & Seaborn | Data visualization |
| FastAPI | Backend API |
| LangGraph | AI workflow orchestration |
| Groq | LLM integration |
| React | Frontend |
| Vite | Frontend development |
| Tailwind CSS | UI styling |
| Joblib | Model serialization |

## Dataset

**Credit Card Fraud Detection Dataset**

- Total cleaned transactions: 283,726
- Legitimate transactions: 283,253
- Fraudulent transactions: 473
- Features: Time, V1–V28, Amount, and engineered features.

The V1–V28 columns are anonymized PCA components.

## Machine Learning Model

A Random Forest Classifier was trained using SMOTE to address class imbalance.

### Model Evaluation Results

| Metric | Score |
|---|---:|
| Accuracy | 99.95% |
| Precision | 91.36% |
| Recall | 77.89% |
| F1 Score | 84.09% |
| ROC-AUC | 96.86% |

## Risk Classification

| Risk Level | Fraud Probability | Recommended Action |
|---|---|---|
| Low | Below 40% | Approve Transaction |
| Medium | 40%–79.99% | Hold for Review |
| High | 80% or above | Block Transaction |

High-risk transactions are automatically added to the human review queue.

**Note:** These actions are system recommendations for this project. The application does not connect to or actually block live banking transactions.

## Project Structure

```text
AI Fraud Detection & Investigation Agent/
│
├── dataset/
│   ├── creditcard.csv
│   ├── cleaned_creditcard.csv
│   └── engineered_creditcard.csv
│
├── ml/
│   ├── data_cleaning.py
│   ├── eda.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── get_sample.py
│   ├── check_high_risk.py
│   └── get_high_risk_sample.py
│
├── models/
│   └── fraud_model.pkl
│
├── backend/
│   ├── main.py
│   ├── schemas.py
│   ├── agent.py
│   └── review.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── index.html
│
├── reports/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd "AI Fraud Detection & Investigation Agent"
```

### 2. Create Virtual Environment

```bash
py -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python Dependencies

```bash
py -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Never upload your actual API key to GitHub.

### 5. Start Backend

From the main project directory:

```powershell
py -m uvicorn backend.main:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

API Documentation:

`http://127.0.0.1:8000/docs`

### 6. Start Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL:

`http://localhost:5173`

If port 5173 is busy, Vite may automatically select another available port.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Backend health check |
| POST | `/predict` | Predict transaction fraud |
| POST | `/investigate` | Run AI investigation |
| GET | `/reviews` | Get human review records |
| GET | `/reviews/{review_id}` | Get review details |
| POST | `/reviews/{review_id}/decision` | Submit human decision |

## Human Review Workflow

1. A transaction is submitted for investigation.
2. The ML model predicts fraud probability.
3. The AI agent assesses the risk and generates an investigation report.
4. High-risk transactions are added to the human review queue.
5. A reviewer can Approve or Reject the transaction.
6. The dashboard updates review status and analytics.

## Future Improvements

- PDF investigation report downloads.
- Email notifications.
- User authentication and role-based access.
