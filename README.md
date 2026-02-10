# Chemical Equipment Parameter Visualizer  
### Hybrid Web + Desktop Application

This project is developed as part of an internship screening task.  
It is a hybrid application that runs as both a Web App and a Desktop App to analyze and visualize chemical equipment data from CSV files.

The system allows users to upload equipment datasets and automatically generates analytics, summaries, and charts to support monitoring and decision-making.

---

# 🚀 Tech Stack

## Backend
- Django
- Django REST Framework
- Pandas
- SQLite

## Web Frontend
- React.js
- Chart.js
- Axios

## Desktop Frontend
- PyQt5
- Matplotlib

---

# 📊 Features

✔ Upload CSV files  
✔ Automatic data parsing & analytics  
✔ Equipment type distribution charts  
✔ Summary statistics (averages, counts)  
✔ Dataset history (last 5 uploads)  
✔ PDF report generation  
✔ Basic authentication  
✔ Hybrid access (Web + Desktop)

---

# 📂 Project Structure

```
chemical-equipment-visualizer
│
├── backend/
├── web-frontend/
├── desktop-frontend/
├── sample_equipment_data.csv
├── README.md
└── .gitignore
```

---

# ⚙️ Setup Instructions

---

## 1️⃣ Clone the Repository

```
git clone https://github.com/shrutidahivalikar06/chemical-equipment-visualizer.git
cd chemical-equipment-visualizer
```

---

# 🔹 Backend Setup (Django)

### Step 1
```
cd backend
```

### Step 2 – Create virtual environment

Windows:
```
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### Step 3 – Install dependencies
```
pip install -r requirements.txt
```

### Step 4 – Run migrations
```
python manage.py migrate
```

### Step 5 – Start server
```
python manage.py runserver
```

Backend runs at:
```
http://127.0.0.1:8000
```

---

# 🔹 Web Frontend Setup (React)

Open a new terminal:

### Step 1
```
cd web-frontend
```

### Step 2
```
npm install
```

### Step 3
```
npm start
```

Runs at:
```
http://localhost:3000
```

---

# 🔹 Desktop App Setup (PyQt5)

Open another terminal:

### Step 1
```
cd desktop-frontend
```

### Step 2
```
pip install pyqt5 matplotlib requests
```

### Step 3
```
python main.py
```

---

# 📂 Sample Data

A sample dataset is included:

```
sample_equipment_data.csv
```

Use it to test CSV upload and visualization.

---

# 🔐 Authentication

Basic authentication is enabled to protect API endpoints.

---

# 📝 API Endpoints

```
/upload/ → Upload CSV file  
/summary/ → Get summary statistics  
/history/ → Retrieve last 5 datasets  
/generate-pdf/ → Export PDF report

# 📌 Future Enhancements

- Predictive maintenance using Machine Learning  
- Cloud deployment  
- Role-based access control  
- Real-time IoT integration  
- Advanced UI/UX improvements



