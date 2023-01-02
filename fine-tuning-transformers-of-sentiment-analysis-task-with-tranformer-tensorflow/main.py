import pandas as pd
from sklearn.model_selection import train_test_split

dataset = pd.read_csv("./IMDB Dataset.csv")[0:100]


def setLabel(x):
    if (x['sentiment'] == 'positive'):
        x['label'] = 1
        return x
    elif (x['sentiment'] == 'negative'):
        x['label'] = 0
        return x
    return None


print('Data preparation')
dataset = dataset.apply(lambda x: setLabel(x), axis=1)
dataset = dataset.dropna()
train_texts = dataset['review'].values.tolist()
train_labels = dataset['label'].values.tolist()
train_texts, test_val_texts, train_labels, test_val_labels = train_test_split(train_texts, train_labels, test_size=.3)
test_texts, val_texts, test_labels, val_labels = train_test_split(test_val_texts, test_val_labels, test_size=.5)


print('Data Tokenization')
from transformers import DistilBertTokenizerFast
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
train_encodings = tokenizer(train_texts, truncation=True, padding=True, return_tensors='np').data
val_encodings = tokenizer(val_texts, truncation=True, padding=True, return_tensors='np').data
test_encodings = tokenizer(test_texts, truncation=True, padding=True, return_tensors='np').data


print('Setup the model')
from transformers import TFAutoModelForSequenceClassification
from tensorflow.keras.layers import *
import tensorflow as tf

model = TFAutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=3, id2label={0: 'negative', 1: 'neutral', 2:'positive'})
optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
model.compile(optimizer=optimizer, loss=model.hf_compute_loss)
print(model.summary())


print('Fine-tuning and Evaluation')
import numpy as np
model.fit(train_encodings, np.array(train_labels), validation_data=(val_encodings, np.array(val_labels)), epochs=1, batch_size=16)
print(model.evaluate(test_encodings, np.array(test_labels)))

print('Export Model and Tokenizer')
model.save_pretrained("IMDB-distilbert-base-uncased")
tokenizer.save_pretrained("IMDB-distilbert-base-uncased")


print('Load model and make a prediction')
from transformers import pipeline
pipe = pipeline("text-classification", model="./IMDB-distilbert-base-uncased", tokenizer="./IMDB-distilbert-base-uncased")
print(pipe("i love this actor"))
print(pipe("i don't like this movie"))
