import json
import os
import logging
from tqdm import tqdm
from datetime import datetime
from config import PATHS, categories, img_size

# Set up logging
log_file_path = os.path.join(PATHS['save_path'], 'process.log')
os.makedirs(PATHS['save_path'], exist_ok=True)

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def generate_yolo_labels(json_path, save_path, fname_prefix=None, fname_postfix=None):
    img_w, img_h = img_size
    ignore_categories = ["drivable area", "lane", "other vehicle", "other person", "trailer"]
    with open(json_path) as json_file:
        data = json.load(json_file)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        for img in tqdm(data):
            # Check if 'labels' key exists
            if 'labels' not in img:
                logging.warning(f"Skipping entry without 'labels': {img.get('name', 'Unknown name')}")
                continue

            img_name = str(img['name'][:-4])
            img_label_txt = (fname_prefix if fname_prefix is not None else '') + img_name
            img_label_txt += (fname_postfix if fname_postfix is not None else '') + ".txt"

            # l type is list element: dict
            img_labels = [l for l in img['labels'] if l['category'] not in ignore_categories]
            file_path = save_path + img_label_txt
            with open(file_path, 'w+') as f_label:
                for label in img_labels:
                    y1 = label['box2d']['y1']
                    x2 = label['box2d']['x2']
                    x1 = label['box2d']['x1']
                    y2 = label['box2d']['y2']
                    class_name = label['category']

                    if class_name not in categories:
                        logging.warning(f"Skipping undefined category: {class_name} in entry {img.get('name')}")
                        continue

                    class_id = categories[class_name]

                    bbox_x = (x1 + x2) / 2
                    bbox_y = (y1 + y2) / 2

                    bbox_width = x2 - x1
                    bbox_height = y2 - y1

                    bbox_x_norm = bbox_x / img_w
                    bbox_y_norm = bbox_y / img_h

                    bbox_width_norm = bbox_width / img_w
                    bbox_height_norm = bbox_height / img_h

                    line_to_write = '{} {} {} {} {}'.format(
                        class_id - 1, bbox_x_norm, bbox_y_norm, bbox_width_norm, bbox_height_norm)
                    f_label.write(line_to_write + "\n")


def generate_yolo_filenames(imgs_path, labels_path, output_file_path):
    os.makedirs(PATHS['save_path'], exist_ok=True)
    count = 0
    with open(output_file_path, 'w+') as f:
        for dirpath, dirs, files in os.walk(imgs_path):
            for filename in tqdm(files):
                is_exist = os.path.isfile(labels_path + filename[:-4] + '.txt')
                if is_exist:
                    if filename.endswith(".jpg"):
                        file_path = os.path.join(
                            PATHS['owner_prefix'], dirpath, filename)
                        f.write(file_path + "\n")
                else:
                    count += 1
    logging.info('Number of skipped files: {}'.format(count))


def generate_names_file(filename='bdd100k.names'):
    os.makedirs(PATHS['save_path'], exist_ok=True)
    output_file_path = PATHS['save_path'] + filename
    with open(output_file_path, 'w+') as f:
        for key in categories.keys():
            f.write(key + "\n")
    logging.info('{} created'.format(filename))


def generate_data_file(filename='bdd100k.data'):
    os.makedirs(PATHS['save_path'], exist_ok=True)
    output_file_path = PATHS['save_path'] + filename
    with open(output_file_path, 'w+') as f:
        f.write('classes = 10' + '\n')
        f.write('train = {}train.txt'.format(PATHS['save_path']) + '\n')
        f.write('valid = {}val.txt'.format(PATHS['save_path']) + '\n')
        f.write('test = {}test.txt'.format(PATHS['save_path']) + '\n')
        f.write('names = {}bdd100k.names'.format(PATHS['save_path']) + '\n')
        f.write('backup = {}backup'.format(PATHS['save_path']) + '\n')
    logging.info('{} created'.format(filename))


if __name__ == '__main__':

    logging.info('Starting YOLO labels creation')
    print("Start yolo train label convertion\n")
    generate_yolo_labels(json_path=PATHS['labels_path_json_train'], save_path=PATHS['labels_save_path_train'],
                         fname_prefix=None, fname_postfix=None)
    print('Start yolo val label convertion\n')
    generate_yolo_labels(json_path=PATHS['labels_path_json_val'], save_path=PATHS['labels_save_path_val'],
                         fname_prefix=None, fname_postfix=None)

    # Generate labels for augmented images (if needed)
    # generate_yolo_labels(PATHS['labels_path_json_train'], PATHS['labels_save_path_train'],
    #                      fname_prefix='train_', fname_postfix='_fake_B')
    # generate_yolo_labels(PATHS['labels_path_json_val'], PATHS['labels_save_path_val'],
    #                      fname_prefix='val_', fname_postfix='_fake_B')

    # Generate test files(ignore now)

    generate_names_file(filename='bdd100k.names')
    generate_data_file(filename='bdd100k.data')

    logging.info('Process completed successfully')
