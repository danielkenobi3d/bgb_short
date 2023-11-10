from REF.asset.babyK import correctives_definition
from RMPY.rig import rigCorrectives
reload(correctives_definition)


def build():
    rig_correctives = rigCorrectives.CorrectiveBlendShapes(definition=correctives_definition)
    rig_correctives.build()


if __name__ == '__main__':
    build()
