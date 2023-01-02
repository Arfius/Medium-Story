import spacy
import textacy
import matplotlib.pylab as plt
import networkx as nx

# Extract Triples

# Load spacy model
nlp = spacy.load('en_core_web_sm')
# Plain text
text = "I am going to extract SVO"
# Process plain text with spacy
doc = nlp(text)


# Extract SVO list from spacy object
triples = list(textacy.extract.subject_verb_object_triples(doc))
print(triples)  # [SVOTriple(subject=[I], verb=[am, going], object=[to, extract, SVO])]


# Populate Graph
nodes = []
relations = []
# iterate over the triples
for triple in triples:
    # extract the Subject and Object from triple
    node_subject = "_".join(map(str, triple.subject))
    node_object = "_".join(map(str, triple.object))
    nodes.append(node_subject)
    nodes.append(node_object)
    # extract the relation between S and O
    # add the attribute 'action' to the relation
    relation = "_".join(map(str, triple.verb))
    relations.append((node_subject, node_object, {'action': relation}))

# remove duplicate nodes
nodes = list(set(nodes))
print(nodes)  # ['to_extract_SVO', 'I']
print(relations)  # [('I', 'to_extract_SVO', {'action': 'am_going'})]

# Create the graph
G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(relations)

# Show the graph
# extract the attribute 'action' from edges
edge_attribute = nx.get_edge_attributes(G, 'action')
edges, weights = zip(*edge_attribute.items())
# resize figure
plt.rcParams["figure.figsize"] = [5, 2]
plt.rcParams["figure.autolayout"] = True
# set figure layout
pos = nx.circular_layout(G)
# draw graph
nx.draw(G, pos, node_color='b', width=2, with_labels=True)
# draw edge attributes
nx.draw_networkx_edge_labels(G, pos, edge_attribute, label_pos=0.75)
plt.show()
