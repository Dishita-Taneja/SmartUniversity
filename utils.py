# Utility functions: decorators, generators, recursion, lambda

# --- Decorator Example ---
def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} returned {result}")
        return result
    return wrapper

# --- Generator Example ---
def student_id_generator(start=1):
    while True:
        yield f"S-{start}"
        start += 1

# --- Recursion Example ---
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# --- Lambda Example ---
calculate_discount = lambda fee, percent: fee - (fee * percent / 100)
