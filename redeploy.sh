docker build -t printf-api:dev backend                               
kind load docker-image printf-api:dev
kubectl rollout restart deploy/backend
kubectl port-forward svc/backend 8000:80