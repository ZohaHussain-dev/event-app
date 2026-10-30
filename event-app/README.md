# Campus Event Management - 3-Tier App (Jenkins + Kubernetes + Monitoring)

Tiers: Nginx frontend -> Flask backend -> PostgreSQL database.
Events: NESCON, ACM Hackathon, Execup, Visionspark.

## Run on the EC2 server (Jenkins + minikube on the SAME server)
1. Push this folder to your own GitHub repo (e.g. event-app).
2. Jenkins -> New Item -> Pipeline -> "Pipeline script from SCM" -> Git -> your repo URL, branch */main, Script Path: Jenkinsfile.
3. Build Triggers -> tick "GitHub hook trigger for GITScm polling". Add webhook in GitHub: http://<JENKINS-IP>:8080/github-webhook/
4. Click Build Now.
5. Open the site: kubectl -n event-app port-forward --address 0.0.0.0 svc/frontend 8081:80
   then browse http://<EC2-IP>:8081 (open port 8081 in the security group, or use an SSH tunnel).

## Monitoring (Task 3)
See the chat steps: helm install kube-prometheus-stack, then kubectl apply -f k8s/monitoring-servicemonitor.yaml
