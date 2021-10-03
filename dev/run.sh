#!/bin/bash
set -e

WORKDIR=$(realpath "$(dirname "$0")")
echo "WORKDIR ${WORKDIR}"

pushd $WORKDIR

./setup.sh
helmfile sync

popd

echo "==========================================================="
echo "Grafana:        http://localhost:1080/grafana (admin - admin)"
echo "Prometheus:     http://localhost:1080/prometheus"
echo "Alert Manager:  http://localhost:1080/alertmanager"
echo "Metrics:        http://localhost:1080/example-metrics"
echo "==========================================================="
