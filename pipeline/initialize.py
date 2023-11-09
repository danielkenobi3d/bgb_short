import pymel.core as pm
def import_model(environment):
    pm.importFile(environment.model)