# mini-rag

this is a minimal implementation of a RAG model for question answering

## Requirements
- python 3.8 or later

#### Install python using conda
1) install miniconda or anaconda from [here](https://docs.conda.io/en/latest/miniconda.html)
2) create a new environment
```bash
conda create -n mini-rag python=3.8
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
