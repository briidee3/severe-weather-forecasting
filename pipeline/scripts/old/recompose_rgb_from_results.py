# This script is for use recomposing RGB images of the output from the models and dataset(s) used
# for the tornado-forecasting project.
# BD 8-13-2023

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import imageio


sequences = list()
new_sequences = list()
save_dir = '.\\results_recomposed\\'
home_dir = '..\\..\\..\\datasets\\results\\eot_paper\\'

square_size = 120
cur_model = 'MS-ConvLSTM_demo'
seq_to_get = ['random_seed_11_demo', 'random_seed_29_demo', 'random_seed_37_demo', 'random_seed_47_demo', 'random_seed_58_demo', 'random_seed_70_demo']
#for seq in seq_to_get:
#    os.mkdir(os.path.join(save_dir, seq))


# normalize int8 png data (0-255) for use by plt for composing new images
def normalize_png(image):
    img_max = 255
    img_min = 0
    return np.clip( ( (image - img_min) / (img_max - img_min) ), 0, 1)
    

# compile and save RGB versions of images
def recompose_image(image_name = '1.png', image_dir = os.path.join(home_dir, cur_model, seq_to_get[0]), seq_name = 'results_seq_one'):   # square size refers to the config height and width from MS-RNN config.py
    image = imageio.imread(os.path.join(image_dir, image_name))  # load image
    
    # make recomposites
    img_rad = np.dstack([image[(square_size * 2):, :, 0], image[(square_size):(square_size * 2), :, 0], image[:(square_size), :, 0]])
    img_no_rad = np.dstack([image[(square_size * 2):, :, 0], image[(square_size):(square_size * 2), :, 0], np.zeros((square_size, (square_size * 2), 1))])
    
    # save with matplotlib.pyplot
    rad_save_path = os.path.join(save_dir, seq_name, image_name[:-4] + '_rad.png')
    no_rad_save_path = os.path.join(save_dir, seq_name, image_name[:-4] + '_no_rad.png')
    matplotlib.use('Agg')   # don't display images when saving
    plt.imsave(rad_save_path, normalize_png(img_rad))
    plt.axis('off')     # don't display axes in output image
    plt.imsave(no_rad_save_path, normalize_png(img_no_rad))
    plt.axis('off')
    
    # return image names
    return [rad_save_path, no_rad_save_path]
    
    
# cycle through directories, get file names
def do_image_sequence(base_dir = home_dir, seq_name = 'sequencename'):
    # get list of original files
    seq_list = os.listdir(base_dir)
    seq_list.sort()
    
    # compose RGBs and aggregate list of recomposites
    new_seq_list = list()
    for i, img in enumerate(seq_list):
        new_seq_list.append(recompose_image(image_name = img, image_dir = base_dir, seq_name = seq_name))
        seq_list[i] = os.path.join(base_dir, seq_list[i])
    
    # append current sequence files to seq_list for compilation creation
    sequences.append(seq_list)
    new_sequences.append(new_seq_list)



# go through all dirs
for seq in seq_to_get:
    seq_dir = os.path.join(home_dir, cur_model, seq, 'truth_pred_img')
    do_image_sequence(seq_dir, seq)
    
    
# create graph-like arrays of the original result images
for k, seq in enumerate(sequences):
    # create subplots
    fig, axs = plt.subplots(2, 10, figsize = (60, 12))
    
    for i, ax in enumerate(fig.axes):
        # plot image
        ax.imshow(imageio.imread(seq[i]))
        ax.axis('off')
        # plot label
        ax.text(0.0, 1.0, 'Frame ' + str(i) + '\n', size = 24)
    
    plt.subplots_adjust(hspace = 0.2, wspace = 0.01)
    fig.savefig(os.path.join(save_dir, 'subplots', 'seq_' + str(k)))
    
# create graph-like arrays of the new composed images
for k, seq in enumerate(new_sequences):
    # do for rad and no_rad variants
    for no_rad in range(0, 2):
        # create subplots
        fig, axs = plt.subplots(2, 10, figsize = (60, 12))
        
        for i, ax in enumerate(fig.axes):
            # plot image
            ax.imshow(imageio.imread(seq[i][no_rad]))
            ax.axis('off')
            # plot label
            if no_rad:
                ax.text(0.0, 1.0, 'Frame ' + str(i) + ' (w/out Rad)\n', size = 24)
            else:
                ax.text(0.0, 1.0, 'Frame ' + str(i) + ' (w/ Rad)\n', size = 24)
            
        plt.subplots_adjust(hspace = 0.2, wspace = 0.1)
        
        if no_rad:
            fig.savefig(os.path.join(save_dir, 'subplots', 'seq_' + str(k) + '_without_rad'))
        else:
            fig.savefig(os.path.join(save_dir, 'subplots', 'seq_' + str(k) + '_with_rad'))
        
