# Übung 06 – Helm: Deploy „Sushi‑Bar“ als Release (install/upgrade/rollback)

## Lernziel

- Helm Chart Struktur verstehen
- Einen Release installieren, updaten und zurückrollen
- Werte (`values`) nutzen, um Verhalten zu ändern (Replicas/Farbe/Version)

## Beschreibung

Du nutzt das Chart in `helm/sushi-bar/`, um die Sushi‑Bar App zu deployen. Danach machst du ein Upgrade (Skalierung + UI‑Farbe) und testest Rollback.

## Technische Aufgaben

### Vorab-Check (damit es nicht scheitert)

Das Chart nutzt standardmäßig lokale Images:

- `sushi-frontend:1.0`
- `sushi-backend:1.0`

Baue die Images jetzt:

- `docker build -t sushi-backend:1.0 .\\app\\backend`
- `docker build -t sushi-frontend:1.0 .\\app\\frontend`

### A) Helm Chart verstehen

Schau dir an:

- `helm/sushi-bar/Chart.yaml`
- `helm/sushi-bar/values.yaml`
- `helm/sushi-bar/templates/`

**Denkfrage:** Welche Werte würdest du in einem echten Projekt immer als `values.yaml` modellieren?

### B) Chart prüfen

- `helm lint helm/sushi-bar`
- (optional) `helm template sushi helm/sushi-bar | Select-String \"kind:\"`

### C) Install (Release v1)

- `kubectl create namespace sushi-helm`
- `helm install sushi helm/sushi-bar -n sushi-helm`

Status prüfen:

- `kubectl -n sushi-helm get deploy,po,svc`
- `helm status sushi -n sushi-helm`

Browser:

- Service-Name prüfen:
  - `kubectl -n sushi-helm get svc | Select-String frontend`
- Dann port-forward (bei Release-Name `sushi`):
  - `kubectl -n sushi-helm port-forward svc/sushi-sushi-bar-frontend 8080:80`
- `http://localhost:8080`

### D) Upgrade (Release v2)

1. Upgrade mit neuen Werten (Beispiele)

- `helm upgrade sushi helm/sushi-bar -n sushi-helm --set frontend.replicaCount=2 --set frontend.env.BG_COLOR=orange --set global.appVersion=v2`

2. Beobachten

- `kubectl -n sushi-helm get pods -o wide`
- `helm history sushi -n sushi-helm`

### E) Rollback

- `helm rollback sushi 1 -n sushi-helm`
- `helm history sushi -n sushi-helm`

## Erwartete Ergebnisse

- App läuft als Helm Release
- Upgrade ändert sichtbares Verhalten (z. B. BG_COLOR/Version/Replicas)
- Rollback stellt den alten Zustand wieder her

## Dashboard-Schritte

1. Namespace `sushi-helm` auswählen
2. Deployments → ReplicaSets (Revisionen) vergleichen
3. Labels prüfen: `app.kubernetes.io/instance=sushi`

## Troubleshooting

- **Port-forward auf Service geht nicht**: `kubectl -n sushi-helm get svc` und richtigen Service-Namen nehmen.
- **Rollback wirkt nicht**: `helm history` prüfen, ob Revision 1 existiert.

## Erweiterungsoptionen

- Packe das Chart: `helm package helm/sushi-bar` und installiere aus dem `.tgz`.
