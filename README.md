# Kubernetes Logging Application

## Overview

This project implements a simple Kubernetes-based application that demonstrates:

 1. Scheduled background processing using Kubernetes CronJobs
 2. Persistent data storage using Persistent Volumes
 3. A containerized HTTP API to expose stored data
 4. Service-based access to the application

A CronJob runs every minute and appends the current date and time to persistent storage.  

A separate API service exposes an HTTP endpoint that allows clients to retrieve the last **N** recorded timestamps as JSON.

The solution is designed to be reproducible locally using **Minikube**.



## Design 

The architecture was developed by first understanding the problem requirements and then selecting the simplest Kubernetes services that's required.


### Scheduled Execution

Since the application requires a task to run every minute, a Kubernetes **CronJob** is chosen as it provides a built-in mechanism for time-based execution. Each scheduled run creates a Job and a short-lived Pod that performs the write operation, which keeps the responsibility of the writer component small and defined.


### Persistent Data Storage

Because Pods in Kubernetes are short-lived and can be restarted or rescheduled at any time, writing data to a Pod’s filesystem would not be reliable. To ensure that timestamps is saved across executions and restarts, a **PersistentVolumeClaim (PVC)** is used. This allows both the scheduled writer job and the API service to share access to the same storage.


### Service Endpoint and Data Retrieval

To make the stored data accessible to user, a continuously running HTTP service is required. A Kubernetes **Deployment** is used to run a containerized API that reads from the persistent volume and exposes an endpoint that returns the last **N** recorded timestamps as a JSON response. Using a Deployment ensures the service is self-healing and remains available even if a Pod is restarted.


### Simplicity and Reproducibility

The overall design avoids unnecessary complexity. Only Kubernetes resources are used and the API is packaged as a Docker image using a Dockerfile. This keeps the solution easy to understand, straightforward to deploy and fully reproducible in a local Minikube environment or a managed Kubernetes cluster.


## Architecture FlowChat

```text
Client (Curl)
     ^
     |
Kubernetes Service
     ^
     |
API Deployment
     |  
     |   reads
     v
Persistent Volume (PVC)
     ^
     |  writes
     |
CronJob (Every minute)
```

## How to Deploy

### Prerequisites

   - Docker Desktop (with WSL2 backend enabled)

   - Minikube

   - kubectl


### Deployment Steps


#### 1. Start the local Kubernetes cluster:

     minikube start


#### 2. Build the Docker image inside Minikube’s Docker daemon:


   This step ensures that Kubernetes can access the custom image without pushing it to an external registry.

#### Windows PowerShell:
   
     minikube -p minikube docker-env | Invoke-Expression
     docker build -t cronlogger-api:local ./app

#### Linux/macOS:

     eval $(minikube -p minikube docker-env)
     docker build -t cronlogger-api:local ./app


#### 3. Deploy all Kubernetes manifests:

     kubectl apply -f ./k8s

 
#### 4. Verify that the resources are running:

     kubectl get pods 
     kubectl get cronjobs
     kubectl get jobs
     kubectl get pvc
     kubectl get svc

 Expected state:
   - API pod is Running
   - CronJob is present
   - Jobs are created every minute and marked Complete
   - PVC is Bound



## How to CURL the service

 ### Expose the API locally using port-forwarding:

     kubectl port-forward svc/cronlogger-api 8080:80

 ### Query the endpoint using curl in new PowerShell Window (.exe will give the exact data):

     curl.exe http://localhost:8080/outputs?limit=5
 
 ### For Linux/macOS:
  
    curl http://localhost:8080/outputs?limit=5

You can change the value of the "limit" query parameter to retrieve a different number of recent timestamps (e.g., limit=10 to return the last 10 entries).

**Sample API response with limit=5:**
<p align="left">
  <img src="images/output.jpg" alt="Sample output with limit=5" width="750">
</p>


## Assumptions
  
  1. The application assumes a single writer process and concurrent writes are not required.
  2. Timestamp data volume is small. 
  3. A flat file stored on persistent volume storage is sufficient.
  4. The API performs read only access to the shared storage.
  5. Authentication and authorization are not considered for this test.
  6. The solution runs on local kubernetes cluster (Minikube) for demonstaration and testing purposes.
   


## Additional Work for Production Environment
  
 To run this application in production, the following improvements would be made:

 1. Run the application on a managed Kubernetes platform (such as EKS, AKS or GKE) instead of a local cluster.
 2. Expose the API using an Ingress with HTTPS rather than using port-forwarding.
 3. Add health checks so Kubernetes can detect when the API is unhealthy and restart it automatically.
 4. Define CPU and memory limits for the API pod to ensure stable performance and fair resource usage.
 5. Add basic monitoring and logging to observe API behavior and detect failures in the scheduled jobs.
 6. Improve security by running containers as non-root users and storing sensitive configuration in Kubernetes Secrets.
 7. Replace file-based storage with a database or shared storage solution if data volume or concurrency increases.
 8. Add a CI/CD pipeline to automatically build, test and deploy new versions of the application.


## Use of LLM-Based Tools

 LLM-based tool Chatgpt was used as a supporting tool during this code challenge. It was helpful in refining documentation wording, clarifying Kubernetes concepts and sanity-checking configuration against common best practices. All design decisions, implementation, debugging and validation was done manually and the solution was tested end-to-end to ensure it behaves correctly and can be reproduced.

