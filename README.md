Things I would implement given more time

 - More robust error handling
 - TLS possibly via a kubernetes ingress and DNS Made Easy
 - Swagger to provide basic documentation

Things I would consider if the app were to be productionized
 - Extraction of Environment Variables and Secrets and Storage in AWS Parameter/Secret Store
 - Auto-scaling based on CPU usage or number of requests
 - Deployment in other regions and routing via CloudFront or a similar Geo service (Azure Traffic Manager)

# Infrastructure Planning

Due to the short development and deployment timeframe I have chosen EKS for this deployment as I am already familiar with it. If more planning was possible I might have chosen ECS or Lambda for this task. The application is stateless so there is no need for a data base or storage solution.

# Scaling and Capacity

For this demonstration I have elected to run on a single node for cost purposes. However if I was to deploy this in the production environment I would consider using EKS's Cluster Autoscaler combined with pod Anti-Affinity settings to keep the workloads on seperate nodes. In regards to scaling the workload itself I would implement a horizontal pod autoscaler in the workload tied to the CPU and Memory metrics if there were no custom metrics for the application, however if the application did provide custom metrics I would look to work with the developer to estrablish thresholds for scaling.

In the case of a high traffic application we might consider decoupling the part of the application that recieves the requests and using an event queue to to make sure that connections don't need to be held open while we wait for capacity on the backend. In this case we would provide a callback url and have a seperate service provide the final response when it is available.

# Security

At the moment there is a simple check of an API Key header to gate access to the service. This is standing in for a much more elaborate deployment that would include OAuth integration. If we were sticking with EKS for this deployment the easiest implementation would be an oauth2 proxy pod with an ingress taking the place of an application ingress. To expand this scope further tokens and accounts would be assigned to specific users to allow for metered billing, rate limiting and logging of usage patterns.

In regards to further security measures, certainly a WAF policy attached to the Load Balancer would be a requirement along with a rate limiting implemtation. In highly secure cases the API might be split into multiple segments, each controlling authentication, handing requests and calling backend services.  