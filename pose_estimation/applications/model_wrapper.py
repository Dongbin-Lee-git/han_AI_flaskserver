import tensorflow as tf
import pose_estimation.post_processing.post as post
import pose_estimation.configs.post_config as post_config
import pose_estimation.configs.keypoints_config as kpts_config

post.Skeletonizer.config(kpts_config.KEYPOINTS_DEF, kpts_config.JOINTS_DEF, post_config)
post.Skeleton.config(kpts_config.KEYPOINTS_DEF, kpts_config.JOINTS_DEF)


class ModelWrapper:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def process_image(self, img):
        input_img = tf.image.resize(img, (368, 368))
        input_img = tf.image.convert_image_dtype(input_img, dtype=tf.float32)
        input_img /= 255
        input_img = input_img[tf.newaxis, ...]
        pafs, kpts = self.model.predict(input_img)
        pafs = pafs[0]
        kpts = kpts[0]
        skeletonizer = post.Skeletonizer(kpts, pafs)
        skeletons = skeletonizer.create_skeletons()
        return skeletons
