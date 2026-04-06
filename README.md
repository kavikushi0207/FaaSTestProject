Resume/JD Matcher API: A FaaS Performance Evaluation

📌 Project Overview

This project implements a Serverless HTTP API designed to analyze resumes against job descriptions (JD). It utilizes Natural Language Processing (NLP) to return a match score and identifies "skill gaps" to provide career insights. The core objective of this study is to benchmark Function-as-a-Service (FaaS) behaviors, specifically focusing on cold vs. warm start latency, horizontal scaling, and resource management within a Kubernetes environment.

🏗 System Architecture

The system follows a containerized microservices pattern:


* Serverless API: Developed using Azure Functions (Python V2).


* NLP Engine: Built with Scikit-learn using TF-IDF Vectorization and Cosine Similarity.


* Containerization: Packaged via Docker (emulated for linux/amd64 compatibility).


* Orchestration: Managed by Kubernetes (Minikube) with automated scaling.


🚀 Getting Started

 Prerequisites
 
* Docker Desktop

* Minikube & kubectl

* Azure Functions Core Tools

Deployment Steps

1. Build the Image:

   ```
    docker build --platform linux/amd64 -t resume-matcher-v1 .
   ```
   
3. Initialize Cluster:
   ```
    minikube start --driver=docker
    minikube image load resume-matcher-v1
   ```
5. Deploy to Kubernetes:
   ```
    kubectl apply -f deployment.yaml
   ```
7. Access the API:

   ```
    minikube service resume-matcher-service --url
   ```

📊 Performance Evaluation Metrics

As part of our research, we are supposed to evaluate the following metrics:


* Cold Start Latency


* Warm Start Latency


* Scalability


* Reliability

🛠 Troubleshooting & Insights

* Auth Level: Set to ANONYMOUS for localized benchmarking to eliminate security handshake overhead.

* Resource Constraints: Identified that emulated x86_64 environments on ARM64 hosts require higher CPU/RAM quotas to prevent SIGABRT errors.

👥 Team

* **Member 1**: [Kavini Pathagamage](https://github.com/kavikushi0207): Infrastructure setup, Dockerization, K8s Orchestration, and CI/CD basics, Analyzing test results

* **Member 2**: [Taniya Afreen](https://github.com/taanyaafreen): Logic/Model development, Test dataset preparation, and Performance experiment design, Analyzing test results
