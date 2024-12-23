import threading
import time

class Counter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()  # Create a lock for synchronization
    
    def increment_unsync(self):
        """Increment counter without synchronization"""
        current = self.count
        time.sleep(0.0001)  # Simulate some processing time
        self.count = current + 1
    
    def increment_sync(self):
        """Increment counter with synchronization"""
        with self.lock:  # Use context manager for automatic lock release
            current = self.count
            time.sleep(0.0001)  # Simulate some processing time
            self.count = current + 1

class WorkerThread(threading.Thread):
    def __init__(self, counter, synchronized, name):
        super().__init__()
        self.counter = counter
        self.synchronized = synchronized
        self.name = name
    
    def run(self):
        print(f"Starting {self.name}")
        for _ in range(100):
            if self.synchronized:
                self.counter.increment_sync()
            else:
                self.counter.increment_unsync()
        print(f"Finished {self.name}")

def run_counter_test(synchronized):
    counter = Counter()
    threads = []
    
    # Create three threads
    for i in range(3):
        thread = WorkerThread(counter, synchronized, f"Thread-{i+1}")
        threads.append(thread)
    
    # Start all threads
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    
    print(f"\n{'Synchronized' if synchronized else 'Unsynchronized'} Counter Test:")
    print(f"Final counter value: {counter.count}")
    print(f"Expected value: 300")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print("Result: {}".format("✓ Correct" if counter.count == 300 else "✗ Race condition detected"))

def main():
    print("Starting Thread Synchronization Demo\n")
    
    # Run unsynchronized test
    run_counter_test(synchronized=False)
    
    # Run synchronized test
    run_counter_test(synchronized=True)

if __name__ == "__main__":
    main()