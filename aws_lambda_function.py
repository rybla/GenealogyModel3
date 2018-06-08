from genealogy_lib import graphviz
import json
import tempfile
import genealogy_lib.genealogy as G
import genealogy_lib.graphviz as GV

def lambda_handler(event, context):
    return { "success":json.dumps(process_template(get_user_args(event)))}

def get_user_args(form_data):
    #print(form_data)
    return {
        "M": int(form_data['Mval']),
        "N": int(form_data['Nval']),
        "P": int(form_data['Pval']),
        "A": float(form_data['Aval']),
        "C": float(form_data['Cval']),
        #"P": int(request.form.get('RedToBlueSurvival')),
        "init-distribution": [int(form_data['RedStart'])/(int(form_data['BlueStart'])+int(form_data['RedStart']))],
        "V": [int(form_data['RedSurvival']),int(form_data['BlueSurvival'])],
        'assign-position': form_data['should_run_fast'] == "true"
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
    return svgfile.read().decode("utf-8")
