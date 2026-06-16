# Sonkamble Enterprise POS & Algorithmic Procurement Engine

## 📖 Overview
A cloud-hosted, real-time retail ecosystem designed to modernize local business operations. This project features a dual Progressive Web App (PWA) architecture, a zero-fee programmatic UPI payment infrastructure, and a machine learning-inspired procurement optimization engine powered by Particle Swarm Optimization (PSO). It bridges the gap between high-speed counter billing and advanced business intelligence.

## ⚠️ The Problem Statement
When I had to temporarily manage my father's small retail shop, I quickly encountered the "micro-retail bottleneck": operating a physical business purely on intuition. I identified three major engineering challenges:

**1.Capital Inefficiency:** Ordering based on "gut feeling" wastes limited budgets on slow-moving stock, while high-profit items constantly sell out.

**2.Data Opacity:** No localized system existed to track real-time sales velocity or item-specific Return on Investment (ROI).

**3.Hardware Constraints:** Small shop counters cannot support bulky, expensive desktop POS systems.

**The Solution:** This ecosystem isolates the counter-billing (Shop POS) from the management dashboard (Admin PWA) while keeping them perfectly synced via WebSockets. Furthermore, it replaces "guessing" with a PSO algorithm that calculates the exact amount of stock to buy for maximum Return on Investment (ROI).

## 💻 Tech Stack
* **Backend Framework:** Python, Flask
* **Real-Time Engine:** WebSockets (Flask-SocketIO)
* **Database:** SQLite3 (ACID-compliant relational design)
* **Frontend UI:** Tailwind CSS, Vanilla JS (ES6+), HTML5
* **Data Visualization:** Chart.js
* **Algorithmic Engine:** NumPy, Pandas

## 🏗️ System Architecture
The application runs on a centralized Flask core, utilizing the principle of **Separation of Concerns**. It exposes RESTful endpoints for state changes and WebSocket gateways for zero-latency synchronization between two separate frontends.

## 🏗️ System Architecture
The application runs on a centralized Flask core, utilizing the principle of **Separation of Concerns**. It exposes RESTful endpoints for state changes and WebSocket gateways for zero-latency synchronization between two separate frontends.

```text
                                  +---------------------------------------+
                                  |         Flask Cloud Backend           |
                                  |     (PythonAnywhere / SQLite3)        |
                                  +---+-------------------------------+---+
                                      |                               |
                   REST APIs / JSON   |                               |  REST APIs / JSON
                                      v                               v
                        +-------------+-------------+   +-------------+-------------+
                        |      Admin Dashboard      |   |       Shop Store POS      |
                        |  (PWA - Desktop/Mobile)   |   |  (PWA - Desktop/Mobile)   |
                        +-------------+-------------+   +-------------+-------------+
                                      |                               ^
                                      |                               |
                                      +------- WebSockets Sync -------+
                                              (Zero-Latency Updates)
```
## ⚙️ Installation & Setup (Local Development)

Follow these exact steps to run the complete dual-PWA ecosystem on your local machine.

### Prerequisites
* Python 3.8+ installed on your machine.
* Git installed.

### Step 1: Clone the Repository
Open your terminal or command prompt and run:
bash
git clone https://github.com/snehal533/inventory-management-system.git
cd inventory-management-system


### Step 2: Create & Activate a Virtual Environment
It is highly recommended to isolate the project dependencies to prevent conflicts.

**On Windows:**
bash
python -m venv venv
venv\Scripts\activate


**On macOS/Linux:**
bash
python3 -m venv venv
source venv/bin/activate


### Step 3: Install Dependencies
Install the required Python libraries using the `requirements.txt` file:
bash
pip install -r requirements.txt


### Step 4: Configure Environment Variables
Create a new file named `.env` in the root directory of the project. Add your secret key for Flask session security:
text
SECRET_KEY=your_super_secret_key_here


### Step 5: Initialize and Run the Server
The application features auto-initialization. When you run it for the first time, it will automatically generate the `business.db` SQLite database and populate it with the default inventory algorithm parameters.
bash
python app.py


### Step 6: Access the Ecosystem
Once the local server is running, open your web browser and navigate to:
* **Admin Dashboard (Management & PSO Engine):** `http://127.0.0.1:5000/`
* **Shop POS Terminal (Counter Billing):** `http://127.0.0.1:5000/store`

*(Note for local development: The system automatically provisions a test admin account. You can log in using Username: `admin`, Password: `admin123`. For production deployments, ensure you override this by setting the `ADMIN_PASSWORD` variable in your `.env` file).*


