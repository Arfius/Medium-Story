
from transformers import pipeline

classifier = pipeline("ner", model='./model_output')
print("WRITE SENTENCE")
while True:
	text = input()
	v = classifier(text)
	[print(x['entity'],x['word']) for x in v]
	print("===========")
	