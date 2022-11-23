import glob
import os
from tqdm import tqdm 
from unetseg.train import TrainConfig, train
from unetseg.evaluate import plot_data_generator
import pathlib
import matplotlib.pyplot as plt



images_path = "../data/train/images/*.tif"

labels_path = "../data/train/labels/la_ladera.gpkg"

size = 600                

step_size = 100           

batch_size=16

output_dir = f"../data/tmp/chips/train_{size}_{step_size}"

os.system(command="~/Documents/Maiia-main-eduardo/notebooks/preproces.sh "+images_path+" "+labels_path+" "+str(size)+"  "+str(step_size)+" "+output_dir+" ")

contar_chips = 0

path_chips = "../data/tmp/chips/train_600_100/images"

for path in pathlib.Path(path_chips).iterdir():
    if path.is_file():
        contar_chips +=1

steps_per_epoch = int((contar_chips/batch_size) * 0.1)

print("steps per ecpch:" +str(steps_per_epoch) )

size_unet =batch_size * 10 

print("size unet:" +str(size_unet))

model_path = "../data/models/chimalhuacan_sample.h5"

config = TrainConfig(
    width=size_unet,  
    height=size_unet, 
    n_channels=3,     # cantidad de canales/bandas de la imagen
    n_classes=1,
    apply_image_augmentation=True,
    seed=42,
    epochs=10,        # cantidad de iteraciones
    batch_size=batch_size, 
    steps_per_epoch=steps_per_epoch, 
    early_stopping_patience=10,
    validation_split=0.1, 
    test_split=0.1,
    model_architecture='unet', # o "unetplusplus"
    images_path=output_dir,
    model_path=model_path,
    evaluate=True,
    class_weights=[1]
)


#plot_data_generator(num_samples=3, fig_size=(10, 10), train_config=config, img_ch=3)

# Entrenamiento

res_config = train(config)


plt.figure(figsize=(16,4))

plt.subplot(121)
plt.plot(res_config.history['loss'])
plt.plot(res_config.history['val_loss'])
plt.title('Loss')

plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc='upper left')

plt.subplot(122)
plt.plot(res_config.history['mean_io_u'])
plt.plot(res_config.history['val_mean_io_u'])
plt.title('mean_iou')
plt.ylabel('val_mean_iou')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc='upper left')

plt.show()
