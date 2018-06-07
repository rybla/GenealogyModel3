from genealogy_lib.graphviz_defaults import *
from subprocess import call
import tempfile
import sys

class Graph:

    def __init__(self, genealogy, parameters=None):
        self.genealogy = genealogy
        self.parameters = parameters or default_graphviz_parameters
        self.attributes = {}
        self.attributes["graph"] = []
        self.attributes["edge"] = []
        self.attributes["node"] = []
        self.content = []

    def setParameters(self, params):
        for k,v in params.items():
            self.params[k] = v

    def generate(self):
        # start
        self.addContentLine("graph genealogy {")

        # set all attributes
        for field in ["graph","node","edge"]:
            for (attr,val) in self.parameters[field+"-attributes"]:
                self.setAttribute(field,attr,val)

        generations = [ [] for _ in range(self.genealogy.parameters["N"]) ]

        # add all nodes and edges
        # for each generation

        for gen_ind in range(self.genealogy.parameters["N"]):
            generation_population = self.genealogy.getGeneration(gen_ind)
            # for each agent
            for agent_ind in range(len(generation_population)):
                agent = generation_population[agent_ind]
                agent_nodename = self.agentToNodeName(agent)
                agent_nodelabel = str(agent.getAbsoluteFitness())
                agent_color = self.parameters["cs-to-color"](agent.getCS())
                agent_pos = self.node_pos(gen_ind,agent_ind) if self.parameters["assign-position"] else ""
                agent_shape = self.parameters["cs-to-shape"](agent.getCS())
                # node
                self.addNode(
                    agent_nodename,
                    agent_nodelabel,
                    agent_color,
                    pos=agent_pos,
                    shape=agent_shape
                )
                # edges to all children
                # print("getChildrenInds:",agent.getChildrenInds())
                for (_gen_ind,_agent_ind) in agent.getChildrenInds():
                    self.addEdge(
                        agent_nodename,
                        self.indsToNodeName(_gen_ind, _agent_ind),
                        agent_color
                    )
                # add to generation
                generations[gen_ind].append(agent_nodename)

        # add ranks if positions aren't directly assigned
        if not self.parameters["assign-position"]:
            rankslen = len(generations)
            self.addRankNodes(rankslen)
            for i in range(rankslen):
                self.setSameRank(generations[i],i)

        # end
        self.addContentLine("}")

    def node_pos(self,gen_id,agent_ind):
        pos_focus_factor = 100
        reversed_gen_id = self.genealogy.parameters["N"] - gen_id
        return '"{},{}!"'.format(pos_focus_factor*agent_ind,pos_focus_factor*reversed_gen_id)

    def makeDot(self,name):
        with open(name, "w") as file:
            for line in self.content:
                file.write(line + "\n")

    def make_output(self,name,type):
        with tempfile.NamedTemporaryFile() as dotfile:
            self.makeDot(dotfile.name)
            if self.parameters["assign-position"]:
                call(["dot","-Kneato","-n","-T"+type,dotfile.name,"-o",name])
            else:
                #print(dotfile.name)
                #print(name)
                call(["dot","-T"+type,dotfile.name,"-o",name])

    def makePDF(self,name):
        self.make_output(name,"pdf")

    def makeSVG(self,name):
        self.make_output(name,"svg")

    def setAttribute(self, field, attr, val):
        self.addContentLine(field + " [" + attr + " = " + val + "];")

    def addNode(self, name, label, color, shape=None, width=None, fontsize=None, pos=None):
        s = "\""+name+"\" [ label=\""+label+"\" color=\""+color+"\""
        if shape: s += " shape="+shape
        if width: s += " width="+width
        if fontsize: s += " fontsize="+fontsize
        if pos: s += " pos="+pos
        s += "];"
        self.addContentLine(s)

    def addEdge(self, node1, node2, color, penwidth=None):
        s = "\""+node1+"\" -- \""+node2+"\" [" + " color=\""+color+"\""
        if penwidth: s += "penwidth=" + penwidth
        s += "];"
        self.addContentLine(s)

    def addRankNodes(self, rankslen):
        self.addContentLine("subgraph ranks {")
        self.addContentLine("node[style=invis];edge[style=invis];")
        s = ""
        for i in range(rankslen):
            s += "\"rank:"+str(i)+"\" -- "
        s = s[:-4] + ";"
        self.addContentLine(s)
        self.addContentLine("}")

    def setSameRank(self, nodenames, rank):
        s = "{rank=same;\"rank:" + str(rank) + "\";"
        for nodename in nodenames:
            s += "\""+nodename+"\";"
        s += "};"
        self.addContentLine(s)

    def addContentLine(self, s):
        self.content.append(s)

    def agentToNodeName(self, agent):
        return self.indsToNodeName(agent.gen_ind, agent.agent_ind)

    def indsToNodeName(self, gen_ind, agent_ind):
        return str(gen_ind) + ":" + str(agent_ind)
