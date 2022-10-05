#!/bin/bash
script_dir=$(dirname $([ -L $0 ] && readlink -f $0 || echo $0))
if [[ $(uname -o) == "Darwin" ]]; then
  script_dir="$(dirname "$(readlink "$0")")"
fi

cluster_config_endpoint=$1

function usage() {
  echo "USAGE $0 {vespa-config-endpoint}"
  echo ""
  echo "Example: $0 http://my-vespa-cluster-config.our.domain.net:19071"
  echo ""
  exit 1
}

if [[ -z $cluster_config_endpoint ]]; then
  usage
fi

curl -s $cluster_config_endpoint/config/v2/tenant/default/application/default/cloud.config.model | \
   python3 $script_dir/prometheus_gen_config.py
