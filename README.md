Install the dependencies; this creates a Conda env named `langchain-aws-service-openai` and activates it.
```bash
conda deactivate
conda env create -f environment.yml # only needed once
conda activate langchain-aws-service-openai
```


Build and Push the Docker image to AWS ECR repository: 

1- Use the following steps to authenticate and push an image to your repository. For additional registry authentication methods, including the Amazon ECR credential helper, see Registry Authentication .
Retrieve an authentication token and authenticate your Docker client to your registry.
Use the AWS CLI:

```bash
aws ecr get-login-password --region <AWS_region>| docker login --username AWS --password-stdin <account_id>.dkr.ecr.<AWS_region>.amazonaws.com/llm-cur:latest

```
Note: If you receive an error using the AWS CLI, make sure that you have the latest version of the AWS CLI and Docker installed.

2- Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here . You can skip this step if your image is already built:

```bash
docker build -t llm-cur .
```

3- After the build completes, tag your image so you can push the image to this repository:

```bash
docker tag llm-cur:latest <account_id>.dkr.ecr.<AWS_region>.amazonaws.com/llm-cur:latest
```

4- Run the following command to push this image to your newly created AWS repository:
```bash
docker push <account_id>.dkr.ecr.<AWS_region>.amazonaws.com/llm-cur:latest

```

Deploy the Docker to AWS ECS: 
for more details please visit the AWS documentation https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_run_task.html 

Note: Once you have the task deployed, copy the task public IP. 


Move to the webapp directory
```bash
cd webapp
```

Update the `<your-api-endpoint>` in `api.py` to the ECS task public IP 

Start the web application
```bash
streamlit run app.py
```