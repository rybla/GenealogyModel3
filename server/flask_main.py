#!/usr/bin/env python

from flask import Flask, render_template, request
from genealogy_lib import graphviz
import json
import tempfile
import genealogy_lib.genealogy as G
import genealogy_lib.graphviz as GV

# This is a tinkertoy web app. Please enjoy.

# Here we make our application; we'll use this to set routes, among other
# things.
app = Flask(__name__)
# For now we're manually turning on `debug`; we like this for a few
# reasons. Chief among them: much better logging; "hot reloading," in which
# changes to our code will show up without having to stop and restart the
# server.
app.debug = True


# This is a "route" -- it tells the http server what URLs it can respond to
# (technically, we're defining "resources"). This route responds to "/", which
# is the "root" of our website. "/" is what you get implicitly if you go to,
# say "www.google.com" -- google.com is the "host", and with nothing else
# specified you get "/".
@app.route('/')
@app.route('/index.html')
def index():
    return app.send_static_file('html/graph.html')

@app.route('/get_plot', methods=['POST'])
def plot_thingy():
    #print(form.args.get('fname'))
    return process_template(get_user_args(request.form))

def run_server_publicly():
    app.run(host='0.0.0.0')

def get_user_args(form_data):
    #print(form_data)
    print(form_data.get('should_run_fast'))
    return {
        "M": int(form_data.get('Mval')),
        "N": int(form_data.get('Nval')),
        "P": int(form_data.get('Pval')),
        "A": float(form_data.get('Aval')),
        "C": float(form_data.get('Cval')),
        #"P": int(request.form.get('RedToBlueSurvival')),
        "init-distribution": [int(form_data.get('RedStart'))/(int(request.form.get('BlueStart'))+int(request.form.get('RedStart')))],
        "V": [int(form_data.get('RedSurvival')),int(form_data.get('BlueSurvival'))],
        'assign-position': form_data.get('should_run_fast') == "true"
    }

def verify_user_args(user_args):
    assert (user_args['N']) > 0
    assert (user_args['M']) > 0
    assert (user_args['P']) > 0
    assert (user_args['C']) >= 0
    user_args['init-distribution']

def process_template(user_args):
    verify_user_args(user_args)
    data = ""
    template_filepath = "makegen_config/server_default_template.json"
    with open(template_filepath, "r") as f:
        data = json.load(f)
    json_genparams = data["genealogy-parameters"]

    name = json_genparams['name']
    # user parameters
    M_ = user_args["M"]
    N  = user_args["N"]
    P_ = user_args["P"]
    V  = user_args["V"]

    def M(prev_m, gen_ind): return M_
    def P(gen_ind): return P_
    def CF(cs): return V[0] if cs[0] else V[1]
    def F(agent, ref_gen_ind, A): return (agent.absolute_fitness*(ref_gen_ind - agent.gen_ind) ** A)

    genealogy_parameters = {
        "name" : name,
        "M" : M,
        "N" : N,
        "P" : P,
        "A" : user_args["A"],
        "C" : user_args["C"],
        "G" : json_genparams["G"],
        "T" : 1, # json_genparams["T"],
        "CF" : CF,
        "F"  : F,
        "init_distribution" : user_args["init-distribution"],
        "replacement" : json_genparams["replacement"]
    }

    graphviz_parameters = data["graphviz-parameters"]
    graphviz_parameters["cs-to-color"] = lambda cs: "#FF0000" if cs[0] else "#0000FF"
    graphviz_parameters["assign-position"] = user_args['assign-position']

    # Genealogy
    genea = G.Genealogy(genealogy_parameters)
    genea.generate()

    # Graph
    graph = GV.Graph(genea,graphviz_parameters)
    graph.generate()
    svgfile = tempfile.NamedTemporaryFile()
    graph.makeSVG(svgfile.name)
    return svgfile.read()
