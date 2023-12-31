import os
import cv2
import numpy as np
import tensorflow.compat.v1 as tf
import network
import guided_filter
from tqdm import tqdm
tf.compat.v1.disable_eager_execution()


def cartoonize(load_folder, save_folder, model_path):
    print(f"cartoonize staring...............")
    input_photo = tf.placeholder(tf.float32, [1, None, None, 3])
    network_out = network.unet_generator(input_photo)
    final_out = guided_filter.guided_filter(
        input_photo, network_out, r=1, eps=5e-3)

    all_vars = tf.trainable_variables()
    gene_vars = [var for var in all_vars if 'generator' in var.name]
    saver = tf.train.Saver(var_list=gene_vars)
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)

    sess.run(tf.global_variables_initializer())
    saver.restore(sess, tf.train.latest_checkpoint(model_path))
    name_list = os.listdir(load_folder)
    my_list = name_list

    def divide_chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]
    n = 11
    name_list_chunks = list(divide_chunks(my_list, n))
    total_iteration = len(name_list_chunks)
    print(f"Total image is  {len(name_list)}")
    print(f"Total iteration is {total_iteration}")
    count=0
    for i in name_list_chunks:
        print(f"Iteration {count}")
        for name in tqdm(i):
            try:
                print(f"Image name : {name}")
                load_path = os.path.join(load_folder, name)
                save_path = os.path.join(save_folder, name)
                image = cv2.imread(load_path)
                batch_image = image.astype(np.float32)/127.5 - 1
                batch_image = np.expand_dims(batch_image, axis=0)
                output = sess.run(final_out, feed_dict={
                                  input_photo: batch_image})
                output = (np.squeeze(output)+1)*127.5
                output = np.clip(output, 0, 255).astype(np.uint8)
                cv2.imwrite(save_path, output)
            except Exception  as e:
                print('cartoonize {} failed {}'.format(load_path,str(e)))
        count += 1


if __name__ == '__main__':
    model_path = 'saved_models'
    load_folder = 'test_images'
    save_folder = 'cartoonized_images'
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    cartoonize(load_folder, save_folder, model_path)
