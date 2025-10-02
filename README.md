# alcatraz-api

## Application

Application and docker-related files are in the /app directory.

## Terraform

Deploying the application is done manually with terraform.

You can deploy the infrastructure with:

`terraform init`

`terraform plan`

`terraform apply`

## LB testing tool

Tool is located in /tool directory and used as: 

`./tool.py -u $URL-where-app-is-running -r $number-of-requests`

## Workflows

Build is automatic on push to main branch and produces a container image uploaded to ghcr.io.