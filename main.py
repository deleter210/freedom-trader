import time
from trader import execute_trade

def main():
    while True:
        execute_trade()
        time.sleep(60)  # Wait for 1 minute before checking again

if __name__ == "__main__":
    main()
