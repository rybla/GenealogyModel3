from genealogy_lib import graphviz
import json
import tempfile
import genealogy_lib.genealogy as G
import genealogy_lib.graphviz as GV
from genealogy_lib.graphviz_defaults import default_graphviz_parameters

def lambda_handler(event, context):
    return { "success":json.dumps(process_template(get_user_args(event)))}

def get_user_args(form_data):
    #print(form_data)
    #print(form_data.get('should_run_fast'))
    use_single_trait = form_data.get('use_single_trait') == "true"
    print(float(form_data.get('Aval')))
    return {
        "M": int(form_data.get('Mval')),
        "N": int(form_data.get('Nval')),
        "P": int(form_data.get('Pval')),
        "A": -float(form_data.get('Aval')),
        "C": float(form_data.get('Cval')),
        #"P": int(request.form.get('RedToBlueSurvival')),
        "init-distribution": [1-float(form_data.get('RedPropStart'))]
                                if use_single_trait else
                             [1-float(form_data.get('RedPropStart')),1-float(form_data.get('DarkPropStart'))],
        "use_single": use_single_trait,
        "with_replacement": form_data.get('WithReplacement') == "true",
        "V": [
            float(form_data.get('RedSurvival')),
            float(form_data.get('BlueSurvival'))
        ],
        "TWO":  [
            [
                float(form_data.get('LightRedSurv')),
                float(form_data.get('DarkRedSurv'))
            ],
            [
                float(form_data.get('LightBlueSurv')),
                float(form_data.get('DarkBlueSurv'))
            ],
        ],
        'assign-position': form_data.get('should_run_fast') == "true"
    }

def verify_user_args(user_args):
    assert (user_args['N']) > 0
    assert (user_args['M']) > 0
    assert (user_args['P']) > 0
    assert (user_args['C']) >= 0

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
    TWO  = user_args["TWO"]
    using_single = user_args["use_single"]

    def M(prev_m, gen_ind): return M_
    def P(gen_ind): return P_
    def CF(cs): return V[cs[0]] if using_single else TWO[cs[0]][cs[1]]
    def F(agent, ref_gen_ind, A): return (agent.absolute_fitness*(ref_gen_ind - agent.gen_ind) ** A)

    genealogy_parameters = {
        "name" : name,
        "M" : M,
        "N" : N,
        "P" : P,
        "A" : user_args["A"],
        "C" : user_args["C"],
        "G" : json_genparams["G"],
        "T" : 1 if using_single else 2 , # json_genparams["T"],
        "CF" : CF,
        "F"  : F,
        "init_distribution" : user_args["init-distribution"],
        "replacement" : user_args["with_replacement"]
    }

    graphviz_parameters = data["graphviz-parameters"]
    graphviz_parameters["cs-to-color"] = default_graphviz_parameters["cs-to-color"]
    graphviz_parameters["cs-to-shape"] = default_graphviz_parameters["cs-to-shape"]
    graphviz_parameters["assign-position"] = user_args['assign-position']
    graphviz_parameters['dot-command'] = "./dot_static"

    # Genealogy
    genea = G.Genealogy(genealogy_parameters)
    genea.generate()

    # Graph
    graph = GV.Graph(genea,graphviz_parameters)
    graph.generate()
    svgfile = tempfile.NamedTemporaryFile()
    graph.makeSVG(svgfile.name)
    return svgfile.read().decode("utf-8")
