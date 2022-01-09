import argparse
import io
import os
import numpy as np

from yolo4.model import yolo_load_model


ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config_path",help="path to config file", default = "./model_data/yolov4.cfg")
ap.add_argument("-o","--output_path",help='path to output file',default = './model_data/yolov4_weight.h5')
ap.add_argument("-w","--weights_path",help='path to weights file',default='./model_data/yolov4.weights')
args = vars(ap.parse_args())

def main():
    config_path = args["config_path"]
    output_path = args["output_path"]
    weights_path = args["weights_path"]
    weights_only = False

    model = yolo_load_model(config_path,weights_path)
    if weights_only:
        model.save_weights(output_path)
        print('Saved Keras weights to {}'.format(output_path))
    else:
        model.save(output_path)
        print('Saved Keras model to {}'.format(output_path))


if __name__ == '__main__':
    main()
