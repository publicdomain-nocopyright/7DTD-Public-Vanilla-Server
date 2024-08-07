import http.server
import socketserver
import threading
import time
import asyncio
from aiohttp import web
import requests
from concurrent.futures import ThreadPoolExecutor
import statistics

class SlowHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        time.sleep(0.01)  # Simulate some processing time
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, World!")

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

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
async def handle_async(request):
    await asyncio.sleep(0.01)  # Simulate some processing time
    return web.Response(text="Hello, World!")

async def run_async_server(port, stop_event):
    app = web.Application()
    app.router.add_get('/', handle_async)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', port)
    await site.start()
    try:
        while not stop_event.is_set():
            await asyncio.sleep(0.1)
    finally:
        await runner.cleanup()

def make_requests(url, duration):
    start_time = time.time()
    count = 0
    with requests.Session() as session:
        while time.time() - start_time < duration:
            try:
                session.get(url, timeout=1)
                count += 1
            except requests.RequestException:
                pass
    return count

def test_server(server_func, port, duration, num_clients):
    stop_event = threading.Event()
    if asyncio.iscoroutinefunction(server_func):
        async def run_async_wrapper():
            try:
                await server_func(port, stop_event)
            except Exception as e:
                print(f"Async server error: {e}")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server_task = loop.create_task(run_async_wrapper())
        loop.run_until_complete(asyncio.sleep(1))  # Give the server time to start
    else:
        server_thread = threading.Thread(target=server_func, args=(port, stop_event))
        server_thread.start()
        time.sleep(1)  # Give the server time to start

    with ThreadPoolExecutor(max_workers=num_clients) as executor:
        futures = [executor.submit(make_requests, f"http://localhost:{port}", duration) for _ in range(num_clients)]
        total_requests = sum(future.result() for future in futures)

    stop_event.set()
    if asyncio.iscoroutinefunction(server_func):
        loop.run_until_complete(asyncio.sleep(1))  # Give the server time to stop
        server_task.cancel()
        try:
            loop.run_until_complete(server_task)
        except asyncio.CancelledError:
            pass
        loop.close()
    else:
        server_thread.join(timeout=1)

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
    num_clients = 200  # 200 concurrent clients
    num_trials = 5  # 5 trials for each server
    simple_port = 8000
    threaded_port = 8001
    async_port = 8002

    print(f"Testing Simple HTTP Server ({num_trials} trials, {duration} seconds each, {num_clients} concurrent clients)...")
    simple_results = run_test(run_simple_server, simple_port, duration, num_clients, num_trials)

    print(f"\nTesting Threaded HTTP Server ({num_trials} trials, {duration} seconds each, {num_clients} concurrent clients)...")
    threaded_results = run_test(run_threaded_server, threaded_port, duration, num_clients, num_trials)

    print(f"\nTesting Async HTTP Server ({num_trials} trials, {duration} seconds each, {num_clients} concurrent clients)...")
    async_results = run_test(run_async_server, async_port, duration, num_clients, num_trials)

if __name__ == "__main__":
    main()