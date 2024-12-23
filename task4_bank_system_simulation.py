import threading
import random
import time
from datetime import datetime
from queue import Queue

class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
        self.lock = threading.Lock()
        self.transaction_log = Queue()
    
    def get_balance(self):
        with self.lock:
            return self.balance
    
    def deposit(self, amount, client_id):
        with self.lock:
            if amount <= 0:
                return False, "Invalid deposit amount"
            
            initial_balance = self.balance
            self.balance += amount
            
            transaction = {
                'client_id': client_id,
                'type': 'deposit',
                'amount': amount,
                'initial_balance': initial_balance,
                'final_balance': self.balance,
                'timestamp': datetime.now(),
                'status': 'success'
            }
            self.transaction_log.put(transaction)
            return True, f"Deposited ${amount:.2f}"

    def withdraw(self, amount, client_id):
        with self.lock:
            if amount <= 0:
                return False, "Invalid withdrawal amount"
            
            initial_balance = self.balance
            if self.balance < amount:
                transaction = {
                    'client_id': client_id,
                    'type': 'withdrawal',
                    'amount': amount,
                    'initial_balance': initial_balance,
                    'final_balance': initial_balance,
                    'timestamp': datetime.now(),
                    'status': 'failed',
                    'reason': 'insufficient funds'
                }
                self.transaction_log.put(transaction)
                return False, "Insufficient funds"
            
            self.balance -= amount
            transaction = {
                'client_id': client_id,
                'type': 'withdrawal',
                'amount': amount,
                'initial_balance': initial_balance,
                'final_balance': self.balance,
                'timestamp': datetime.now(),
                'status': 'success'
            }
            self.transaction_log.put(transaction)
            return True, f"Withdrew ${amount:.2f}"

class BankClient(threading.Thread):
    def __init__(self, account, client_id, num_transactions):
        super().__init__()
        self.account = account
        self.client_id = f"Client-{client_id}"
        self.num_transactions = num_transactions
        self.successful_transactions = 0
        self.failed_transactions = 0
    
    def run(self):
        for _ in range(self.num_transactions):
            # Randomly choose between deposit and withdrawal
            if random.random() < 0.5:
                amount = random.randint(1, 1000)
                success, message = self.account.deposit(amount, self.client_id)
            else:
                amount = random.randint(1, 500)
                success, message = self.account.withdraw(amount, self.client_id)
            
            if success:
                self.successful_transactions += 1
            else:
                self.failed_transactions += 1
            
            print(f"{self.client_id}: {message}")
            time.sleep(random.uniform(0.1, 0.3))  # Simulate processing time

def print_transaction_summary(account, clients):
    print("\nTransaction Summary:")
    print(f"Final Balance: ${account.get_balance():.2f}")
    
    print("\nClient Statistics:")
    for client in clients:
        print(f"{client.client_id}:")
        print(f"  Successful transactions: {client.successful_transactions}")
        print(f"  Failed transactions: {client.failed_transactions}")
    
    print("\nTransaction Log:")
    while not account.transaction_log.empty():
        transaction = account.transaction_log.get()
        print(f"\n{transaction['timestamp']} - {transaction['client_id']}:")
        print(f"  Type: {transaction['type']}")
        print(f"  Amount: ${transaction['amount']:.2f}")
        print(f"  Status: {transaction['status']}")
        print(f"  Balance: ${transaction['initial_balance']:.2f} -> ${transaction['final_balance']:.2f}")

def main():
    # Initialize bank account with $1000
    account = BankAccount(1000)
    
    # Create multiple clients
    num_clients = 3
    transactions_per_client = 5
    clients = [BankClient(account, i+1, transactions_per_client) 
              for i in range(num_clients)]
    
    # Start all clients
    print("Starting bank transaction simulation...")
    start_time = time.time()
    
    for client in clients:
        client.start()
    
    # Wait for all clients to complete
    for client in clients:
        client.join()
    
    end_time = time.time()
    
    # Print summary
    print(f"\nSimulation completed in {end_time - start_time:.2f} seconds")
    print_transaction_summary(account, clients)

if __name__ == "__main__":
    main()