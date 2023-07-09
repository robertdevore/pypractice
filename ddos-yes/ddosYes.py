import requests
import threading
import time
import csv
import sys

target_url = "http://example.com/wp-content/admin-ajax.php"
num_requests = 100
max_concurrent_requests = 10
timeout = 10
csv_filename = "request_details.csv"

# Shared variables for tracking requests
completed_requests = 0
failed_requests = 0
start_time = None

# Lock for thread-safe writing to the CSV file
csv_lock = threading.Lock()

# Function to send HTTP requests and track results
def send_request(url, thread_num):
    global completed_requests, failed_requests, start_time

    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            completed_requests += 1
        else:
            failed_requests += 1
            print(f"Failed request - Thread #{thread_num} - URL: {url}")
            write_to_csv(thread_num, url, str(response.content))
    except requests.exceptions.RequestException:
        failed_requests += 1
        print(f"Failed request - Thread #{thread_num} - URL: {url}")
        write_to_csv(thread_num, url, str(response.content))

    # Check if all requests are completed
    if completed_requests + failed_requests == num_requests:
        elapsed_time = time.time() - start_time
        print("[+] Test complete.")
        print(f"[-] Total requests sent: {num_requests}")
        print(f"[-] Completed requests: {completed_requests}")
        print(f"[-] Failed requests: {failed_requests}")
        print(f"[-] Time taken: {elapsed_time:.2f} seconds")

# Function to write details to the CSV file
def write_to_csv(thread_num, url, response_data):
    with csv_lock:
        with open(csv_filename, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([thread_num, url, response_data])

try:
    # Start the test
    print(f"Sending {num_requests} requests to {target_url}...")
    print(f"Max concurrent requests: {max_concurrent_requests}")
    print(f"Saving details to CSV file: {csv_filename}")
    print("Press Ctrl+C to stop the test.")

    # Create and start threads for sending requests
    threads = []
    start_time = time.time()

    for i in range(num_requests):
        t = threading.Thread(target=send_request, args=(target_url, i + 1))
        threads.append(t)
        print(f"Thread #{i + 1} opened.")
        t.start()
        # Limit the number of concurrent requests
        if len(threads) >= max_concurrent_requests:
            # Wait for the oldest thread to complete before starting a new one
            threads[0].join()
            del threads[0]

    # Wait for all threads to finish
    for t in threads:
        t.join()

except KeyboardInterrupt:
    elapsed_time = time.time() - start_time
    print("\n[x] Test interrupted by user.")
    print(f"[-] Total requests sent: {num_requests}")
    print(f"[-] Completed requests: {completed_requests}")
    print(f"[-] Failed requests: {failed_requests}")
    print(f"[-] Time taken: {elapsed_time:.2f} seconds")
    sys.exit(0)
