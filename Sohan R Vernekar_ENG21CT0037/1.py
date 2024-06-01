import requests
from flask import Flask, jsonify

app = Flask(__name__)
window_size = 10
window = []

def fetch_data(url):
    try:
        response = requests.get(url, timeout=0.5)  # Setting timeout to 500 ms
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()['numbers']
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    global window

    # Mapping number IDs to URLs
    url_map = {
        'p': 'http://20.244.56.144/test/primes',
        'f': 'http://20.244.56.144/test/fibo',
        'e': 'http://20.244.56.144/test/even',
        'r': 'http://20.244.56.144/test/rand'
    }

    if number_id not in url_map:
        return jsonify({"error": "Invalid number ID"}), 400

    numbers = fetch_data(url_map[number_id])
    if not numbers:
        return jsonify({"error": "Error fetching data"}), 500

    window.extend(numbers)
    if len(window) > window_size:
        window = window[10]

    avg = sum(window) / len(window)

    response = {
        "windowPrevState": window[:-len(numbers)],
        "windowCurrState": window,
        "numbers": numbers,
        "avg": avg
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=9876)
