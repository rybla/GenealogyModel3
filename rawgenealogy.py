FILEENDING = ".rawgen"

def toRawGen(genealogy, name):
    with open(name + FILEENDING, "wb+") as file:
        # parameters
        file.write("PARAMETERS\n")
        for k,v in parameters.items():
            file.write()
        # agents
        # relations

def fromRawGen(filename)