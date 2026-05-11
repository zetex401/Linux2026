import hashlib
import itertools
import string
import multiprocessing
import time

TARGET_HASH = "098f6bcd4621d373cade4e832627b4f6"

CHARSET = string.ascii_lowercase
MAX_LEN = 4

def generate_candidates():

    candidates = []

    for length in range(1, MAX_LEN + 1):
        for combo in itertools.product(CHARSET, repeat=length):
            candidates.append(''.join(combo))

    return candidates

def worker(chunk):

    for candidate in chunk:

        if hashlib.md5(candidate.encode()).hexdigest() == TARGET_HASH:
            return candidate

    return None

def brute_force_parallel(num_processes=4):

    start = time.time()

    candidates = generate_candidates()

    chunk_size = len(candidates) // num_processes

    chunks = []

    for i in range(num_processes):

        lo = i * chunk_size

        if i == num_processes - 1:
            hi = len(candidates)
        else:
            hi = (i + 1) * chunk_size

        chunks.append(candidates[lo:hi])

    with multiprocessing.Pool(num_processes) as pool:

        results = pool.map(worker, chunks)

    for r in results:
        if r is not None:

            elapsed = time.time() - start

            print(f"Найдено: {r}")
            print(f"Время multiprocessing: {elapsed:.2f} сек")

            return

brute_force_parallel()
