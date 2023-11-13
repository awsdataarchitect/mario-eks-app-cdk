# Open source example code for Music Note Transcription on Amazon ECS Fargate with TensorFlow based Deep Learning Model

This is a CDK project written in TypeScript that provisions a Streamlit UI based Music Sheet Transcriber (Music Notes Annotator) App powered by Tensorflow Machine Learning Model running on an ECS Fargate Cluster in a VPC with Public Subnets and associated IAM Roles/Policies, Security Groups, Route Tables, Internet Gateway and an Application Load Balancer.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template
