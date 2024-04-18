# Mock-Endpoint-Generator

## Overview
Mock-Endpoint-Generator is a Flask-based application designed to dynamically create mock API endpoints from Mok files. This tool facilitates rapid backend development and testing, allowing developers to simulate various API responses with ease.

## Getting Started

### Prerequisites
Ensure you have Python 3.6 or higher installed. You will also need Flask, which can be installed using pip:

```bash
pip install flask watchdog
```

### Installation
To get started, clone the repository and navigate into the directory:

```bash
git clone https://github.com/ovrdoz/mock-endpoint-generator.git
cd mock-endpoint-generator
```

### Usage

1. **Prepare Mok Files:**
   Store your Mok files in the `data` directory. Start each file with a comment specifying the API endpoint route, like so:
   ```bash
   # /api/get-user
   {
       "id": "uuid-1234",
       "email": "user@example.com",
       "roles": ["admin", "user"]
   }
   ```
   If no HTTP method or status code is mentioned, `GET` and `200 OK` are assumed by default.

2. **Configure the Server:**
   Set the server port via the `PORT` environment variable (default is 5001):
   ```bash
   export PORT=8000
   ```

3. **Run the Server:**
   Execute the following command to start the server:
   ```bash
   python app.py
   ```
   This action will serve the APIs on the specified port using the Mok files in the `data` directory.

4. **Updating Endpoints:**
   Modify or add new Mok files in the `data` directory to update endpoints. Changes take effect upon server restart.

## HTTP Methods and Status Codes

- **Default Method and Code:** If unspecified, endpoints default to `GET` with a `200 OK` status.
- **Supported Methods:** `GET`, `POST`, `PUT`, `DELETE`, `PATCH`.
- **Specifying in Mok Files:** Include the method and code in the first line after the route:
  ```bash
  # /api/update-user PUT 201
  {
      "success": true,
      "message": "User updated successfully"
  }
  ```

## Features

- **Dynamic Endpoint Creation:** Automatically generates endpoints from Mok files.
- **Flexible Configuration:** Easy setup of server ports and quick modifications to endpoints.
- **Real-Time Updates:** Changes in Mok files are quickly reflected by restarting the server.
