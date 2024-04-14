#!/bin/bash

# Check if python3-venv is installed on host to create virtual environment, if not, install it
if ! command -v python3-venv &>/dev/null; then
    echo "Installing python3-venv..."
    sudo apt update
    sudo apt install -y python3-venv || {
        echo "Error: Failed to install python3-venv"
        exit 1
    }
fi

# Create and activate virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv || {
        echo "Error: Failed to create virtual environment"
        exit 1
    }
fi

echo "Activating virtual environment..."
. venv/bin/activate || {
    echo "Error: Failed to activate virtual environment"
    exit 1
}

# Function to display an error message and exit
error_exit() {
    echo "Error: $1" >&2
    deactivate
    exit 1
}

# Install Prowler
echo "Installing Prowler..."
if ! pip install prowler; then
    error_exit "Failed to install Prowler"
fi

# Add Prowler directory to PATH in shell profile if not already added
if ! grep -qxF 'export PATH="$PATH:$PWD/venv/bin"' ~/.bashrc; then
    echo 'export PATH="$PATH:$PWD/venv/bin"' >> ~/.bashrc
fi

# Reload shell profile
. ~/.bashrc

# Install awscli if not already installed
if ! command -v aws >/dev/null; then
    echo "Installing awscli..."
    sudo apt install -y awscli || error_exit "Failed to install awscli"
fi

# Install psycopg2-binary for postgres
echo "Installing psycopg2-binary..."
if ! pip install psycopg2-binary; then
    error_exit "Failed to install psycopg2-binary"
fi

# Install python-dotenv
echo "Installing python-dotenv..."
if ! pip install python-dotenv; then
    error_exit "Failed to install python-dotenv"
fi

# Run Prowler with AWS credentials
echo "Running Prowler..."
if ! prowler -v; then
    error_exit "Failed to run Prowler"
fi

echo "Prowler execution completed successfully."