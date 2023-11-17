
build_order = ['source', 'rig', 'load data', 'finalize']
build = {
    'source': [
        ('Import geometry', ['.import_guiderig_build.import_geometry']),
        ('Import guides', ['rig_builds'])
        ],
    'rig': [
        ('build rig', ['rig_build.build_rig']),
        ('custom rig', ['rig_build.custom_rig'])
        ],
    'load data': [
        ('load skinning', ['rig_build.load_skinning_data']),
        ('load shapes', ['rig_build.load_shapes_data'])
    ],
    'finalize': [
        ('cleanup', ['rig_build.cleanup']),
        ('custom finalize', ['rig_build.custom_finalize'])
    ],
}