# Übung 06 – Volumes: `emptyDir` vs. PVC (Persistenz verstehen)

## Ziel

- `emptyDir`: Daten existieren nur solange der Pod existiert
- PVC: Daten überleben Pod-Neustart/Neuerstellung (im Rahmen des Storage-Backends)

## Dauer

35–55 Minuten

---

## Teil A – `emptyDir` (ephemeral)

### Schritt 1 – Pod mit `emptyDir` erstellen

Erstelle `emptydir-pod.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: writer-emptydir
spec:
  containers:
    - name: writer
      image: busybox:1.36
      command: ["sh", "-c", "while true; do date >> /data/log.txt; sleep 5; done"]
      volumeMounts:
        - name: data
          mountPath: /data
  volumes:
    - name: data
      emptyDir: {}
```

```powershell
kubectl apply -f .\emptydir-pod.yaml
kubectl get pod writer-emptydir
```

### Schritt 2 – Datei prüfen

```powershell
kubectl exec writer-emptydir -- tail -n 5 /data/log.txt
```

### Schritt 3 – Pod löschen und neu erstellen

```powershell
kubectl delete pod writer-emptydir
kubectl apply -f .\emptydir-pod.yaml
kubectl exec writer-emptydir -- ls -la /data
```

**Erwartung:** Die alte Datei ist weg (weil `emptyDir` an den Pod gebunden ist).

---

## Teil B – PVC (persistent)

### Schritt 1 – PVC erstellen

Erstelle `data-pvc.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 128Mi
```

```powershell
kubectl apply -f .\data-pvc.yaml
kubectl get pvc data-pvc
```

**Erwartung:** Status wird `Bound` (kann kurz dauern).

### Schritt 2 – Pod mit PVC erstellen

Erstelle `pvc-pod.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: writer-pvc
spec:
  containers:
    - name: writer
      image: busybox:1.36
      command: ["sh", "-c", "while true; do date >> /data/log.txt; sleep 5; done"]
      volumeMounts:
        - name: data
          mountPath: /data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: data-pvc
```

```powershell
kubectl apply -f .\pvc-pod.yaml
kubectl exec writer-pvc -- tail -n 5 /data/log.txt
```

### Schritt 3 – Pod löschen und wieder erstellen (Daten bleiben)

```powershell
kubectl delete pod writer-pvc
kubectl apply -f .\pvc-pod.yaml
kubectl exec writer-pvc -- tail -n 5 /data/log.txt
```

**Erwartung:** Die Datei existiert weiter und enthält alte Einträge.

---

## Dashboard-Schritte

Im Dashboard (Namespace `training`):

1. **Storage → PersistentVolumeClaims** öffnen → `data-pvc` ist `Bound`
2. Pod `writer-pvc` öffnen → **Volumes** prüfen
3. Pod neu starten/löschen → PVC bleibt bestehen

---

## Best Practice (kurz)

- In echten Projekten ist „State“ oft außerhalb von Kubernetes (DB/Objektspeicher). Wenn stateful in Kubernetes: dann bewusst mit PVC/StatefulSet.
- PVCs werden über **StorageClasses** provisioniert (Cloud/On-Prem unterschiedlich).

