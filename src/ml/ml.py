import logging
import warnings

warnings.warn = lambda *args, **kwargs: ...

print(".", end="\r", flush=True)
print("")
for _ in range(3):
    print(".")
line = "==============================="
print(f"{line}  TensorFlow Output  {line} \n")

import tensorflow as tf

tf.compat.v1.get_logger().setLevel(logging.ERROR)  # Unnecessary but let it be
tf.compat.v2.get_logger().setLevel(logging.ERROR)  # Unnecessary but let it be

print(f"{line}  Program Output  {line} \n")

ML = tf
