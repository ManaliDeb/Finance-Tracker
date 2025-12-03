from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
from db import get_db, close_db, init_db as _init_db
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='your_secret_key',
        DATABASE=os.path.join(app.instance_path, "finance_tracker.db"),
    )

    # tests may override config if necessary
    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    @app.teardown_appcontext
    def _teardown(exc):
        close_db()

    with app.app_context():
        _init_db()

    # temporary
    register_routes(app)
    return app

def register_routes(app):
    @app.route('/')
    def index():
        if 'username' not in session:
            return redirect(url_for('login'))
        user_id = session['user_id']
        db = get_db()
        transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,)).fetchall()
        total_amount = sum(t['amount'] for t in transactions)
        total_upi = sum(t['amount'] for t in transactions if t['payment_method'] == 'UPI')
        total_cash = sum(t['amount'] for t in transactions if t['payment_method'] == 'Cash')
        return render_template('index.html', username=session['username'],
                               total_amount=total_amount, total_upi=total_upi, total_cash=total_cash)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

            db = get_db()
            user = db.execute(
                "SELECT id, username, password FROM users WHERE username = ?",
                (username,),
            ).fetchone()

            if user and check_password_hash(user[2], password):
                # reset session to avoid fixation, then store identity
                session.clear()
                session['user_id'] = user[0]
                session['username'] = user[1]
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password. Please try again.', 'error')

        return render_template('login.html')


    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']

            db = get_db()
            existing = db.execute(
                "SELECT 1 FROM users WHERE username = ?", (username,)
            ).fetchone()

            if existing:
                flash('Username already exists. Please choose a different one.', 'error')
            else:
                hashed = generate_password_hash(password)  # pbkdf2:sha256 by default
                db.execute(
                "INSERT INTO users (username, email, phone, password) VALUES (?, ?, ?, ?)",
                (username, email, phone, hashed)
                )

        return render_template('register.html')

    @app.route('/transactions')
    def transactions():
        if "username" not in session:
            return redirect(url_for("login"))

        user_id = session["user_id"]
        db = get_db()
        rows = db.execute(
            "SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC, id DESC",
            (user_id,),
        ).fetchall()

        return render_template(
            "transaction.html", transactions=rows, username=session["username"]
        )


    @app.route('/add_transaction', methods=['POST'])
    def add_transaction():
        if "user_id" not in session:
            return redirect(url_for("login"))

        user_id = session["user_id"]
        category = request.form.get("category", "").strip()
        payment_method = request.form.get("payment_method", "").strip()
        description = request.form.get("notes", "").strip()

        # parse & validate amount
        try:
            amount = float(request.form["amount"])
        except (KeyError, TypeError, ValueError):
            flash("Amount must be a valid number.", "error")
            return redirect(url_for("transactions"))

        # date (expect YYYY-MM-DD)
        date = request.form.get("date", "").strip()

        # requested check
        if not category or amount is None:
            flash("Category and amount required", "error")
            return redirect(url_for("transactions"))

        # stricter date validation
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            flash("Date must be in YYYY-MM-DD format.", "error")
            return redirect(url_for("transactions"))

        db = get_db()
        db.execute(
            """
            INSERT INTO transactions (user_id, date, category, amount, payment_method, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, date, category, amount, payment_method, description),
        )
        db.commit()

        flash("Transaction added.", "success")
        return redirect(url_for("transactions"))
    
    @app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
    def delete_transaction(transaction_id):
        if 'username' in session:
            flash("You must be logged in to delete a transaction.", "error")
            return redirect(url_for("login"))

        db = get_db()
        db.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        db.commit()
        flash("Transaction deleted successfully.", "success")
        return redirect(url_for("transactions"))

    @app.route('/daily_spending_data')
    def daily_spending_data():
        if 'username' not in session:
            return redirect(url_for("login"))

        user_id = session["user_id"]
        db = get_db()
        data = db.execute(
            "SELECT date, SUM(amount) AS total FROM transactions WHERE user_id = ? GROUP BY date",
            (user_id,),
        ).fetchall()

        labels = [row["date"] for row in data]
        amounts = [row["total"] for row in data]
        return jsonify({"labels": labels, "amounts": amounts})

    @app.route('/monthly_spending_data')
    def monthly_spending_data():
        if 'username' not in session:
            return redirect(url_for("login"))

        user_id = session["user_id"]
        db = get_db()
        data = db.execute(
            "SELECT strftime('%Y-%m', date) AS month, SUM(amount) AS total "
            "FROM transactions WHERE user_id = ? GROUP BY month",
            (user_id,),
        ).fetchall()

        # keep labels as YYYY-MM for simplicity; format client-side if desired
        labels = [row["month"] for row in data]
        amounts = [row["total"] for row in data]
        return jsonify({"labels": labels, "amounts": amounts})

    @app.route('/statistics')
    def statistics():
        if "user_id" not in session:
            return redirect(url_for("login"))

        user_id = session["user_id"]
        db = get_db()

        total_expenses = db.execute(
            "SELECT COALESCE(SUM(amount), 0) AS total FROM transactions WHERE user_id = ?",
            (user_id,),
        ).fetchone()["total"]

        expense_by_category_rows = db.execute(
            "SELECT category, SUM(amount) AS total FROM transactions "
            "WHERE user_id = ? GROUP BY category",
            (user_id,),
        ).fetchall()
        expense_by_category = {r["category"]: r["total"] for r in expense_by_category_rows}

        top_rows = db.execute(
            "SELECT category, SUM(amount) AS total FROM transactions "
            "WHERE user_id = ? GROUP BY category ORDER BY total DESC LIMIT 5",
            (user_id,),
        ).fetchall()
        top_spending_categories = {r["category"]: r["total"] for r in top_rows}

        return render_template(
            "statistics.html",
            total_expenses=total_expenses,
            expense_by_category=expense_by_category,
            top_spending_categories=top_spending_categories,
        )

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
