from flask import Flask, render_template, request, jsonify, session, redirect, url_for,send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import numpy as np
import pandas as pd
import datetime
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit

load_dotenv() # Loads variables from .env

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app.secret_key = os.environ.get('SECRET_KEY') 
DB_NAME = 'business.db'

# ==========================================
# DATABASE SETUP
# ==========================================
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        selling_price REAL,
                        bulk_cp REAL,
                        qty REAL,
                        E REAL,
                        F REAL,
                        current_stock INTEGER DEFAULT 0,
                        category TEXT DEFAULT 'General',
                        image_file TEXT DEFAULT 'default.png')''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_name TEXT,
                        action_type TEXT,
                        quantity INTEGER,
                        upi_id TEXT DEFAULT 'None',
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        hashed_pw = generate_password_hash('LALITHA15!')
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ('admin', hashed_pw))
    
    cursor.execute("SELECT COUNT(*) FROM items")
    if cursor.fetchone()[0] == 0:
        X_units = {
            "Thums Up":[20, 470, 28, 180,7], "Sprite":[20, 470, 28, 180,7],
            "Sting":[20, 510, 30, 90,7], "Limca":[20, 470, 28, 180,6],
            "Maaza":[20, 550, 30, 120,3], "Dew":[20, 510, 30, 120,7],
            "pulpy orange":[25, 650, 30, 90,3], "Appy Fizz":[ 10, 340, 40, 180,3],
            "Mom's Magic": [5, 775, 180, 240,24], "Good Day":[5, 800, 180, 240,24],
            "Parle":[ 5, 645, 144, 180,12], "Marie Gold":[ 5, 700, 150, 180,10],
            "Happy Happy": [5, 220, 48, 120,3], "Cream Biscuits":[ 5, 220, 48, 120,3],
            "Kings":[25, 240, 10, 365,10], "Lights" :[25, 220, 10, 365,10],
            "Small Gold":[12, 115, 10, 365,5], "Small Advance":[ 12, 115, 10, 365,6],
            "Millies": [25, 440, 20, 365,7], "Charms":[ 10, 80, 10, 365,10],
            "Bristol":[10, 80, 10, 365,6], "Malabar":[ 20, 104, 10, 15,6],
            "Connect":[20, 360, 20, 365,20], "Silk":[20, 290, 16, 300,8],
            "American": [20, 190, 10, 365,27], "Small Malbar":[ 12, 230, 20, 365,20]
        }
        for name, data in X_units.items():
            # 1. Auto-generate the image name (e.g., thumsup.png)
            auto_image_name = name.lower().replace(" ", "").replace("'", "") + ".png"
            
            # 2. Auto-assign the Category
            if name in ["Thums Up", "Sprite", "Sting", "Limca", "Maaza", "Dew", "Pulpy orange", "Appy Fizz"]:
                category = "Cool Drinks"
            elif name in ["Mom's Magic", "Good Day", "Parle", "Marie Gold", "Happy Happy", "Cream Biscuits"]:
                category = "Biscuits"
            elif name in ["Kings", "Lights", "Small Gold", "Small Advance", "Millies", "Charms","Silk", "Bristol", "Malabar", "Connect", "American", "Small Malbar"]:
                category = "Cigarettes"
            else:
                category = "General"
            
            # 3. Save EVERYTHING (including category) into the database
            cursor.execute('''INSERT INTO items (name, selling_price, bulk_cp, qty, E, F, image_file, category) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                           (name, data[0], data[1], data[2], data[3], data[4], auto_image_name, category))
    
    conn.commit()
    conn.close()

init_db()

def load_math_data():
    conn = get_db()
    items = conn.execute("SELECT * FROM items").fetchall()
    conn.close()
    
    names = [row['name'] for row in items]
    sp = np.array([row['selling_price'] for row in items])
    bulk_cp = np.array([row['bulk_cp'] for row in items])
    qty = np.array([row['qty'] for row in items])
    E = np.array([row['E'] for row in items])
    F = np.array([row['F'] for row in items])
    
    C = bulk_cp / qty
    PM = sp - C
    max_limit = np.multiply(F, E)
    return names, sp, C, PM, F, max_limit

# ==========================================
# ROUTES: AUTHENTICATION & DASHBOARD
# ==========================================

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/sw.js')
def serve_sw():
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('index.html')

# ==========================================
# ROUTES: INVENTORY, METRICS & TRANSACTIONS
# ==========================================
@app.route('/system_restart',methods=['GET','POST'])
def systemrestart():
    if 'user_id' not in session:
        return jsonify({"error":"unauthorized"}) , 401
    
    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("DROP TABLE IF EXISTS items")
    cursor.execute("DROP TABLE IF EXISTS users")
    conn.commit()
    conn.close()

    init_db()
    session.clear()
    return jsonify({"status":"success"})
    
@app.route('/api/metrics')
def metrics():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. FIXED TOTAL INVESTMENT: current_stock * (bulk_cp / qty)
    cursor.execute("""
        SELECT SUM(current_stock * (bulk_cp / qty)) as total_inv 
        FROM items 
        WHERE qty > 0
    """)
    inv_result = cursor.fetchone()['total_inv']
    investment = round(inv_result, 2) if inv_result else 0.00
    
    # 2. FIXED TOTAL PROFIT: quantity_sold * (selling_price - (bulk_cp / qty))
    cursor.execute("""
        SELECT SUM(t.quantity * (i.selling_price - (i.bulk_cp / i.qty))) as tot_profit
        FROM transactions t
        JOIN items i ON t.item_name = i.name
        WHERE t.action_type = 'sell' AND i.qty > 0
    """)
    tp_result = cursor.fetchone()['tot_profit']
    total_profit = round(tp_result, 2) if tp_result else 0.00

    # 3. FIXED WEEKLY PROFIT: Same logic, but filtered for last 7 days
    cursor.execute("""
        SELECT SUM(t.quantity * (i.selling_price - (i.bulk_cp / i.qty))) as wk_profit
        FROM transactions t
        JOIN items i ON t.item_name = i.name
        WHERE t.action_type = 'sell' 
        AND t.timestamp >= datetime('now', '-7 days')
        AND i.qty > 0
    """)
    wk_result = cursor.fetchone()['wk_profit']
    weekly_profit = round(wk_result, 2) if wk_result else 0.00

    # 4. Empty Stock Alerts (Optional, if you kept it in the UI)
    cursor.execute("SELECT COUNT(*) as low_stock FROM items WHERE current_stock = 0")
    ls_result = cursor.fetchone()['low_stock']
    low_stock = int(ls_result) if ls_result else 0

    conn.close()
    
    return jsonify({
        "investment": investment,
        "weekly_profit": weekly_profit,
        "total_profit": total_profit,
        "low_stock": low_stock
    })

@app.route('/api/inventory')
def get_inventory():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    conn = get_db()
    items = conn.execute("SELECT id, name, current_stock, selling_price FROM items").fetchall()
    conn.close()
    return jsonify([dict(item) for item in items])

@app.route('/api/transactions')
def get_transactions():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    conn = get_db()
    logs = conn.execute("SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 50").fetchall()
    conn.close()
    return jsonify([dict(log) for log in logs])

@app.route('/api/update_stock', methods=['POST'])
def update_stock():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    item_name, action, qty = data['item_name'], data['action'], int(data['qty'])
    
    conn = get_db()
    cursor = conn.cursor()
    
    if action == 'buy':
        cursor.execute("UPDATE items SET current_stock = current_stock + ? WHERE name = ?", (qty, item_name))
    elif action == 'sell':
        cursor.execute("UPDATE items SET current_stock = MAX(0, current_stock - ?) WHERE name = ?", (qty, item_name))
        
    cursor.execute("INSERT INTO transactions (item_name, action_type, quantity) VALUES (?, ?, ?)", (item_name, action, qty))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/api/edit_stock', methods=['POST'])
def edit_stock():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    item_name = data['item_name']
    new_stock = int(data['new_stock'])
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT current_stock FROM items WHERE name = ?", (item_name,))
    old_stock = cursor.fetchone()['current_stock']
    diff = new_stock - old_stock
    
    if diff != 0:
        # UPDATED: Changed the terminology to be business-accurate
        action = 'restock' if diff > 0 else 'stock_correction'
        
        cursor.execute("UPDATE items SET current_stock = ? WHERE name = ?", (new_stock, item_name))
        # Use abs(diff) so it logs the exact amount you bought/lost
        cursor.execute("INSERT INTO transactions (item_name, action_type, quantity) VALUES (?, ?, ?)", (item_name, action, abs(diff)))
        
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})


# ==========================================
# ROUTE: PSO LOGIC
# ==========================================

@app.route('/api/inventory_stats')
def inventory_stats():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    
    # Get the days from the slider (default is 7)
    days = int(request.args.get('days', 7))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Fetch items and calculate TOTAL SOLD in the requested time frame, sorted highest to lowest
    query = """
        SELECT 
            i.name, i.current_stock, i.selling_price,
            COALESCE(SUM(t.quantity), 0) as total_sold
        FROM items i
        LEFT JOIN transactions t 
            ON i.name = t.item_name 
            AND t.action_type = 'sell' 
            AND t.timestamp >= datetime('now', ?)
        GROUP BY i.name
        ORDER BY total_sold DESC, i.current_stock DESC
    """
    cursor.execute(query, (f'-{days} days',))
    items_data = [dict(row) for row in cursor.fetchall()]
    
    # 2. Fetch daily sales breakdown for the Accordion Graph
    cursor.execute("""
        SELECT item_name, date(timestamp) as sell_date, SUM(quantity) as daily_sold
        FROM transactions
        WHERE action_type = 'sell' AND timestamp >= datetime('now', ?)
        GROUP BY item_name, date(timestamp)
    """, (f'-{days} days',))
    
    chart_data = {}
    for row in cursor.fetchall():
        name = row['item_name']
        if name not in chart_data: chart_data[name] = {}
        chart_data[name][row['sell_date']] = row['daily_sold']
        
    conn.close()
    
    return jsonify({
        "items": items_data,
        "chart_data": chart_data
    })

@app.route('/api/get_pso_data')
def get_pso_data():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    names, sp, C, PM, F, max_limit = load_math_data()
    
    num_particles = 100; max_iterations = 500; w1 = 1.5; w2 = 1.5                
    num_dimensions = len(names)
    particles_position = np.random.uniform(0, max_limit, (num_particles, num_dimensions))
    pbest_position = particles_position.copy()      
    pbest_score = np.zeros(num_particles)    
    gbest_position = np.zeros(num_dimensions)       
    gbest_score = 0.0                                
    
    graph_points = []; flat_counter = 0 

    for i in range(max_iterations):
        for p in range(num_particles):
            T = particles_position[p]
            total_cost, total_profit = np.dot(T, C), np.dot(T, PM)
            if total_profit > 0:
                days = np.max(T / F)
                cost_function = (total_cost * days + 0.1) / (total_profit * total_profit + 0.01)
            else:
                cost_function = 99999.0 
            
            if i == 0 or cost_function < pbest_score[p]:
                pbest_score[p], pbest_position[p] = cost_function, T.copy()
            if i == 0 or cost_function < gbest_score:
                gbest_score, gbest_position = cost_function, T.copy()

        graph_points.append({"iteration": i, "value": round(gbest_score, 4)})
        for p in range(num_particles):
            dx = (w1 * (gbest_position - particles_position[p])) + (w2 * (pbest_position[p] - particles_position[p])) + np.random.rand(num_dimensions)
            particles_position[p] = np.clip(particles_position[p] + dx, 0, max_limit)

        if i > 0 and graph_points[-1]["value"] == graph_points[-2]["value"]: flat_counter += 1
        else: flat_counter = 0
        if flat_counter == 20: break

    business_plan = []
    for v in range(len(names)):
        final_units = int(np.round(F[v]*7))
        final_cost, final_profit = final_units * C[v], final_units * PM[v]
        roi = ((final_profit / final_cost) * 100) if final_cost > 0 else 0
        business_plan.append({"item": names[v], "units": final_units, "roi": round(roi, 2)})

    return jsonify({"optimization_history": graph_points, "business_plan": business_plan})

# ==========================================
# ROUTES: CUSTOMER STOREFRONT (PUBLIC)
# ==========================================
import json

@app.route('/store')
def store():
    conn = get_db()
    # Fetch all items and sort them by Category
    items = conn.execute("SELECT * FROM items ORDER BY category, name").fetchall()
    conn.close()

    # Group items into a dictionary so HTML can display them under headers
    # Group items into a dictionary so HTML can display them under headers
    store_items = {}
    for item in items:
        cat = item['category']
        if cat not in store_items:
            store_items[cat] = []
        store_items[cat].append(dict(item))

    return render_template('store.html', store_items=store_items)

@app.route('/process_order', methods=['POST'])
def process_order():
    cart_data = request.form.get('cart_data')
    if not cart_data:
        return redirect(url_for('store'))

    items = json.loads(cart_data)

    order_summary = {}
    grand_total = 0
    for item in items:
        name = item['name']
        price = item['price']
        order_summary[name] = order_summary.get(name, 0) + 1
        grand_total += price

    conn = get_db()
    cursor = conn.cursor()

    # Deduct stock and save to database (No manual UPI ID needed anymore)
    for name, qty in order_summary.items():
        cursor.execute("UPDATE items SET current_stock = MAX(0, current_stock - ?) WHERE name = ?", (qty, name))
        cursor.execute("INSERT INTO transactions (item_name, action_type, quantity) VALUES (?, 'sell', ?)", (name, qty))

    conn.commit()
    conn.close()

    # BROADCAST TO ADMIN DASHBOARD
    order_details = {
        "items": order_summary,
        "total": grand_total,
        "time": datetime.datetime.now().strftime("%I:%M %p")
    }
    socketio.emit('new_order', order_details)

    return f"""
        <div style='text-align:center; font-family:Arial; padding:50px;'>
            <h1 style='color:green;'>Order Confirmed!</h1>
            <h2>Total Paid: ₹{grand_total}</h2>
            <p>The shop owner has been notified. Please collect your items.</p>
            <br><br>
            <a href='/store' style='padding:15px; background:#3498db; color:white; text-decoration:none; border-radius:5px;'>Return to Store</a>
        </div>
    """

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)