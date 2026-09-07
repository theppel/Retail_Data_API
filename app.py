import os
import csv
import io
from flask import Flask, Response
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def flatten_row(row, parent_key=""):
    flat = {}
    for key, value in row.items():
        new_key = f"{parent_key}{key}" if not parent_key else f"{parent_key}_{key}"
        if isinstance(value, dict):
            flat.update(flatten_row(value, new_key))
        else:
            flat[new_key] = value
    return flat


@app.route("/")
def home():
    return {"message": "Incorrect Route"}


@app.route("/categories")
def export_categories():
    response = supabase.table('categories').select("*").execute()
    data = response.data

    if not data:
        return {"error": "No data found"}

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=categories.csv"}
    )


@app.route("/customers")
def export_customers():
    response = supabase.table('customers').select("*").execute()
    data = response.data

    if not data:
        return {"error": "No data found"}

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=products.csv"}
    )


@app.route("/products")
def export_products():
    response = supabase.table('products').select("*").execute()
    data = response.data

    if not data:
        return {"error": "No data found"}

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=products.csv"}
    )


@app.route("/orders")
def export_orders():
    response = supabase.table('orders').select("*").execute()
    data = response.data

    if not data:
        return {"error": "No data found"}

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=orders.csv"}
    )


@app.route("/details")
def export_details():
    response = supabase.table('order_details').select(
        "*, orders(*, customers(*)), products(*, categories(*))").execute()
    data = response.data

    if not data:
        return {"error": "No data found"}

    flattened = [flatten_row(row) for row in data]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=flattened[0].keys())
    writer.writeheader()
    writer.writerows(flattened)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=details.csv"}
    )


if __name__ == "__main__":
    app.run(debug=True)
