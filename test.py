def generate(start: float, end: float, step: float = 1) -> int:
    current_value = start

    while current_value < end:
        yield current_value
        current_value += step

for value in generate(1, 100):
    print(value)
