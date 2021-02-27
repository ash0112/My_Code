Deploy application on AWS ECS via ECR
- Build the image using the following command
`docker build -t aws_dep_hello_world .`
- Run the Docker container using the command shown below.
`docker run -d -p 5000:5000 aws_dep_hello_world`
