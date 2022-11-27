#!/bin/bash

uvicorn --app-dir=src main:app --reload --host 0.0.0.0 --port 8000
