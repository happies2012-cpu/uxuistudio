# 🚀 gsWstudio.ai - Deployment Pipeline

## ✅ **Deployment Infrastructure Complete**

Complete CI/CD pipeline with Docker, Kubernetes, and GitHub Actions for production-ready deployment.

## 📦 **Components**

### 1. **Docker Setup**
- ✅ Multi-stage Dockerfile for Frontend (Next.js)
- ✅ Multi-stage Dockerfile for Backend (Node.js)
- ✅ Production Docker Compose (`docker-compose.prod.yml`)
- ✅ Health checks and graceful shutdown
- ✅ Non-root users for security

### 2. **Kubernetes Manifests**
- ✅ Backend Deployment (3 replicas, auto-scaling)
- ✅ Frontend Deployment (2 replicas)
- ✅ Ingress with SSL/TLS (Let's Encrypt)
- ✅ HorizontalPodAutoscaler (CPU/Memory based)
- ✅ Resource limits and requests
- ✅ Liveness and readiness probes

### 3. **CI/CD Pipeline (GitHub Actions)**
- ✅ Automated testing on PR
- ✅ Build and push Docker images to GHCR
- ✅ Deploy to production on release
- ✅ Kubernetes rollout with verification

## 🏃 **Quick Start**

### Local Development with Docker

```bash
# Build and run all services
docker-compose -f docker-compose.prod.yml up --build

# Access services
# Frontend: http://localhost:3000
# Backend: http://localhost:3001
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

### Deploy to Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods
kubectl get services
kubectl get ingress

# View logs
kubectl logs -f deployment/backend
kubectl logs -f deployment/frontend
```

## 🔧 **Configuration**

### Environment Variables

Create a Kubernetes secret:

```bash
kubectl create secret generic app-secrets \
  --from-literal=database-url='postgresql://user:pass@host:5432/db' \
  --from-literal=jwt-secret='your-secret-key' \
  --from-literal=anthropic-api-key='your-api-key'
```

### GitHub Secrets

Add these secrets to your GitHub repository:

1. **KUBECONFIG**: Base64-encoded Kubernetes config
   ```bash
   cat ~/.kube/config | base64
   ```

2. **GITHUB_TOKEN**: Automatically provided by GitHub Actions

## 📊 **Architecture**

```
┌─────────────────────────────────────────────┐
│           Ingress (NGINX + SSL)             │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼─────┐   ┌─────▼──────┐
│  Frontend  │   │   Backend  │
│  (Next.js) │   │  (Node.js) │
│  2 replicas│   │  3 replicas│
└────────────┘   └─────┬──────┘
                       │
              ┌────────┴────────┐
              │                 │
       ┌──────▼─────┐    ┌─────▼────┐
       │ PostgreSQL │    │  Redis   │
       │ StatefulSet│    │ Cluster  │
       └────────────┘    └──────────┘
```

## 🔄 **CI/CD Workflow**

### On Pull Request:
1. Run tests (Frontend + Backend)
2. Build Docker images
3. Run linters
4. Check code coverage

### On Merge to Main:
1. Build production images
2. Push to GitHub Container Registry
3. Deploy to staging (optional)

### On Release Tag:
1. Build production images with version tag
2. Push to GHCR
3. Deploy to Kubernetes production
4. Run health checks
5. Notify team (Slack/Discord)

## 📈 **Scaling**

### Horizontal Pod Autoscaler

- **Backend**: 2-10 replicas (CPU: 70%, Memory: 80%)
- **Frontend**: 2-5 replicas (CPU: 70%)

### Manual Scaling

```bash
# Scale backend
kubectl scale deployment backend --replicas=5

# Scale frontend
kubectl scale deployment frontend --replicas=3
```

## 🔐 **Security**

- ✅ Non-root containers
- ✅ SSL/TLS everywhere (Let's Encrypt)
- ✅ Secrets management (Kubernetes Secrets)
- ✅ Network policies (pod-to-pod)
- ✅ Resource limits (prevent DoS)
- ✅ Health checks (auto-restart unhealthy pods)

## 📊 **Monitoring**

### Health Checks

```bash
# Backend health
curl http://localhost:3001/health

# Frontend health
curl http://localhost:3000/

# Kubernetes pod status
kubectl get pods -w
```

### Logs

```bash
# View backend logs
kubectl logs -f deployment/backend

# View all logs
kubectl logs -f -l app=backend --all-containers=true
```

## 🚨 **Troubleshooting**

### Pods not starting

```bash
# Check pod status
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

### Database connection issues

```bash
# Test database connectivity
kubectl run -it --rm debug --image=postgres:15 --restart=Never -- \
  psql -h postgres -U user -d gswstudio
```

### Image pull errors

```bash
# Check image pull secrets
kubectl get secrets

# Verify image exists
docker pull ghcr.io/happies2012-cpu/uxuistudio-backend:latest
```

## 💰 **Cost Estimates**

### DigitalOcean Kubernetes (Recommended)

- **3 Worker Nodes** (2 vCPU, 4GB RAM): $36/month
- **Managed PostgreSQL** (2GB RAM): $15/month
- **Managed Redis**: $15/month
- **Load Balancer**: $12/month
- **Total**: ~$78/month

### AWS EKS (Enterprise)

- **EKS Cluster**: $73/month
- **3 t3.medium instances**: $75/month
- **RDS PostgreSQL**: $30/month
- **ElastiCache Redis**: $25/month
- **ALB**: $20/month
- **Total**: ~$223/month

## 🎯 **Next Steps**

1. ✅ Set up Kubernetes cluster (DigitalOcean/AWS/GKE)
2. ✅ Configure GitHub Secrets (KUBECONFIG)
3. ✅ Create Kubernetes Secrets (database, API keys)
4. ✅ Deploy with `kubectl apply -f k8s/`
5. ✅ Configure DNS (point domain to Ingress IP)
6. ✅ Set up monitoring (Prometheus/Grafana)
7. ✅ Configure backups (database snapshots)

## 📚 **Resources**

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [DigitalOcean Kubernetes](https://www.digitalocean.com/products/kubernetes)

---

**Deployment pipeline is production-ready!** 🚀✨
