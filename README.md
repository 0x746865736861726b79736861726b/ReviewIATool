# How to run 
 I guess its not about the code repo.

`docker-compose build && docker-compose up`

# For What If

For handling 100+ request, users etc.
 ***Backend optimizations***
 It will be great to use async task queues like (Celery, AWS SQS, or RebbitMQ). Logs we can store in services like AWS S3. Using multiple worker nodes to handle LangChain calls and Github API interactions. So for those tasks we can use LangChain to fetch repository content and than split it intro small chunks for better handling. When we process repo with OpenAI we can store embeddings in vector database such as Pinecone, Weaviate, Qdrant for quick reference and partial reviews. Run LangChain workflows on destributed workers to process multiple code files concurrently. For cache responses we can use Redis to cache frequently requested data(Github metadata). For optimazing AI model usage we can batch similar requests into a single API call, its great if multiple users request reviews for the same repository. Process smaller chunks of code with clear prompts to minimize token consumption. Switch to dedicated APIs like Anthropic, Cohere, or OpenAI’s enterprise API for more predictable scaling.

So technology stack can be like this

| Component    | Tool/Technology |
| -------- | ------- |
| API Layer  | FastAPI, AWS Lambda    |
| LangChain Integration | LangChain + OpenAI     |
| Asynchronous Queue    | Celery, RabbitMQ, or AWS SQS    |
|Worker Execution|  Kubernetes, AWS Fargate|
|Object Storage | AWS S3 |
|Vector Database for Embeddings| Pinecone, Weaviate |
|Load Balancer | AWS ELB, NGINX |
|Cache | Redis |