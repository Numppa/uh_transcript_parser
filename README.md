# uh_transcript_parser
A simple parsing tool to convert a University of Helsinki transcript of studies into CSV. 
This tool is meant to speed up the process of reviewing stipend applications.


## Backend

Runs FastAPI deployed to port 5000. There's a single enpoint `/parse` which accepts POST requests with PDF file uploads. 

Uses pdftotext to convert the PDF into text. The text is converted to CSV with a custom parser

## Frontend

A single HTML page (with some JavaScript) served by nginx. Connects to backend via localhost:5000. 

## Deployment

### Local

Use `docker compose up`

You now should have the service running in `localhost:8080`. 

### AWS 

The app can be deployed to AWS by using Terraform with ECR and ECS. 

First, create a container registry by applying `/terraform/ecr`. Then, go to the AWS console and follow the instructions to push the images to the registry. Basically, you need to login to ECR, `docker compose build`, then tag the images with `docker tag`, and then `docker push`. 

Register a domain, Create a certificate, and create a hosted zone. 

Apply `terraform/service`. 

You now should have the sercvice running in `<domain-name>:443`

