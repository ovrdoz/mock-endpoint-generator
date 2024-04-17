# Mock-Endpoint-Generator

## Overview
Mock-Endpoint-Generator is a Flask-based application that dynamically creates mock API endpoints from Mok files stored in a specified directory. It's designed to facilitate rapid backend development and testing by allowing developers to easily simulate API responses.

## Getting Started

### Prerequisites
- Python 3.6 or higher
- Flask

You can install Flask using pip if you don't have it already:
```bash
pip install flask watchdog
```

### Installation
Clone this repository to your local machine:
```bash
git clone https://github.com/ovrdoz/mock-endpoint-generator.git
cd mock-endpoint-generator
```

### Usage
1. **Prepare Mok Files:**
   Place your Mok files in the data directory. To define the API endpoint for each file, start the file with a comment line that specifies the route. This route comment dictates the endpoint path that the API will serve. For example, if the first line of your Mok file is # /api/get-user, the content of the file will be available at http://localhost:5000/api/get-user. This method allows you to dynamically create and update endpoints simply by adding or modifying Mok files in the data directory. Here's how you format the file:
   ```bash
   # /api/get-user
   {
       "id": "uuid-1234",
       "email": "user@example.com",
       "roles": ["admin", "user"]
   }
   ```

2. **Configure the Server:**
   You can configure the port by setting the `PORT` environment variable. If no port is set, the default Flask port (5000) will be used.
   ```bash
   export PORT=8000  # Set your desired port
   ```

3. **Run the Server:**
   Start the server by running:
   ```bash
   python app.py
   ```
   This will serve the APIs on the configured port, creating endpoints based on the Mok files in the `data` directory.

4. **Updating Endpoints:**
   Simply modify the Mok files in the `data` directory or add new files. Restart the server to see the changes reflected in the API endpoints.

## Features
- Dynamic endpoint creation from Mok files.
- Easy configuration of the server port.
- Immediate updates by modifying Mok files and restarting the server.