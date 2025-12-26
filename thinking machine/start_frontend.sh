#!/bin/bash

# Start the frontend
cd "$(dirname "$0")/frontend"
streamlit run app.py --server.port 8501

