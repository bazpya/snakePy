import logging
import warnings
from bazpy.print import print_line, print_vertical_space

warnings.warn = lambda *args, **kwargs: ...

print_vertical_space(3, ".")
print_line(False, "TensorFlow Output", True)

import tensorflow as tf

tf.compat.v1.get_logger().setLevel(logging.ERROR)  # Unnecessary but let it be
tf.compat.v2.get_logger().setLevel(logging.ERROR)  # Unnecessary but let it be

print_line(False, "Program Output", True)

ML = tf
