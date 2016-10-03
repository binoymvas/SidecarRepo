from sidecarclient import client

sidecar = client.Client(
    auth_version = 2,
    username = "admin",
    password = "5d6baead492b",
    endpoint = "https://api.stage1.nephoscale.com:9090/v2",
    auth_url = "https://api.stage1.nephoscale.com:5000/v2.0",
    endpoint_type="publicURL",
    region_name = "stage1",
    tenant_name = "admin",
    timeout = 10,
    insecure = False
)

print "###############################################################"
print "# HealthCheck for Events                                      #"
print "###############################################################"
events = sidecar.events.evacuate_healthcheck()
