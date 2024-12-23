from queue import Queue
from collections import deque
from threading import Thread, Lock
import time
import random

class ThreadSafeList:
    def __init__(self):
        self.list = deque()
        self.lock = Lock()
    
    def append(self, item):
        with self.lock:
            self.list.append(item)
    
    def remove(self, item):
        with self.lock:
            try:
                self.list.remove(item)
                return True
            except ValueError:
                return False
    
    def get_all(self):
        with self.lock:
            return list(self.list)

class Producer(Thread):
    def __init__(self, shared_list, name, num_items):
        super().__init__()
        self.shared_list = shared_list
        self.name = name
        self.num_items = num_items
    
    def run(self):
        for i in range(self.num_items):
            item = f"{self.name}-{i}"
            self.shared_list.append(item)
            print(f"{self.name} added: {item}")
            time.sleep(random.uniform(0.1, 0.3))  # Simulate varying processing times

class Consumer(Thread):
    def __init__(self, shared_list, name, items_to_consume):
        super().__init__()
        self.shared_list = shared_list
        self.name = name
        self.items_to_consume = items_to_consume
        self.items_consumed = []
    
    def run(self):
        while len(self.items_consumed) < len(self.items_to_consume):
            current_items = self.shared_list.get_all()
            for item in current_items:
                if item in self.items_to_consume and item not in self.items_consumed:
                    if self.shared_list.remove(item):
                        self.items_consumed.append(item)
                        print(f"{self.name} consumed: {item}")
                        time.sleep(random.uniform(0.1, 0.2))  # Simulate processing
                        break
            time.sleep(0.1)  # Prevent busy waiting

def run_concurrent_test():
    shared_list = ThreadSafeList()
    
    # Create producers
    producer1 = Producer(shared_list, "Producer-1", 5)
    producer2 = Producer(shared_list, "Producer-2", 5)
    
    # Create items for consumers to look for
    items_for_consumer1 = [f"Producer-1-{i}" for i in range(3)]
    items_for_consumer2 = [f"Producer-2-{i}" for i in range(3)]
    
    # Create consumers
    consumer1 = Consumer(shared_list, "Consumer-1", items_for_consumer1)
    consumer2 = Consumer(shared_list, "Consumer-2", items_for_consumer2)
    
    # Start all threads
    print("\nStarting concurrent operations...")
    start_time = time.time()
    
    producer1.start()
    producer2.start()
    consumer1.start()
    consumer2.start()
    
    # Wait for all threads to complete
    producer1.join()
    producer2.join()
    consumer1.join()
    consumer2.join()
    
    end_time = time.time()
    
    # Print results
    print("\nTest Results:")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print(f"Items remaining in list: {shared_list.get_all()}")
    print(f"Consumer-1 items consumed: {consumer1.items_consumed}")
    print(f"Consumer-2 items consumed: {consumer2.items_consumed}")

if __name__ == "__main__":
    run_concurrent_test()