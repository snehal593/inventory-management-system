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


