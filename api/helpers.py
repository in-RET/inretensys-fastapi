import InRetEnsys

def CreateComponentsList():
    allElements = InRetEnsys.__all__

    # Fancy workaround für meine Dummheit
    if "InRetEnsysConfigContainer" in allElements:
        allElements.remove("InRetEnsysConfigContainer")

    componentslist = []

    for element in allElements:
        componentslist.append(element)

    return componentslist
