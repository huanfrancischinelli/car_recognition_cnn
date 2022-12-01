from sys import displayhook
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from keras.preprocessing.image import ImageDataGenerator
from tensorflow import keras
from keras.regularizers import l2
from imutils import paths
import simplepreprocessor as preprocessor
import simpledatasetloader as loader
import argparse
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pickle
import os

# Argumento opcionais para personalização dos parametros
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--epochs", required=False,
	help="Integer value")
ap.add_argument("-d", "--dataset", required=False,
	help="Path to dataset")
ap.add_argument("-l", "--learnrate", required=False,
	help="Customize learnrate")
args = vars(ap.parse_args())


# parametros default
EPOCHS      = 300
LEARNRATE   = 0.01
BATCH_SIZE  = 32
BASE_DIR    = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
MODELS_DIR  = os.path.join(BASE_DIR, 'models')
LABELS_DIR  = os.path.join(BASE_DIR, 'labels')
LOGS_DIR    = os.path.join(BASE_DIR, 'logs')
HEIGHT, WIDTH = 64, 64

# parametros modificados por argumentos opcionais
if args["epochs"]:
    EPOCHS = int(args["epochs"])
if args["dataset"]:
    DATASET_DIR = str(args["dataset"])
if args["learnrate"]:
    LEARNRATE = str(args["learnrate"])
print(DATASET_DIR)
dataset = list(paths.list_images(DATASET_DIR))
sp = preprocessor.SimplePreprocessor(HEIGHT, WIDTH)
sdl = loader.SimpleDatasetLoader(preprocessors=[sp])
(data, labels) = sdl.load(dataset, verbose=1000)

lb = LabelBinarizer()
binlabels = lb.fit_transform(labels)

# solucao para isolar as labels para uso posterior
getlabels = []
[getlabels.append(x) for x in labels if x not in getlabels]
labels = getlabels


dataNormal = data.astype("float") / 255.0
(trainX, testX, trainY, testY) = train_test_split(dataNormal, binlabels,
    test_size=0.25, random_state=42)



model = keras.Sequential(
    [
        keras.Input(shape=(HEIGHT, WIDTH, 3)),
        keras.layers.Conv2D(64, kernel_size=(3, 3), activation="relu", kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01)),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Conv2D(64, kernel_size=(3, 3), activation="relu", kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01)),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Conv2D(32, kernel_size=(3, 3), activation="relu", kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01)),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dense(len(labels), activation="softmax"),
    ]
)

# treinamento da rede
print("[INFO] training network...")
sgd = keras.optimizers.SGD(LEARNRATE)
model.compile(loss="categorical_crossentropy", optimizer=sgd,
	metrics=["accuracy"])
# adam =  keras.optimizers.Adam()
# model.compile(optimizer=adam,
#               loss="categorical_crossentropy",
#               metrics=['accuracy'])
H = model.fit(trainX, trainY, validation_data=(testX, testY),
	epochs=EPOCHS, batch_size=BATCH_SIZE, shuffle=True)

# avaliacao da rede
print("[INFO] evaluating network...")
predictions = model.predict(testX, batch_size=BATCH_SIZE)
print(classification_report(testY.argmax(axis=1),
	predictions.argmax(axis=1), target_names=lb.classes_))

# geracao do grafico de loss/accuracy
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, EPOCHS), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, EPOCHS), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, EPOCHS), H.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, EPOCHS), H.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend()

# filename de todos os arquivos relacionados tera a mesma terminacao, referente a data
FILENAME = str('{date:%Y%m%d_%H%M}').format(date=datetime.datetime.now())

# save do grafico
plt.savefig(os.path.join(LOGS_DIR, 'log-'+FILENAME+'.png'))
# save do modelo
model.save(os.path.join(MODELS_DIR, 'model-'+FILENAME+'.h5'))
# save das labels
f = open(os.path.join(LABELS_DIR, 'labels-'+FILENAME+'.pickle'), "wb")
f.write(pickle.dumps(labels))
f.close()

