import sys, json, os;

# - targets:
#     - 'gew1-mattivespa10content-contenta-677b.gew1.spotify.net:19092'
#   labels:
#     group: 'a'



service_types = [
    "qrserver",
    "searchnode",
    "container",
    "configserver",
]


def extract_service(hosts, matching_service_type, prometheus_port=19092):
    for host in hosts:
        for service in host['services']:
            service_name = service['name']
            service_type = service['type']
            if service_type == matching_service_type:
                hostname = host['name']
                hostname_parts=hostname.split('-')
                pod=hostname_parts[0]
                role=hostname_parts[1]
                pool=hostname_parts[2]
                clustername = service['clustername']
                print(f"      - targets:")
                print(f"          - '{hostname}:{prometheus_port}'")
                print(f"        labels:")
                print(f"          service_name: '{service_name}'")
                print(f"          role: '{role}'")
                print(f"          pod: '{pod}'")
                print(f"          pool: '{pool}'")
    

data = json.load(sys.stdin)

scrape_interval=os.getenv("scrape_interval", default="15s")
evaluation_intrveal=os.getenv("scrape_interval", default=scrape_interval)


print("global:")
print(f"  scrape_interval:     {scrape_interval}")
print(f"  evaluation_interval: {evaluation_intrveal}")
print("")
print("  # Attach these labels to any time series or alerts when communicating with")
print("  # external systems (federation, remote storage, Alertmanager).")
print("  external_labels:")
print("      monitor: 'vespa-local-grafana'")
print("")
print("# Load and evaluate rules in this file every 'evaluation_interval' seconds.")
print("rule_files:")
print("  - \"alert.rules\"")
print("")
print("# A scrape configuration containing exactly one endpoint to scrape.")
print("scrape_configs:")
print("")
print("  - job_name: 'vespa'")
print("    scrape_interval: 30s")
print("    metrics_path: /prometheus/v1/values")
print("    static_configs:")
for service_type in service_types:
    extract_service(data['hosts'], service_type)

#
# Enable the part below if you have prometheus node exporter enabled on your hosts
#
#print("  - job_name: 'system'")
#print("    scrape_interval: 30s")
#print("    metrics_path: /metrics")
#print("    static_configs:")
#for service_type in service_types:
#    extract_service(data['hosts'], service_type, prometheus_port=9100)

