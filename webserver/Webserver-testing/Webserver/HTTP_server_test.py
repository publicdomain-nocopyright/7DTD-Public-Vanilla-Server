import http.server
import socketserver
import threading
import time
import requests
from concurrent.futures import ThreadPoolExecutor
import statistics

class SlowHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        time.sleep(0.01)  # Simulate some processing time
        return super().do_GET()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

def run_simple_server(port, stop_event):
    with http.server.HTTPServer(("", port), SlowHandler) as httpd:
        httpd.timeout = 0.1
        while not stop_event.is_set():
            httpd.handle_request()

def run_threaded_server(port, stop_event):
    with ThreadedHTTPServer(("", port), SlowHandler) as httpd:
        httpd.timeout = 0.1
        while not stop_event.is_set():
            httpd.handle_request()

def make_requests(url, duration):
    start_time = time.time()
    count = 0
    while time.time() - start_time < duration:
        try:
            requests.get(url, timeout=1)
            count += 1
        except requests.RequestException:
            pass
    return count

def test_server(server_func, port, duration, num_clients):
    stop_event = threading.Event()
    server_thread = threading.Thread(target=server_func, args=(port, stop_event))
    server_thread.start()

    time.sleep(1)  # Give the server time to start

    with ThreadPoolExecutor(max_workers=num_clients) as executor:
        futures = [executor.submit(make_requests, f"http://localhost:{port}", duration) for _ in range(num_clients)]
        total_requests = sum(future.result() for future in futures)

    stop_event.set()
    server_thread.join()

    return total_requests

def run_test(server_func, port, duration, num_clients, num_trials):
    results = []
    for i in range(num_trials):
        requests = test_server(server_func, port, duration, num_clients)
        results.append(requests)
        print(f"Trial {i+1} completed: {requests} requests")
        time.sleep(1)  # Give time for the port to be released
    return results

def main():
    duration = 30  # 30 seconds per trial
    num_clients = 200  # Increased to 200 concurrent clients
    num_trials = 5  # 5 trials for each server
    simple_port = 8000
    threaded_port = 8001

    print(f"Testing Simple HTTP Server ({num_trials} trials, {duration} seconds each, {num_clients} concurrent clients)...")
    simple_results = run_test(run_simple_server, simple_port, duration, num_clients, num_trials)

    print(f"\nTesting Threaded HTTP Server ({num_trials} trials, {duration} seconds each, {num_clients} concurrent clients)...")
    threaded_results = run_test(run_threaded_server, threaded_port, duration, num_clients, num_trials)

    print(f"\nResults:")
    print(f"Simple HTTP Server: {simple_results} requests per trial")
    print(f"Threaded HTTP Server: {threaded_results} requests per trial")

    simple_avg = statistics.mean(simple_results)
    threaded_avg = statistics.mean(threaded_results)

    print(f"\nAverage performance:")
    print(f"Simple HTTP Server: {simple_avg:.2f} requests")
    print(f"Threaded HTTP Server: {threaded_avg:.2f} requests")

    if threaded_avg > simple_avg:
        difference = threaded_avg - simple_avg
        percentage = (difference / simple_avg) * 100
        print(f"\nThe Threaded HTTP Server is faster by {difference:.2f} requests on average ({percentage:.2f}%)")
    elif simple_avg > threaded_avg:
        difference = simple_avg - threaded_avg
        percentage = (difference / threaded_avg) * 100
        print(f"\nThe Simple HTTP Server is faster by {difference:.2f} requests on average ({percentage:.2f}%)")
    else:
        print("\nBoth servers performed equally on average")

if __name__ == "__main__":
    main()