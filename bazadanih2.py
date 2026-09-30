# Логвиненко Максим Юрійович

import sqlite3
import random
import time
import os

ones = [
    "", "один", "два", "три", "чотири", "п'ять",
    "шість", "сім", "вісім", "дев'ять"
]

teens = [
    "десять", "одинадцять", "дванадцять", "тринадцять",
    "чотирнадцять", "п'ятнадцять", "шістнадцять",
    "сімнадцять", "вісімнадцять", "дев'ятнадцять"
]

tens = [
    "", "", "двадцять", "тридцять", "сорок",
    "п'ятдесят", "шістдесят", "сімдесят",
    "вісімдесят", "дев'яносто"
]

hundreds = [
    "", "сто", "двісті", "триста", "чотириста",
    "п'ятсот", "шістсот", "сімсот",
    "вісімсот", "дев'ятсот"
]


def tri_chisla_v_slovo(n):
    result = []

    h = n // 100
    t = (n % 100) // 10
    o = n % 10

    if h:
        result.append(hundreds[h])

    if t == 1:
        result.append(teens[o])
    else:
        if t:
            result.append(tens[t])
        if o:
            result.append(ones[o])

    return " ".join(result)


def chislo_v_slovo(n):
    if n == 100000000:
        return "сто мільйонів"

    result = []

    millions = n // 1000000
    thousands = (n % 1000000) // 1000
    units = n % 1000

    if millions:
        result.append(tri_chisla_v_slovo(millions))
        result.append("мільйонів")

    if thousands:
        result.append(tri_chisla_v_slovo(thousands))
        result.append("тисяч")

    if units:
        result.append(tri_chisla_v_slovo(units))

    return " ".join(result).strip()


def create_db(size):
    db_name = f"db_{size}.db"

    if os.path.exists(db_name):
        os.remove(db_name)

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE numbers(
            number INTEGER,
            value TEXT
        )
    """)

    nums = random.sample(range(1, 100000001), size)

    data = []

    for num in nums:
        data.append((num, chislo_v_slovo(num)))

    random.shuffle(data)

    cur.executemany(
        "INSERT INTO numbers VALUES (?, ?)",
        data
    )

    conn.commit()
    conn.close()

    print(f"Створено {db_name}")

    return nums


def avg_search_time(db_name, nums, count=100):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    total_time = 0

    for _ in range(count):
        num = random.choice(nums)
        text = chislo_v_slovo(num)

        start = time.perf_counter()

        cur.execute(
            "SELECT * FROM numbers WHERE value=?",
            (text,)
        )

        cur.fetchone()

        finish = time.perf_counter()

        total_time += finish - start

    conn.close()

    return total_time / count


def create_index(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("""
        CREATE INDEX idx_value
        ON numbers(value)
    """)

    conn.commit()
    conn.close()


sizes = [10000, 50000, 100000, 500000, 1000000]

results = []

for size in sizes:
    print(f"\nОбробка бази на {size} записів")

    numbers = create_db(size)

    db_name = f"db_{size}.db"

    no_index_time = avg_search_time(
        db_name,
        numbers
    )

    create_index(db_name)

    index_time = avg_search_time(
        db_name,
        numbers
    )

    results.append(
        (size, no_index_time, index_time)
    )

print("\nРезультати:\n")

print(
    f"{'Записів':<12}"
    f"{'Без індексу':<20}"
    f"{'З індексом':<20}"
)

for size, t1, t2 in results:
    print(
        f"{size:<12}"
        f"{t1:<20.8f}"
        f"{t2:<20.8f}"
    )