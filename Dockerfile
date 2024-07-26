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
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
