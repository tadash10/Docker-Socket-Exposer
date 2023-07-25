#!/bin/bash

# Step 1: Clone the repository
git clone https://github.com/your-username/docker-socket-exposer.git
cd docker-socket-exposer

# Step 2: Create and activate the virtual environment
python -m venv venv
source venv/bin/activate

# Step 3: Install the required dependencies
pip install -r requirements.txt

# Step 4: Customize docker_socket_exposer.py (optional)
# Replace /path/to/your/application with your application path.

# Step 5: Execute the script
python main.py
