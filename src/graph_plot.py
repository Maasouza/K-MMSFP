import networkx as nx
import matplotlib.pyplot as plt
import random

def draw_trees(graph, trees):
    graph.make_uncomplete()
    G = nx.Graph()
    G.add_edges_from(list(graph.edges))
    pos = nx.shell_layout(G)
    for tree in trees:
        nodes = set()
        color = [random.random(),random.random(),random.random()]
        for u,v in tree:
            nodes.add(u)
            nodes.add(v)
        nx.draw_networkx_nodes(G,pos,
                                nodelist=list(nodes),
                                node_color=color,
                                node_size=100,
                                alpha = 0.8
        )
        nx.draw_networkx_edges(G,pos,
                                edgelist=list(tree),
                                width=1,
                                alpha = 0.8
        )
    plt.axis('off')
    plt.show()

def plot(trees, roots, infile, grafo=None, outfile='../out.html',draw_all = True):
    pos = []
    max_v = 0
    V,E = 0 ,0
    with open(infile,'r') as file:
        V, E = map(int,file.readline().split())
        for i in range(E):
            file.readline()
        for i in range(V):
            file.readline()
        for i in range(V):
            x, y = map(int,file.readline().split())
            if(x> max_v):
                max_v = x
            if(y>max_v):
                max_v = y
            pos.append([x,y])
    file = open(outfile,"w")
    start = " <!DOCTYPE html><html><body><svg height=\""+str((max_v+50)*2.0)+"\" width=\""+str((max_v+50)*2.0)+"\">"
    middle = ""
    vertex_list = {}

    for idx, tree in enumerate(trees):
        vertex_list[idx] = {
            "color":None,
            "vertexs":set()
        }
        color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        vertex_list[idx]["color"] = color[:]
        for u, v in list(tree.edges):
            vertex_list[idx]["vertexs"].add(u)
            vertex_list[idx]["vertexs"].add(v)
            p1 = pos[u]
            p2 = pos[v]
            middle += "<polyline points=\""
            middle += " "+str(p1[0]*2.0)+","+str(p1[1]*2.0)
            middle += " "+str(p2[0]*2.0)+","+str(p2[1]*2.0)
            middle +="\"style=\"fill:none;stroke:rgb("+str(color[0])+","+str(color[1])+","+str(color[2])+");stroke-width:6\"/>"
    middle2=""
    if(draw_all):
        for u, v in grafo.edges:
            p1 = pos[u]
            p2 = pos[v]
            middle += "<polyline stroke-dasharray=\"2\" points=\""
            middle += " "+str(p1[0]*2.0)+","+str(p1[1]*2.0)
            middle += " "+str(p2[0]*2.0)+","+str(p2[1]*2.0)
            middle +="\"style=\"fill:none;stroke:rgb(200,200,200);stroke-width:2\"/>"
    for _, item in vertex_list.items():
        color = item["color"]
        for v in item["vertexs"]:
            x = pos[v]
            radius = 15 if v not in roots else 25
            fontS = 15 if v not in roots else 26
            middle2+= "<circle cx=\""+str(x[0]*2.0)+"\" cy=\""+str(x[1]*2.0)+"\" r=\""+ str(radius) +"\"  fill=\"rgb("+str(color[0])+","+str(color[1])+","+str(color[2])+")\" />"
            middle2+= "<text font-size=\""+str(fontS)+"\" fill=\"white\" text-anchor=\"middle\" alignment-baseline=\"baseline\" x=\""+str(x[0]*2.0)+"\" y=\""+str(x[1]*2.0+5)+"\">"+str(v)+"</text>"
    end = "</svg></body></html>"
    string_write= start+middle+middle2+end
    file.write(string_write)

def plot_viz(trees, roots, grafo, outfile='../index.html'):
    file = open(outfile,"w")
    cost = {}
    for root in roots:
          cost[root] = 0
    first = """<!DOCTYPE html>
<!-- saved from url=(0106)https://www.l2f.inesc-id.pt/~david/wiki/pt/extensions/vis/examples/network/15_dot_language_playground.html -->
<html><head><meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
  <title>PLOT</title>

  <script type="text/javascript" src="./plot/vis.js.download"></script>
  <link href="./plot/vis.css" rel="stylesheet" type="text/css">

  <style type="text/css">
    body, html {
      font: 10pt sans;
      width: 100%;
      height: 100%;
      padding: 0;
      margin: 0;
      color: #4d4d4d;
    }

    #frame {
      width: 100%;
      height: 99%;
    }
    #frame td {
      padding: 10px;
      height: 100%;
    }
    #error {
      color: red;
    }

    #data {
      width: 100%;
      height: 100%;
      border: 1px solid #d3d3d3;
    }

    #mynetwork {
      float: left;
      width: 100%;
      height: 100%;
      border: 1px solid #d3d3d3;
      box-sizing: border-box;
      -moz-box-sizing: border-box;
      overflow: hidden;
    }

    textarea.example {
      display: none;
    }
  </style>
</head>
<body onload="drawExample()">
<h3>Raizes: """+str(roots)+""" Arquivo: """+grafo.file+"""</h3>
<div id="mynetwork"><div class="vis network-frame" style="position: relative; overflow: hidden; user-select: none; touch-action: pan-y; -webkit-user-drag: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); width: 100%; height: 100%;"><canvas width="649" height="529" style="position: relative; width: 100%; height: 100%; user-select: none; touch-action: pan-y; -webkit-user-drag: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></canvas></div></div>
<script type="text/javascript">
  var network = null;
  var data = null;
  var txtData = "";
  // resize the network when window resizes
  window.onresize = function () {
    network.redraw()
  };

  function destroy() {
    if (network !== null) {
      network.destroy();
      network = null;
    }
  }

  // parse and draw the data
  function draw () {
    destroy();
    try {
      // Provide a string with data in DOT language
      data = {
        dot: txtData
      };

      // create a network
      var container = document.getElementById('mynetwork');
      var options = {};
      network = new vis.Network(container, data, options);
    }
    catch (err) {
      // set the cursor at the position where the error occurred
      // show an error message
    }
  }

  function drawExample() {
    console.log(txtData);
    txtData = \""""
    last = "\";draw();}</script></body></html>";
    start = "graph{ node [shape=circle fontSize=16]  edge [length=100, color=gray, fontColor=black] "
    middle = ""
    for idx, tree in enumerate(trees):
        for u, v in tree.edges:
            cost[tree.root] = cost.setdefault(tree.root, 0) + grafo.adj_matrix[u][v]
            middle += " "+str(u)+" -- " +str(v)+"[label="+str(grafo.adj_matrix[u][v])+"];"
    for root in roots:
        middle+= " "+str(root)+" -- "+str(root)+"[label="+str(cost[root])+"];"
        middle+= " "+str(root)+"[fontColor=white,color=red,];"
    end = "}"
    file.write(first+start+middle+end+last)
