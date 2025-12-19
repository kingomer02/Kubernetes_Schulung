# Helm

Dieser Ordner enthält Helm-Material für die Schulung:

- `helm/sushi-bar/` – Helm Chart für die Mini‑Projekt App (Frontend/Backend)

Typische Helm-Workflows (für die Übungen):
- `helm lint helm/sushi-bar`
- `helm template sushi helm/sushi-bar`
- `helm install sushi helm/sushi-bar -n sushi-helm --create-namespace`
- `helm upgrade sushi helm/sushi-bar -n sushi-helm --set frontend.replicaCount=2`
- `helm rollback sushi 1 -n sushi-helm`

Optional (Dashboard via Helm, wenn nicht installiert):
- `helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/`
- `helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard -n kubernetes-dashboard --create-namespace`

