import os
import json
import random
from flask import Flask, render_template, request

app = Flask(__name__)

DATA_FILE = os.path.join(app.static_folder, "data", "allocations.json")

def load_allocations():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            return []
    return []

def save_allocations(allocations):
    with open(DATA_FILE, "w") as f:
        json.dump(allocations, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    allocation = None
    wallet = ""
    x_handle = ""
    leaderboard = []

    allocations = load_allocations()

    if request.method == "POST":
        wallet = request.form.get("wallet", "").strip()
        x_handle = request.form.get("x_handle", "").strip().lstrip("@")

        # Check if this user already exists in allocations
        existing_user = next(
            (user for user in allocations if user["wallet"].lower() == wallet.lower() and user["x_handle"].lower() == x_handle.lower()),
            None,
        )

        if existing_user:
            allocation = existing_user["allocation"]
        else:
            allocation = random.randint(1000, 10000)
            allocations.append({
                "wallet": wallet,
                "x_handle": x_handle,
                "allocation": allocation
            })
            save_allocations(allocations)

    # Sort leaderboard by allocation descending
    leaderboard = sorted(allocations, key=lambda x: x["allocation"], reverse=True)

    return render_template(
        "index.html",
        allocation=allocation,
        wallet=wallet,
        x_handle=x_handle,
        leaderboard=leaderboard,
    )

if __name__ == "__main__":
    app.run(debug=True)
