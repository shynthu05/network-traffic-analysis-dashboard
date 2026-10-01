from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

DATA_FILE = "data/traffic.csv"


def load_data():
    return pd.read_csv(DATA_FILE)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/traffic")
def traffic_data():

    df = load_data()

    total_packets = int(df["packet_count"].sum())
    total_records = len(df)
    total_sources = df["source_ip"].nunique()
    total_destinations = df["destination_ip"].nunique()

    protocol_data = (
        df.groupby("protocol")["packet_count"]
        .sum()
        .reset_index()
    )

    return jsonify({
        "total_packets": total_packets,
        "total_records": total_records,
        "total_sources": total_sources,
        "total_destinations": total_destinations,
        "protocols": protocol_data.to_dict(orient="records"),
        "packets": df.to_dict(orient="records")
    })


if __name__ == "__main__":
    app.run(debug=True)