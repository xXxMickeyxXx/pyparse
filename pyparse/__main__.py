# from .runtime import main


# if __name__ == "__main__":
#     main()



import csv


TEST_FILEPATH = r"/Users/mickey/Desktop/Python/custom_packages/pyparse/files/data/example_grammar_parse_table.csv"


_data = {}
with open(TEST_FILEPATH, "r", newline=None) as in_file:
    _csv_reader = csv.DictReader(in_file, delimiter=",", fieldnames=["A", "B", "C"])
    next(_csv_reader)

    print(f"READING TEST CSV FILE AT FILEPATH ---> {TEST_FILEPATH}")
    print()
    for i in _csv_reader:
        _new_data = {k: v for k, v in i.items()}
        _data.update(_new_data)



_len_data = len(_data)
for idx, (data_key, data_val) in enumerate(_data.items(), start=0):
    print(f"{data_key}:\n  {data_val}")
    print()
print()
