from threading import Thread
from time import sleep


def func(*args, **kwargs):
    thread_number = i
    print(f"thread {thread_number} start")
    sleep(1)
    print(f"thread {thread_number} end")


if __name__ == "__main__":
    count = 20
    threads = []
    for i in range(count):
        thread = Thread(target=func, args=[])
        threads.append(thread)
        thread.start()

    for i in range(count):
        thread: Thread = threads[i]
        thread.join(4.0)

    print("finished")
