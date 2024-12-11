import json
import os 
from tqdm import tqdm

# 将 Labelme 生成的 Json 文件的矩形框转换为 YOLO 的矩形框标注格式 （txt）
def json2yolo(cls_dict, json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # get info
    img_width = data['imageWidth']
    img_height = data['imageHeight']
    shapes = data['shapes']

    for shape in shapes:
        cls_name = shape['label']
        cls_id = int(cls_dict[cls_name])
        points = shape['points']
        x1, y1 = points[0]
        x2, y2 = points[1]

        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        w = abs(x2 - x1)
        h = abs(y2 - y1)

        x = x / img_width
        y = y / img_height
        w = w / img_width
        h = h / img_height

        with open(json_file.replace('.json', '.txt'), 'a') as f:
            f.write(f'{cls_id} {x} {y} {w} {h}\n')
    pass

if __name__ == 'main':
    class_dict = {
        'gap': 0, 
        'wafer': 1,
        'bad_wafer': 2,
        'broken': 3,
        'hole': 4,
        'crack': 5
    }

    # listdir and keep only json files
    json_files = [f for f in os.listdir('micro_crack_1209') if f.endswith('.json')]

    for json_file in tqdm(json_files):
        json2yolo(class_dict, os.path.join('micro_crack_1209', json_file))