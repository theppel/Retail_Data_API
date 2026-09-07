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


@app.route("/")
def home():
    return {"message": "Incorrect Route"}


@app.route("/categories")
def export_csv():
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
        headers={"Content-Disposition": "attachment;filename=export.csv"}
    )


if __name__ == "__main__":
    app.run(debug=True)
