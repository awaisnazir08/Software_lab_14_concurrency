import threading
import time

class NumberPrinter(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def run(self):
        print(f"\nStarting {self.name}")
        for i in range(1, 11):
            if self.name == "Number Thread":
                print(f"{self.name}: {i}")
            else:
                print(f"{self.name}: {i * i}")
            time.sleep(0.5)  # Small delay to better demonstrate concurrent execution
        print(f"Finished {self.name}")

def main():
    # Create thread instances
    number_thread = NumberPrinter("Number Thread")
    square_thread = NumberPrinter("Square Thread")
    
    # Start both threads
    print("Starting threads...")
    number_thread.start()
    square_thread.start()
    
    # Wait for both threads to complete
    number_thread.join()
    square_thread.join()
    
    print("\nAll threads completed!")

if __name__ == "__main__":
    main()