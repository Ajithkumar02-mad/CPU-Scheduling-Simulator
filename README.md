# CPU Scheduling Simulator

An interactive full-stack CPU Scheduling Simulator for visualizing CPU scheduling algorithms, process execution, Gantt charts, performance metrics, animations, and step-by-step solutions.

## 🚀 Features

- Interactive CPU scheduling simulator
- 6 CPU scheduling algorithms
- Process configuration
- Arrival Time, Burst Time, and Priority inputs
- Time Quantum support for Round Robin
- Gantt Chart visualization
- Process execution animation
- Completion Time
- Turnaround Time
- Waiting Time
- Response Time
- Average performance metrics
- Performance charts
- Step-by-step solution generation
- Beginner-friendly algorithm explanations
- Worked examples and exam tips
- Algorithm navigation
- Simulator navigation
- Light/Dark mode
- Responsive UI
- REST API backend
- Automated testing

## 🧠 Supported Algorithms

1. FCFS — First Come First Serve
2. SJF — Shortest Job First
3. SRTF — Shortest Remaining Time First
4. Round Robin
5. Priority Scheduling — Non-Preemptive
6. Priority Scheduling — Preemptive

## 🛠️ Tech Stack

### Frontend
- React
- Vite
- JavaScript
- HTML5
- CSS3
- Axios
- Recharts

### Backend
- Python
- Flask
- Flask-CORS

### Testing
- Pytest

### Tools
- Git
- GitHub
- VS Code
- npm
- Python Virtual Environment

## 📁 Project Structure

```text
CPU-Scheduling-Simulator/
│
├── backend/
│   ├── algorithms/
│   │   ├── fcfs.py
│   │   ├── sjf.py
│   │   ├── srtf.py
│   │   ├── round_robin.py
│   │   ├── priority_non_preemptive.py
│   │   ├── priority_preemptive.py
│   │   └── registry.py
│   │
│   ├── models/
│   │   └── process.py
│   │
│   ├── utils/
│   │   ├── validators.py
│   │   └── explanation.py
│   │
│   ├── tests/
│   ├── app.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AlgorithmTheory.jsx
│   │   │   ├── GanttChart.jsx
│   │   │   ├── PerformanceCharts.jsx
│   │   │   ├── ProcessTable.jsx
│   │   │   ├── ResultsTable.jsx
│   │   │   ├── SimulationAnimation.jsx
│   │   │   └── SolutionExplanation.jsx
│   │   │
│   │   ├── data/
│   │   │   └── algorithmTheory.js
│   │   │
│   │   ├── pages/
│   │   │   └── Simulator.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   └── ...
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── ...
│
└── README.md

## 📋 Requirements

Make sure the following are installed on your system:

- Python 3.x
- Node.js
- npm
- Git

---

## 📥 Clone the Repository

Open a terminal and run:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd CPU-Scheduling-Simulator



## ⚙️ Installation & Setup
🐍 Backend Setup

Navigate to the backend folder:

cd backend

Create a Python virtual environment:

python -m venv venv

Activate the virtual environment:

.\venv\Scripts\Activate.ps1

Install the required Python packages:

pip install -r requirements.txt

Start the Flask backend:

python app.py

Backend will run at:

http://127.0.0.1:5000
⚛️ Frontend Setup

Open a new terminal and navigate to the frontend folder:

cd CPU-Scheduling-Simulator\frontend

Install frontend dependencies:

npm install

Start the development server:

npm run dev

Frontend will run at:

http://localhost:5173
🧪 Testing

To run the backend test suite:

cd backend
.\venv\Scripts\Activate.ps1
pytest -v

Expected result:

68 passed
📦 Production Build

To create the frontend production build:

cd frontend
npm run build

The production files will be generated inside:

frontend/dist/
▶️ Running the Project
Terminal 1 — Backend
cd CPU-Scheduling-Simulator\backend
.\venv\Scripts\Activate.ps1
python app.py
Terminal 2 — Frontend
cd CPU-Scheduling-Simulator\frontend
npm run dev

Then open the frontend URL shown by Vite, normally:

http://localhost:5173
📄 License

This project is developed for educational and academic purposes.

If you plan to distribute or modify this project publicly, add an appropriate open-source license to the repository.