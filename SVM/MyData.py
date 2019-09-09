def load_data_set(filepath):
    data_box = []
    label_box = []
    data_file = open(filepath)
    lines = data_file.readlines()
    lines = [p for p in lines if p != '\n']
    for line in lines:
        arr = line.strip().split('\t')
        arr = [x for x in arr if x != '']
        data_box.append([float(arr[0]), float(arr[1])])
        label_box.append(float(arr[2]))
    return data_box, label_box
