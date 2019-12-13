#Load packages
import altair as alt
alt.data_transformers.enable('json')
import pandas as pd
import numpy as np
import networkx as nx
import nx_altair as nxa
import EoN
import math


#Read in data
df = pd.read_csv("data/Books.csv",)
df = pd.read_csv("data/all-nodes.csv",)
df = pd.read_csv("data/PetSupplies.csv")


#Function to count the depth of the node
def count_depth (pathName):
   return pathName.count("',")

#This creates the depth column
df['Depth'] = df.pathName.apply(count_depth)
df.head()

#https://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3
#Create the graph and convert to tree
G = nx.from_pandas_edgelist(df, source = "parent", target = "id", edge_attr = True)
G = nx.bfs_tree(G, 0)

#Circular position, to convert to top down remove with and use pos below
pos = EoN.hierarchy_pos(G,0)#, width = 2*math.pi)
circle_pos = {u:(r*math.cos(theta),r*math.sin(theta)) for u, (theta, r) in pos.items()}

#Supply attributes to the nodes
for n in G.nodes():
    G.nodes[n]['id'] = df['id'][n]
    G.nodes[n]['name'] = df['name'][n]
    G.nodes[n]['Depth'] = df['Depth'][n]
    G.nodes[n]['productCount'] = df['productCount'][n]
    G.nodes[n]['subtreeProductCount'] = df['subtreeProductCount'][n]
    G.nodes[n]['numChildren'] = df['numChildren'][n]
    G.nodes[n]['alsoCount'] = df['alsoCount'][n]
    G.nodes[n]['also'] = df['also'][n]
    
#Build the graph vega object
vg_graph = nxa.draw_networkx(G=G, 
                             pos = pos, 
                             node_size = 20, 
                             node_tooltip = ['name:N','productCount'], 
                             node_label = 'name:N',
                             width = 0.25, 
                             arrow_width = 0.0, 
                             node_color = 'red').interactive()

# Get the layers
edges = vg_graph.layer[0]
nodes = vg_graph.layer[1]
attr = vg_graph.layer[2]

#Selection for left chart
brush_left = alt.selection_interval(encodings=['x'],empty='all')
brush_right = alt.selection_multi(encodings=['x'], empty = 'all')
brush_bottom = alt.selection_multi(encodings=['x'], fields=['name','Depth','productCount'], empty='all')

#Product categories by number of products
left = alt.Chart(attr.data).mark_bar().encode(
        alt.X("productCount:Q",
          bin=alt.BinParams(extent = [0,2500], step = 250),
          scale=alt.Scale(domain=(0, 2500)),
          axis=alt.Axis(title="Number of Products")),
        alt.Y('count()',
          axis=alt.Axis(title = "Number of Nodes"))
    ).properties(width = 400, height = 400)

#Product categories by depth
right = alt.Chart(attr.data).mark_bar().encode(
        alt.Y("count()",
             axis=alt.Axis(title = "")),
        alt.X('Depth:O',
              )
    ).properties(width = 400, height = 400)

                 
# gray background with selection
left_background = left.encode(
    color=alt.value('#ddd')
).add_selection(brush_left)

# blue highlights on the transformed data
left_highlight = left.transform_filter(brush_left).transform_filter(brush_right)

left_final = alt.layer(
    left_background,
    left_highlight
    )

right_background = right.encode(
    color=alt.value('#ddd')
).add_selection(brush_right)

# blue highlights on the transformed data
right_highlight = right.transform_filter(brush_left).transform_filter(brush_right)

right_final = alt.layer(
    right_background,
    right_highlight
    )

attr_background = attr.encode(
    opacity=alt.value(0.0)
).add_selection(brush_bottom)

attr_highlight = attr.transform_filter(brush_left).transform_filter(brush_right).transform_filter(brush_bottom)

attr_final = alt.layer(
    attr_background,
    attr_highlight
    )

bottom_final = edges+nodes+attr_final
bottom_final.configure_axis(grid = False)

table = alt.Chart(attr.data).mark_text().encode(
    y=alt.Y('row_number:O',axis=None)
).transform_window(
    row_number='row_number()'
).transform_filter(
    brush_bottom
).encode(text='also:N'
).properties(title = "Alsos"
).transform_window(
    rank='rank(row_number)'
).transform_filter(
    alt.datum.rank<5
).properties(width = 850, height = 500)


alt.vconcat(left_final|right_final,
            bottom_final.properties(width = 850, height = 500)&table,#&table.properties(width = 850, height = 500), 
            data=attr.data, 
            title = "Distribution of Product Categories by Number of Products & Depth",
            resolve = alt.Resolve(scale=alt.LegendResolveMap(color=alt.ResolveMode('independent')), axis=alt.AxisResolveMap('independent'))
           ).save('kerr_dc3.html')