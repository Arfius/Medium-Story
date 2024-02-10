import re
import json
import random

file = open('./dataset.txt')
dataset = file.read().split('\n')
file.close()

ids = []
ner_tags = []
tokens = []
feature_names = ["0"]

random.shuffle(dataset)

for i, sentence in enumerate(dataset):
	ids.append(i)
	sentence = sentence[0:-1]
	sentence_plain = sentence.replace("])", "").replace("[", '').replace("((", '(')
	sentence_plain = re.sub('\([a-z A-Z 0-9 ]*\)', "", sentence_plain)
	sentence_plain = re.sub('[ ]+', " ", sentence_plain)
	sentence_tokens = re.findall(r"[\w']+|[.,!?;]", sentence_plain)
	tags = ["0"] * len(sentence_tokens)

	annotations = re.findall('\(\([a-z A-Z 0-9\[\) ]*\]\)', sentence)
	for annotation in annotations:
		action = re.findall('\([a-z A-Z 0-9 ]*\)', annotation)[0].replace("(", "").replace(")", "")
		value = re.findall('\[[a-z A-Z 0-9 ]*\]', annotation)[0].replace("[", "").replace("]", "")
		
		for i, p_value in enumerate(value.split(" ")):
			_action = "B-"+action

			if i > 0:
				_action = "I-"+action

			tags[sentence_tokens.index(p_value)] = _action
			feature_names.append(_action)

	ner_tags.append(tags)
	tokens.append(sentence_tokens)


feature_names = list(set(feature_names))

for index_ner_tag in range(0, len(ner_tags)):

	for feature_index, value in enumerate(feature_names):
		indexes = [i for i, val in enumerate(ner_tags[index_ner_tag]) if val == value]
		for x in indexes:
			ner_tags[index_ner_tag][x] = feature_index

dataset_array_of_dict = []
for id, tags, tokens in zip(ids, ner_tags, tokens):
	dataset_array_of_dict.append({'id': id, 'ner_tags': tags, 'tokens': tokens})


# feature_names.json
feature_names_file_save = open('feature_names.json', 'w')
feature_names_file_save.write(json.dumps(feature_names))


# train.json
start = 0
end = int(len(dataset_array_of_dict)*0.80)
train = open('train.json', 'w')
train.write(json.dumps(dataset_array_of_dict[start:end]))

# test.json
start = int(len(dataset_array_of_dict)*0.80)
end = int(len(dataset_array_of_dict)*0.90)
test = open('test.json', 'w')
test.write(json.dumps(dataset_array_of_dict[start:end]))

# validation.json
start = int(len(dataset_array_of_dict)*0.90)
end = int(len(dataset_array_of_dict)*1.0)
validation = open('validation.json', 'w')
validation.write(json.dumps(dataset_array_of_dict[start:end]))