from flask import Flask, jsonify, render_template
import speedtest
import csv
from datetime import datetime

app = Flask(__name__)

def run_speed_test():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000      # Convert to Mbps
    ping = st.results.ping
    wat_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Save the results in CSV
    with open('speed_test_results.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([wat_time, download_speed, upload_speed, ping])

    return download_speed, upload_speed, ping, wat_time

@app.route('/')
def index():
    return render_template('speed_test.html')

@app.route('/run-speed-test')
def speed_test():
    download, upload, ping, wat_time = run_speed_test()
    return jsonify({
        'download': download,
        'upload': upload,
        'ping': ping,
        'time': wat_time
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
