import time

start_time = time.monotonic()
limit = 30

while True:
    if time.monotonic() - start_time >= limit:
        print("time out")
        time.sleep(1)
        break