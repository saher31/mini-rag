# mini-rag

this is a minimal implementation of a RAG model for question answering

## Requirements
- python 3.8 or later

#### Install python using conda
1) install miniconda or anaconda from [here](https://docs.conda.io/en/latest/miniconda.html)
2) create a new environment
```bash
conda create -n mini-rag python=3.11
```
3) activate the environment
```bash
conda activate mini-rag
```
## Installation

### Install the required packages
```bash
pip install -r requirements.txt
```

### setup the environment variables
```bash
cp .env.example .env
```
set your environment vartables in the .env file. Like `OPENAI_API_KEY` value.

## Run the server
```bash
uvicorn main:app --reload --host [IP_ADDRESS] --port 5050
```

## Run the FastAPI server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5050
```

## POSTMAN Collection
Download the POSTMAN collection from [here](assets/mini-rag-app.postman_collection.json)
