# Base image with Python
FROM python:3.11 AS base

# Set the working directory
WORKDIR /app

# Copy the dependency files
COPY config/config.yaml params.yaml /app/config/
COPY ./src/plant_disease_classification/pipeline /app/src/plant_disease_classification/pipeline

# Install necessary packages
RUN pip install --upgrade pip && \
    pip install -r /app/src/plant_disease_classification/pipeline/requirements.txt

# Data Ingestion Stage
FROM base AS data_ingestion
COPY ./src/plant_disease_classification/pipeline/data_ingestion_pipeline.py /app/src/plant_disease_classification/pipeline/
RUN python ./src/plant_disease_classification/pipeline/data_ingestion_pipeline.py

# Base Model Preparation Stage
FROM data_ingestion AS base_model_preparation
COPY ./src/plant_disease_classification/pipeline/data_preparebasemodel_pipeline.py /app/src/plant_disease_classification/pipeline/
RUN python ./src/plant_disease_classification/pipeline/data_preparebasemodel_pipeline.py

# Training Base Model Stage
FROM base_model_preparation AS training_base_model
COPY ./src/plant_disease_classification/pipeline/model_training_pipeline.py /app/src/plant_disease_classification/pipeline/
RUN python ./src/plant_disease_classification/pipeline/model_training_pipeline.py

# Evaluation Stage
FROM training_base_model AS evaluation
COPY ./src/plant_disease_classification/pipeline/model_evaluation_pipeline.py /app/src/plant_disease_classification/pipeline/
RUN python src/plant_disease_classification/pipeline/model_evaluation_pipeline.py

# Web Application Stage
FROM python:3.11 AS web_application_app
WORKDIR /app
COPY . /app

# Set environment variable for Django secret key
ENV SECRET_KEY =

# Set GitHub PAT environment variable
ARG GITHUB_PAT
ENV GITHUB_PAT=${GITHUB_PAT}

# Troubleshooting step: Verify the presence of requirements.txt
RUN ls -la /app/requirements.txt

# Install required packages
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Clone the GitHub repository using PAT
RUN git clone https://${GITHUB_PAT}@github.com/mauriceoboya/Plant_Disease_Classification.git /app/src/plant-disease-classification

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
