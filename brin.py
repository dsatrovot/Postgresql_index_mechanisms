
def build_brin(data, range_size):
    index = []

    for start in range(0, len(data), range_size):
        end = min(start + range_size, len(data))

        min_value = min(data[start:end])
        max_value = max(data[start:end])

        index.append({
            "start": start,
            "end": end,
            "min": min_value,
            "max": max_value
        })

    return index


def brin_search(data, index, value):
    result = []

    for block in index:

        # Проверяем summary
        if block["min"] <= value <= block["max"]:

            print(
                f"Scanning block range: "
                f"{block['start']}:{block['end']}"
            )

            # Recheck реальных строк
            for i in range(block["start"], block["end"]):

                if data[i] == value:
                    result.append(data[i])

        else:
            print(
                f"Skipping block range: "
                f"{block['start']}:{block['end']}"
            )

    return result





data = [
    10, 20, 30, 40,
    50, 60, 70, 80,
    90, 100, 110, 120,
    130, 140, 150, 160
]

index = build_brin(data, 4)

for item in index:
    print(item)
print(brin_search(data,index,100))