# Open-source code for Deploying Super Mario Game on an EKS Cluster using CDK EKS Blueprints

This is a CDK project written in TypeScript that provisions an EKS Cluster using CDK EKS Blueprints and also the required Kubernetes EKS add-ons (VPC CNI and AWS Load Balancer) along with the Kubernetes manifests (Deployment, Service, Ingress) to launch the Dockerized version of the popular Super Mario Game.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template
