This repository demonstrates how to utilize LangChain Agents and large language models (LLMs) to extract insights from numeric tabular data through natural language queries. We specifically focus on the AWS Cost and Usage Report (CUR) as our data source in this example.

## Install the dependencies 
This creates a Conda env named `langchain-aws-service-openai` and activates it.
```bash
conda deactivate
conda env create -f environment.yml # only needed once
conda activate langchain-aws-service-openai
```


## Build and Push the Docker image to AWS ECR repository: 

Use the following steps to authenticate and push an image to your repository. For additional registry authentication methods, including the Amazon ECR credential helper, see Registry Authentication .

### 1- Retrieve an authentication token and authenticate your Docker client to your registry.
Use the AWS CLI:

```bash
aws ecr get-login-password --region <AWS_region> | docker login --username AWS --password-stdin <account_id>.dkr.ecr.<AWS_region>.amazonaws.com/llm-cur:latest

```
Note: If you receive an error using the AWS CLI, make sure that you have the latest version of the AWS CLI and Docker installed.

### 2- Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here . You can skip this step if your image is already built:

```bash
docker build -t llm-cur .
```

### 3- After the build completes, tag your image so you can push the image to this repository:

```bash
docker tag llm-cur:latest <account_id>.dkr.ecr.<AWS_region>.amazonaws.com/llm-cur:latest
```

### 4- Run the following command to push this image to your newly created AWS repository:
```bash
docker push <account_id>.dkr.ecr.<AWS_region>.amazonaws.com/llm-cur:latest

```
## Deploy the Docker container to AWS ECS:
For more details please visit the AWS documentation https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_run_task.html

### 1. Create an ECS cluster:
- Open the Amazon ECS console.
- Choose "Create Cluster".
- Select the cluster template (e.g., "EC2 Linux + Networking") and click "Next step".
- Provide a cluster name and configure other settings as needed.
- Click "Create" to create the cluster.

### 2. Create a task definition:
- In the Amazon ECS console, choose "Task Definitions" from the navigation pane, and then click "Create new Task Definition".
- Select "EC2" as the launch type compatibility and click "Next step".
- Provide a task definition name and configure other settings such as the task role, network mode, and container definitions.
- Under "Container Definitions", click "Add container".
- Provide a container name, and enter the image URI from your ECR repository (e.g., <account_id>.dkr.ecr.<AWS_region>.amazonaws.com/llm-cur:latest).
- Configure other container settings, such as memory limits, port mappings, and environment variables.
- Click "Add" to add the container to the task definition, and then click "Create" to create the task definition.

### 3. Run a task using the task definition:
- In the Amazon ECS console, choose "Clusters" from the navigation pane, and then select the cluster you created earlier.
- Click the "Tasks" tab, and then click "Run new Task".
- Select the "EC2" launch type and choose the task definition you created in step 2.
- Configure other settings such as the VPC, security groups, and IAM role.
- Click "Run Task" to launch the task.

### 4. Access the task's public IP:
- In the "Tasks" tab of your cluster, click on the task ID of the running task.
- In the "Task Details" section, you'll find the "Public IP" address of the task. Use this IP address to connect your local Streamlit app to the deployed Docker container.



## Run the local Streamlit UI 
### Move to the webapp directory
```bash
cd webapp
```

### Update the `<your-api-endpoint>` in `api.py` to the ECS task public IP 

### Start the web application
```bash
streamlit run app.py
```

![](webapp/images/aws_cur_data.gif)