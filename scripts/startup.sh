#!/bin/bash
set -e

echo "======================================"
echo " Starting Redis + FastAPI Environment "
echo "======================================"

K8S_DIR="../k8s"

echo ""
echo "Applying Redis ConfigMap..."
kubectl apply -f "$K8S_DIR/redis-configmap.yaml"

echo "Applying Redis Secret..."
kubectl apply -f "$K8S_DIR/redis-secret.yaml"

echo "Applying Redis PVC..."
kubectl apply -f "$K8S_DIR/redis-pvc.yaml"

echo "Applying Redis Deployment..."
kubectl apply -f "$K8S_DIR/redis-deployment.yaml"

echo "Applying Redis Service..."
kubectl apply -f "$K8S_DIR/redis-service.yaml"

echo ""
echo "Applying FastAPI Service..."
kubectl apply -f "$K8S_DIR/service-fastapi.yaml"

echo "Applying FastAPI Deployment..."
kubectl apply -f "$K8S_DIR/deployment.yaml"

echo ""
echo "Applying Ingress..."
kubectl apply -f "$K8S_DIR/ingress.yaml"

echo ""
echo "Waiting for all pods to be ready..."
kubectl wait --for=condition=ready pod -l app=redis --timeout=60s
kubectl wait --for=condition=ready pod -l app=python-api --timeout=60s

echo ""
echo "All resources applied successfully!"
echo "You can now test your API at http://localhost/api"


