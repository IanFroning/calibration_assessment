Calibration Optimization Assessment
=======

## Overview
This assignment is designed to evaluate your software engineering skills, problem-solving approach, and ability to work with scientific programming concepts. The task involves interacting with a REST API server to determine the optimal input for a measurement endpoint. Your solution will serve as the core of our technical interview.

We are interested in the solution you produce, but we are more interested in how you approach the problem, how you decompose tasks, how you validate your solution, and how you think about the maintainability of the code you produce.

### File structure:
- `server.py` - this contains a FastAPI server that simulates a device requiring calibration. You will interact with this server to complete the task.
- requirements.txt - this contains the dependencies needed to run `server.py`.

### Server Endpoints

The provided server implements a small REST API with the following endpoints:

- **Root endpoint**: `/`
  - Returns a JSON object: `{"status": "up"}`. This can be used to validate that the server is running.

- **Measurement endpoint**: `/measure?angle`
  - Accepts a query parameter `angle` with numeric values between `0.0` and `360.0`.
  - Returns a measured "response" as a numeric value between `0.0` and `100.0`. This value represents a simulated voltage from a photodetector. The server adds noise to the output, but the underlying behavior is static.

The server is implemented in `server.py`. You should review the file to understand its behavior and ensure there is no malicious code. The code is intentionally not well-documented to simulate working with third-party code that you do not control.

### Goal
Your task is to create a Python module that determines the angle (input to the `/measure` endpoint) that results in the maximum output from the device (output from `/measure`). This process should:

1. **Reliably** find the optimal value in as few measurements as possible.
2. Fit the data to a Gaussian curve and use that information to determine the optimal angle.

Your code should not assume that the server will return the same distribution of data but that it will return data with the same underlying signal. Your solution should make HTTP requests to the server to gather the necessary data.

In review, we will run your code against versions of the server with different configuration and evaluate how well it performs.

While this is a toy example, we will use this to assess your ability to write modular, robust, maintainable, production code. Please ensure your code is representative of how you would handle this problem while working at Infleqtion.

### Requirements
Your implementation should produce the following outputs:

1. Print to stdout:
   - The angle that produces the optimal response.
   - The measured voltage for that angle.
   - The expected value for that angle as determined by the fitted Gaussian curve.
   - The total number of measurements taken.

2. Produce a scatter plot of the measured points:
   - The x-axis should represent the angles.
   - The y-axis should represent the measured voltages.
   - The scatter plot should include the fitted Gaussian curve.

### Constraints
- Your code should not require any additional third-party packages beyond those already listed in `requirements.txt`. If you choose to add additional packages, please explain why they are necessary.
- Your solution should be well-structured, maintainable, and easy to understand. Be sure to include appropriate unit tests.

### Getting Started
1. Start the server by running `server.py`. You can use the following command:
   ```bash
   python server.py
   ```
   By default, the server will run on localhost:8000.

2. Verify that the server is running by testing the root endpoint (/). You can do this using a browser or curl:

    - Using a browser: 
        - Open your browser and navigate to `http://localhost:8000/`. You should see a JSON response: `{"status": "up"}`.
    - Using curl: 
        - Run the following command in your terminal:
        ```bash
        curl http://localhost:8000/
        ```
        - This should return the same JSON response: {"status": "up"}.
3. Once you have confirmed the server is running, proceed to create your Python module to interact with the /measure endpoint and complete the task.
