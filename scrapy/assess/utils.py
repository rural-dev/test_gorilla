
def clean(data):
    data_cleaned = data
    if data:
        data_cleaned = str(data).encode('ascii', errors='ignore').decode('unicode-escape').replace("\n", "").replace('\r', "").replace('\t', "").strip()
    return data_cleaned