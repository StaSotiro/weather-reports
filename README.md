# weather-reports

### Help from

- https://help.dreamhost.com/hc/en-us/articles/115000695551-Installing-and-using-virtualenv-with-Python-3
- https://medium.com/bi3-technologies/creating-python-deployment-package-for-aws-lambda-function-25205f033ac5
- https://www.serverless.com/blog/serverless-python-packaging

- The provided execution role does not have permissions to call CreateNetworkInterface on EC2
  Attached policy AWSLambdaVPCAccessExecutionRole to allow the lambda function to make changes in the VPC - Now Lambda and DB are in the same VPC and can can access each other

- https://aws.amazon.com/premiumsupport/knowledge-center/internet-access-lambda-function/ Allow Lambda to perform outbound requests
- https://stackoverflow.com/questions/56895635/aws-lambda-timeout-when-making-external-https-request - Stopping since this requires about 32$ /mo
