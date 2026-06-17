# Imventory Management System - PSO Algorithm

## 1.Overview
A cloud-hosted, real-time retail ecosystem designed to modernize local business operations. This project features a dual Progressive Web App (PWA) architecture, a zero-fee programmatic UPI payment infrastructure, and a machine learning-inspired procurement optimization engine powered by Particle Swarm Optimization (PSO). It bridges the gap between high-speed counter billing and advanced business intelligence.

## 2.The Problem Statement
When I had to temporarily manage my father's small retail shop, I quickly encountered the "micro-retail bottleneck": operating a physical business purely on intuition. I identified three major engineering challenges:

**1.Capital Inefficiency:** Ordering based on "gut feeling" wastes limited budgets on slow-moving stock, while high-profit items constantly sell out.

**2.Data Opacity:** No localized system existed to track real-time sales velocity or item-specific Return on Investment (ROI).

**3.Hardware Constraints:** Small shop counters cannot support bulky, expensive desktop POS systems.

**The Solution:** This ecosystem isolates the counter-billing (Shop POS) from the management dashboard (Admin PWA) while keeping them perfectly synced via WebSockets. Furthermore, it replaces "guessing" with a PSO algorithm that calculates the exact amount of stock to buy for maximum Return on Investment (ROI).

## 3.Tech Stack
* **Backend Framework:** Python, Flask
* **Real-Time Engine:** WebSockets (Flask-SocketIO)
* **Database:** SQLite3 (ACID-compliant relational design)
* **Frontend UI:** Tailwind CSS, Vanilla JS (ES6+), HTML5
* **Data Visualization:** Chart.js
* **Algorithmic Engine:** NumPy, Pandas

## 4.System Architecture
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
## 5.Installation & Setup (Local Development)

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


## 6.The Optimization Algorithm (Particle Swarm Optimization)
Instead of relying on basic inventory thresholds or arbitrary reorder points, the backend features a custom deterministic model that calculates the mathematically optimal purchase order for every single stock item. 

The engine simulates a multi-dimensional search space where $100$ individual "particles" (candidate inventory strategies) evaluate potential purchasing combinations over $500$ iterations.

* **The Objective Function:** The swarm minimizes capital expenditure while simultaneously maximizing profit margin velocity. The cost function evaluated at every iteration is mathematically defined as:

$$\text{Cost Function} = \frac{(\text{Total Cost} \times \text{Days to Depletion}) + 0.1}{(\text{Total Predicted Profit})^2 + 0.01}$$

* **Position Update Heuristic:** Particles dynamically adjust their trajectories based on their personal historical best position ($p_{best}$) and the global swarm's best known position ($g_{best}$), driven by cognitive ($w_1 = 1.5$) and social ($w_2 = 1.5$) acceleration constants:

$$V_{t+1} = w_1(g_{best} - X_t) + w_2(p_{best} - X_t) + \text{rand}()$$

* **Real-World Business Output:** The mathematical minimum discovered by the swarm is parsed directly into a readable "Restock Business Plan," telling the owner the exact unit counts to buy to maximize Return on Investment (ROI) without exceeding their budget.



## 7.Frontend & Backend Pipeline (How Data Flows)
The ecosystem completely abandons standard HTTP polling, ensuring that changes at the physical shop counter instantly reflect on the manager's dashboard without a page refresh.

* **The Transaction Flow:** 1. The **Shop POS Frontend** processes a sale and updates its local cart state using optimized JavaScript event listeners.
  2. Upon checkout, the cart array is stringified into a JSON payload and transmitted via an asynchronous REST `POST` request to the Flask server.
  3. The **Flask Backend** accepts the payload, opens an atomic database connection, and executes ACID-compliant SQL queries to safely decrement stock counts.
* **The Real-Time Sync:** 1. Immediately following the database commit, the server triggers a WebSocket broadcast event (`new_order`) via `Flask-SocketIO`.
  2. The **Admin Dashboard Frontend**, maintaining a persistent full-duplex WebSocket link, intercepts the payload in real-time.
  3. A JavaScript callback catches the data, dynamically mutates the DOM, re-renders the Chart.js business analytics canvas, and triggers a real-time auditory alert.


## 8.Outputs & Results
*Below are live screenshots demonstrating the operational dual-PWA architecture and real-time backend updates.*

#### 1. Admin Analytics & Inventory Management Dashboard
<img width="1913" height="873" alt="Screenshot 2026-06-16 204708" src="https://github.com/user-attachments/assets/aefc1180-befa-4e4d-bba7-0a69993fbca8" />


#### 2. Mobile-First Shop POS Counter Billing Interface
<img width="1895" height="961" alt="Screenshot 2026-06-16 205252" src="https://github.com/user-attachments/assets/c8dfea61-546e-46c6-a16c-d249f849336b" />


#### 3. Dynamic UPI Payment QR Code Modal Generation
<img width="1862" height="962" alt="Screenshot 2026-06-16 205400" src="https://github.com/user-attachments/assets/630ef388-bd32-4dc4-8a18-75369e0fee57" />

---
## 9.Conclusion
This project represents more than just a web application; it is a scalable engineering solution to a socio-economic bottleneck. By applying deterministic mathematical algorithms (PSO) and modern web architecture (Dual-PWAs, WebSockets) to traditional micro-retail, it completely eliminates the guesswork of inventory management. It proves that enterprise-grade business intelligence can be deployed efficiently and affordably to small business owners on low-power devices.

## 10.Live App Link: https://bhimrao.pythonanywhere.com/






