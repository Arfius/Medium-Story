import pandas as pd
import networkx as nx
import matplotlib.pylab as plt

groceries = pd.read_csv('Groceries_dataset.csv')
groceries['Receipt_id'] = [f"{d}_{i}" for d,i in zip(groceries['Date'], groceries['Member_number'])]

# To check a recepit we can run the code below.
receipts = groceries.sort_values(by=['Date']).groupby(by=['Receipt_id'])
r_id = list(receipts.groups.keys())[0]
print(receipts.get_group(r_id))

# list product nodes
items_unique = groceries['itemDescription'].unique()
node_items = [(x, {'type':'item'}) for x in items_unique]

# list member nodes
members_unique = groceries['Member_number'].unique()
node_members = [(x, {'type':'member'}) for x in members_unique]

# list member nodes
receipt_id_unique = groceries['Receipt_id'].unique()
node_receipts = [(x, {'type':'receipt'}) for x in receipt_id_unique]

# Create Relations
relations_has_item = []
relations_has_purchased = []

for index, row in groceries.iterrows():
    relations_has_purchased.append((row['Member_number'], row['Receipt_id'], {'relation':'has_purchased'}))
    relations_has_item.append((row['Receipt_id'], row['itemDescription'], {'relation':'has_item'}))

relations = relations_has_item + relations_has_purchased


# create an empty Graph
G = nx.MultiGraph()

# populate the Graph with nodes and relations
G.add_nodes_from(node_items)
G.add_nodes_from(node_members)
G.add_nodes_from(node_receipts)
G.add_edges_from(relations)


# # Plot the graph
# plt.rcParams["figure.figsize"] = [10, 10]
# plt.rcParams["figure.autolayout"] = True

# pos = nx.circular_layout(G)

# nx.draw_networkx(G, pos=pos, nodelist=[x[0] for x in node_items] ,node_color='g', node_size=2000)
# nx.draw_networkx(G, pos=pos, nodelist=[x[0] for x in node_members] ,node_color='y', node_size=2000)
# nx.draw_networkx(G, pos=pos, nodelist=[x[0] for x in node_receipts], node_color='r', node_size=2000)
# plt.show()


# compute the degree_centrality measure
g_centrality = nx.degree_centrality(G)

# filter node taking only the items
items_centrality = {k: v for k, v in g_centrality.items() if k in items_unique}

# sort the degree_centrality in ascending mode
items_centrality = sorted(items_centrality.items(), key=lambda x: x[1], reverse=False)

# # print products
the_10_less_important_products=[x[0] for x in items_centrality[0: 10]]

print(the_10_less_important_products)
# ['kitchen utensil', 'preservation products', 'baby cosmetics', 
# 'bags', 'frozen chicken', 'rubbing alcohol', 'make up remover', 
# 'toilet cleaner', 'salad dressing', 'whisky']


receipts = list(G.neighbors('whisky'))
print(receipts)
# ['25-03-2015_1654', '31-08-2015_1090', '03-09-2015_2152', '25-12-2015_2825', '15-01-2015_2232', '05-04-2014_3523', '01-10-2014_2138', '29-05-2014_4261']

products = []
for x in receipts:
    products.extend(list(G.neighbors(x))[0:-1])
    
target_product_centrality = {k: v for k, v in g_centrality.items() if k in products}
items_centrality = sorted(target_product_centrality.items(), key=lambda x: x[1], reverse=True)
products_for_promotion = items_centrality[0][0]
print(products_for_promotion)