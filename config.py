import os

owner_prefix = '/home/belle'
dataset_path = os.path.join(owner_prefix, 'YOLO', 'datasets', 'bdd100k')
labels_path = os.path.join(dataset_path, 'labels')
images_path = os.path.join(dataset_path, 'images', '100k')

images_path_train = os.path.join(images_path, 'train')
images_path_val = os.path.join(images_path, 'val')
images_path_test = os.path.join(images_path, 'test')

labels_path_json_train = os.path.join(labels_path, 'bdd100k_labels_images_train.json')
labels_path_json_val = os.path.join(labels_path, 'bdd100k_labels_images_val.json')

save_path = os.path.join(dataset_path, 'yolo_')
labels_save_path = os.path.join(save_path, 'labels')
labels_save_path_train = os.path.join(labels_save_path, 'train')
labels_save_path_val = os.path.join(labels_save_path, 'val')
labels_save_path_test = os.path.join(labels_save_path, 'test')

file_path_train = os.path.join(save_path, 'train.txt')
file_path_val = os.path.join(save_path, 'val.txt')
file_path_test = os.path.join(save_path, 'test.txt')

img_size = (1280, 720)
categories = {
    'pedestrian': 1,
    'rider': 2,
    'car': 3,
    'truck': 4,
    'bus': 5,
    'train': 6,
    'motorcycle': 7,
    'bicycle': 8,
    'traffic light': 9,
    'traffic sign': 10
}

PATHS = {
    'dataset_path': dataset_path,
    'labels_path': labels_path,
    'images_path_train': images_path_train,
    'images_path_val': images_path_val,
    'images_path_test': images_path_test,
    'labels_path_json_train': labels_path_json_train,
    'labels_path_json_val': labels_path_json_val,
    'file_path_train': file_path_train,
    'file_path_val': file_path_val,
    'file_path_test': file_path_test,
    'save_path': save_path,
    'labels_save_path_train': labels_save_path_train,
    'labels_save_path_val': labels_save_path_val,
    'labels_save_path_test': labels_save_path_test
}
