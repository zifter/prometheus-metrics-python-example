set -e
REGISTRY=${1}
VERSION=${2:-"local"}

echo $VERSION

TAG=${REGISTRY}/example-metrics-app:${VERSION}

docker build . --tag $TAG
docker push $TAG
docker rmi -f $TAG
