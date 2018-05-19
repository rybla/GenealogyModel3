default_graphviz_parameters = {
    
    "graph-attributes" : [
        ("nodesep", "0.1"),
        ("ranksep", "1"),
        ("size", "5"),
        ("ratio", "fill")
    ],

    "node-attributes" : [
        ("style", "filled"),
        ("fontcolor", "white"),
        ("shape", "circle"),
        ("width", "1"),
        ("fontsize", "20.0")
    ],

    "edge-attributes" : [
        ("penwidth", "4")
    ],

    "cs-to-color" : (
        lambda cs: "#FF0000" if cs[0] else "#0000FF"
    )

}