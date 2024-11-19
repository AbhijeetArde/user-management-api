# User Management API with DynamoDB

This is a simple RESTful API to manage user data. The API is built using **Python (Flask)** and uses **AWS DynamoDB** as a NoSQL database. The API exposes endpoints for creating, retrieving, updating, and deleting users.

## Features

- **Create a user**: Add new users with details such as name, email, phone number, etc.
- **Retrieve a user**: Get details of a user by their unique ID.
- **Update a user**: Modify a user's details.
- **Delete a user**: Remove a user by their ID.
- **Input validation**: Ensures that email, phone number, and other inputs are valid.

## Table of Contents

1. [Installation](#installation)
2. [Setup](#setup)
3. [Running the Application Locally](#running-the-application-locally)
4. [Endpoints](#endpoints)
5. [Testing the API](#testing-the-api)
6. [AWS Deployment](#aws-deployment)
7. [License](#license)

---

## Installation

Follow these steps to get the project up and running on your local machine.

### Prerequisites

- Python 3.8 or later
- AWS account (for DynamoDB and deployment)
- AWS CLI configured with appropriate credentials (for DynamoDB access)

### Step 1: Clone the repository

Clone the repository to your local machine:

```bash
git clone <your-repository-url>
cd user-management-api
```

### Step 2: Create a Virtual Environment

It's recommended to create a virtual environment to manage your dependencies:

```bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

### Step 3: Install dependencies

Install all the required dependencies by running:

```bash
pip install -r requirements.txt
```

---

## Setup

### DynamoDB Setup

1. **Create a DynamoDB table** in your AWS account:
   - **Table name**: `UsersTable`
   - **Partition key**: `user_id` (Type: String)
   
2. Ensure your AWS credentials are configured properly. You can use **AWS CLI** or set environment variables to authenticate with DynamoDB. If you're using AWS CLI, you can configure your credentials using:

   ```bash
   aws configure
   ```

---

## Running the Application Locally

To run the application on your local machine, execute the following command:

```bash
python app.py
```

This will start the Flask development server on `http://127.0.0.1:5000`.

---

## Endpoints

### 1. **POST /users**

Create a new user.

**Request Body** (JSON):
```json
{
  "lastname": "Doe",
  "dob": "1990-01-01",
  "address": "123 Main St, City, Country",
  "gender": "Male",
  "email": "john.doe@example.com",
  "phone_number": "1234567890"
}
```

**Response** (JSON):
```json
{
  "message": "User created",
  "user_id": "uuid-of-new-user"
}
```

### 2. **GET /users/{user_id}**

Retrieve a user by their ID.

**URL**: `/users/{user_id}`

**Response** (JSON):
```json
{
  "user_id": "uuid-of-user",
  "lastname": "Doe",
  "dob": "1990-01-01",
  "address": "123 Main St, City, Country",
  "gender": "Male",
  "email": "john.doe@example.com",
  "phone_number": "1234567890"
}
```

### 3. **PUT /users/{user_id}**

Update a user's details.

**Request Body** (JSON):
```json
{
  "address": "456 Another St, New City"
}
```

**Response** (JSON):
```json
{
  "message": "User updated"
}
```

### 4. **DELETE /users/{user_id}**

Delete a user by their ID.

**Response** (JSON):
```json
{
  "message": "User deleted"
}
```

---

## Testing the API

You can test the API using **Postman** or **curl**.

### Example 1: Create a User (POST /users)

```bash
curl -X POST http://127.0.0.1:5000/users -H "Content-Type: application/json" -d '{
    "lastname": "Doe",
    "dob": "1990-01-01",
    "address": "123 Main St, City, Country",
    "gender": "Male",
    "email": "john.doe@example.com",
    "phone_number": "1234567890"
}'
```

### Example 2: Get a User by ID (GET /users/{user_id})

```bash
curl http://127.0.0.1:5000/users/{user_id}
```

### Example 3: Update a User (PUT /users/{user_id})

```bash
curl -X PUT http://127.0.0.1:5000/users/{user_id} -H "Content-Type: application/json" -d '{
    "address": "456 Another St, New City"
}'
```

### Example 4: Delete a User (DELETE /users/{user_id})

```bash
curl -X DELETE http://127.0.0.1:5000/users/{user_id}
```

---

## AWS Deployment

### 1. **Create a deployment package**

If you wish to deploy the application to **AWS Lambda** with **API Gateway**, you'll need to create a deployment package:

```bash
mkdir package
pip install -r requirements.txt -t package/
cd package
zip -r ../deployment.zip .
cd ..
zip -g deployment.zip app.py
```

### 2. **Create a Lambda function**

- Go to the **AWS Lambda** console and create a new Lambda function.
- Choose **Python 3.8** as the runtime.
- Upload the `deployment.zip` file.
- Set the handler to `app.lambda_handler` (you'll need to adjust the code for Lambda if needed).

### 3. **Set up API Gateway**

- Create a new **REST API** in **API Gateway**.
- Set up the integration with your Lambda function for the routes: `/users`, `/users/{user_id}` for `POST`, `GET`, `PUT`, and `DELETE` operations.

For detailed deployment instructions, you can refer to the [AWS Lambda Flask](https://flask.palletsprojects.com/en/2.3.x/deploying/aws/) documentation.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
