# vespa-local-grafana

This repo shows how you can use the [dockprom](https://github.com/stefanprodan/dockprom) Prometeus/Grafana stack to monitor your [Vespa.AI](https://vespa.ai/) cluster.

## Setup

In this directory clone the dockprom repo:

```
git clone https://github.com/stefanprodan/dockprom.git
```

## Generate prometheus config

You need to figure out one of your config nodes endpoint for the following to work. (The default port should be 19071)

Note also that you should at this point have deployed your application in the vespa cluster as the scripts below 
discovers the cluster topology vi a the vespa cluster model (which is only available once your application is deployed)

The script will also assume the default tenant and application (can easily be changed in the script if needed)

Generate the prometheus job config yaml:

```shell
./prometheus_gen_config.sh http://my-vespa-cluster-config.our.domain.net:19071 > ./dockprom/prometheus/prometheus.yml
```

## Start prometheus

```
cd dockprom
PASSWORD_HASH=JDJhJDE0JE91S1FrN0Z0VEsyWmhrQVpON1VzdHVLSDkyWHdsN0xNbEZYdnNIZm1pb2d1blg4Y09mL0ZP
ADMIN_USER=admin ADMIN_PASSWORD=admin ADMIN_PASSWORD_HASH=${PASSWORD_HASH} docker-compose up -d
```

If you need to set some other password please take a look at the instructions in the [dockprom repo](https://github.com/stefanprodan/dockprom) on how to generate a new password hash.

Then point your browser to prometheus or grafana:

Prometheus endpoint: http://localhost:9090

Grafana endpoint: http://localhost:3000 

(Username/password: admin/admin (if you use the hash above))


To see the logs for prometheus you can just:
```shell
docker logs -f prometheus
```

For details please read the docs at https://github.com/stefanprodan/dockprom

## Stop the services

```
docker rm -f alertmanager grafana cadvisor nodeexporter caddy prometheus pushgateway

# Remove all saved data
docker volume rm $(docker volume ls -q)
```

## Prometheus query samples

The samples below have been taken from trying our queries on the [semantic-vespa cluster](https://backstage.spotify.net/services/semantic-vespa)

### Document matching rate per index/documenttype 

```
avg by (documenttype) (content_proton_documentdb_matching_docs_matched_rate)
```

### Query setup-time per index for selected rank-profile

```
avg by (documenttype) (content_proton_documentdb_matching_rank_profile_query_setup_time_average{rankProfile="semantic_popularity_thresh"})
```

### Query number of documents per pool for document type

```
sum by (pool) (content_proton_documentdb_documents_total_last{documenttype="movement20220512"})
```

## Limitations

- This setup will ONLY monitor vespa metrics. 
If you need to monitor systems metrics as well you need to add the [prometheus node exporter](https://github.com/prometheus/node_exporter) for your nodes and add the endpoints to your generated `prometheus.yml` (There's some commented code in the [`prometheus_gen_config.py`](prometheus_gen_config.py) script that can help you with that)

- The script used in this repo has only been tested on Linux (Ubuntu 20.04 LTS)
