import os
from unetseg.predict import PredictConfig, predict
from unetseg.evaluate import plot_data_results

from satproc.postprocess.polygonize import polygonize 
from satproc.filter import filter_by_max_prob
from maiia.postprocess import filter_by_min_area


size = 600              # tamaño (en pixeles) de las imagenes que se van a generar
step_size = size        # en la predicción no hace falta generar solapamiento, usamos mismo tamaño en step_size

images_path = "../data/predict/images/*.tif"        # ruta a las imagenes satelitales
output_dir = f"../data/tmp/chips/predict_{size}"    # ruta donde se van a dejar las imagenes porcesadas

os.system(command="~/Documents/Maiia-main-eduardo/notebooks/Pred_preproces.sh "+ images_path  +" "+ output_dir +" "+ str(size)  +" "+ str(step_size)  +"  ")


images_path = output_dir                          # usamos los chips generados recientemente con satproc
model_path = "../data/models/chimalhuacan_sample.h5"        # ruta al modelo que generams en el notebook de entrenamiento
results_path = f"../data/tmp/result_chips/{size}"    # ruta a los chips de resultado de predicción

predict_config = PredictConfig(
    images_path=output_dir,
    results_path=results_path,
    batch_size=16,
    model_path=model_path,
    height=160,
    width=160,
    n_channels=3,
    n_classes=1,
    class_weights=[1]
)



predict(predict_config)

plot_data_results(num_samples=5, fig_size=(5, 5), predict_config=predict_config, img_ch=2, n_bands=3)


threshold = 0.5    # parametro a filtrar (probar ≠ prob umbrales, quizas empezar con 0.1)
min_area = 500     # superficie minima a fitrar
output_path = "../data/results/results_sample.gpkg"   # ruta al geopackage final de poligonos



# Filtra todos los chips que tengan menor probabilidad a la especificada (threshold)
# y los guarda en otra carpeta (filt_dir)
filt_dir = "../data/tmp/filt/"
filter_by_max_prob(
    input_dir=results_path,
    output_dir=filt_dir,
    threshold=threshold
)


# Poligoniza todos los chips filtrados en un solo archivo vectorial en formato GeoPackage
poly_path = "../data/tmp/poly.gpkg"
polygonize(
    input_dir=filt_dir,
    output=poly_path,
        threshold=threshold,
)


# Filtra poligonos con área mínima (>= min_area)
filter_by_min_area(
    poly_path,
    output_path,
    min_area=min_area
)

print('Resultados almacenados en:', output_path)
