import tensorflow as tf

gpu_devices = tf.config.list_physical_devices('GPU')

if gpu_devices:
    print("Tiene dispositivos GPU:")
    for dev in gpu_devices:
        print("*", dev.name)
else:
    print("No se han encontrados dispositivos GPU.")