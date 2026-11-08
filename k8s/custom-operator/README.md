# Custom operator for Kubernetes

## init project
```sh

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## check connection with k8s
```sh
# TODO: start K3S/K8S locally 
kubectl config current-context
kubectl cluster-info
kubectl get nodes
```

```sh
python -c "
from kubernetes import config
config.load_kube_config()
print('Kubernetes authentication configured')
"
```

## create new K8S resource type
```sh
kubectl apply -f crd.yaml
```

## create new custom resource
```sh
kubectl apply -f custom-operator.yaml
```

## Kopf development mode run
```sh
kopf run operator.py --verbose
```