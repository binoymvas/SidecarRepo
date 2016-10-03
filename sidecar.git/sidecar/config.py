server = {
    'port': '9090',
    'host': 'api.stage1.nephoscale.com'
}

# Pecan Application Configurations
app = {
    'root': 'sidecar.controllers.root.RootController',
    'modules': ['sidecar'],
    'debug': True
}

