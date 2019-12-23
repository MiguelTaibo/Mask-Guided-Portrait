### Copyright (C) 2017 NVIDIA Corporation. All rights reserved.
### Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
import os
from collections import OrderedDict
from torch.autograd import Variable
from options.test_options import TestOptions
from data.data_loader import CreateDataLoader
from models.models import create_model
import util.util as util
from util.visualizer import Visualizer
from util import html
import torch

opt = TestOptions().parse(save=False)
opt.nThreads = 1  # test code only supports nThreads = 1
opt.batchSize = 1  # test code only supports batchSize = 1
opt.serial_batches = True  # no shuffle
opt.no_flip = True  # no flip

data_loader = CreateDataLoader(opt)
dataset = data_loader.load_data()
visualizer = Visualizer(opt)
# create website
web_dir = os.path.join(opt.results_dir, opt.name, '%s_%s' % (opt.phase, opt.which_epoch))
webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.which_epoch))


def merge_image(no_bg_tensor, bg_tensor, label):
    assert no_bg_tensor.dim() == 3
    mask = (label == 0).type(torch.FloatTensor)
    mask_f = (label != 0).type(torch.FloatTensor)
    return no_bg_tensor.type(torch.FloatTensor) * mask_f + bg_tensor * mask


# test
if not opt.engine and not opt.onnx:
    model = create_model(opt)
    if opt.data_type == 16:
        model.half()
    elif opt.data_type == 8:
        model.type(torch.uint8)

    if opt.verbose:
        pass
        print(model)
else:
    from run_engine import run_trt_engine, run_onnx

for i, data in enumerate(dataset):

    import numpy as np
    from PIL import Image
    import shutil
    import matplotlib.pyplot as plt

    path = str(data['path'])
    print(path)
    path=path[4:len(path)-2]
    n = path.find('_label/')

    #rellenamos segunda imagen
    try:
        path_b=path[0:n]+'2_label/'+path[n+7:len(path)]
        Image.open(path_b)
    except:

        import matplotlib.pyplot as plt

        g_label = model.inference_parsing(data['label'], data['bg_contentimage'])
        img = g_label.cpu().detach().numpy()[0]
        img = np.array(img, dtype='uint8')
        #array_i = np.save("./datasets/helen_align/edit_label/1000.npy", img3)
        img = Image.fromarray(img)
        print('Generamos la mascara ' + path)
        img.save(path)

        path2 = path[0:n] + '2' + path[n:len(path)]
        print('La copiamos en ' + path2)
        img.save(path2)


        # img1 = data['bg_contentimage'].cpu().detach().numpy()[0][0]
        # img2 = data['label'].cpu().detach().numpy()[0][0]
        # plt.subplot(3, 1, 1)
        # plt.imshow(img1, cmap='gray')
        # plt.subplot(3, 1, 2)
        # plt.imshow(img2, cmap='gray')
        # plt.subplot(3, 1, 3)
        # plt.imshow(img, cmap='gray')
        # plt.show()


