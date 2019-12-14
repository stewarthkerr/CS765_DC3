library(data.tree)
library(DiagrammeR)
library(networkD3)
df = read.csv("../data/Books.csv")

#Remove brackets, single quotes from pathName
df$pathName = gsub("\\[|\\]|\\'", "", df$pathName)

#Create the tree
df_tree = FromDataFrameTable(df, pathName = "pathName", pathDelimiter = ",")

#Visualize
df_tree_list <- ToListExplicit(df_tree, unname = TRUE)
radialNetwork(df_tree_list)