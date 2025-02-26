# Dining Chatbot

## Introduction

A **serverless** chatbot application that provides restaurant recommendations based on user preferences.  
- **Currently supports restaurants in New York, Brooklyn, and Queens**, based on the collected dataset.
- **Email notifications are limited** to manually verified recipients due to **SES sandbox mode**.

**Try it out**: [Dining Chatbot](http://cs-gy-9223-dining-chatbot.s3-website-us-east-1.amazonaws.com/)

## System Architecture

### Data Collection & Storage
- **Yelp API**: Fetches restaurant data.
- **DynamoDB**: Stores full restaurant details.
- **OpenSearch**: Indexes restaurant records for fast lookups based on cuisine and location.

### Chatbot & API Management  
- **Amazon Lex (Bot)**: Defines conversation structure using intents and slots.
- **LF0 (Lambda Function)**: Handles communication between **Lex** and **API Gateway**.
- **LF1 (Lambda Function)**: Manages **Lex** conversation flow, validates user inputs, and sends requests to **SQS**.
- **API Gateway**: Facilitates communication between the chatbot frontend and backend services.
- **S3**: Hosts and serves the chatbot's static web interface.

### Message Queue & Automation
- **SQS (Simple Queue Service)**: Holds pending user requests for decoupled processing.
- **EventBridge (CloudWatch Events)**: Periodically triggers **LF2** to process messages from **SQS**.

### **Recommendation Processing & Delivery**  
- **LF2 (Lambda Function)**:  
    - Fetches messages from **SQS**.
    - Queries **OpenSearch** for restaurants based on user preferences.
    - Retrieves full restaurant details from **DynamoDB**.
    - Sends personalized recommendations via **SES**.
- **SES (Simple Email Service)**: Handles email delivery of restaurant recommendations.