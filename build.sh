#!/bin/bash
# Railway build script
echo "Building El Akeil Application..."

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "Build completed successfully!"
