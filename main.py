from flask import render_template
from flask import Flask, jsonify
import psutil
import os

app = Flask(__name__)

@app.route("/cpu")
def get_cpu():
    cpu = psutil.cpu_percent(interval=1)
    return jsonify({"cpu_usage": cpu})

@app.route("/memory")
def get_memory():
    memory = psutil.virtual_memory()
    return jsonify({"memory_usage": memory.percent})

@app.route("/processes")
def get_processes():
    psutil.cpu_percent(interval=None)  # prime CPU stats
    process_list = []

    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            process_list.append({
                "pid": process.info['pid'],
                "name": process.info['name'],
                "cpu": process.cpu_percent(interval=0.1),
                "memory": round(process.info['memory_percent'], 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return jsonify(process_list)

@app.route("/kill/<int:pid>", methods=["POST"])
def kill_process(pid):
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        return jsonify({"status": "terminated"})
    except:
        return jsonify({"status": "failed"})

@app.route("/")
def dashboard():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
