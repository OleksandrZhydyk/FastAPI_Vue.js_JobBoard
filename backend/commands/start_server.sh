#!/bin/bash

cd src && uvicorn main:app --host 0.0.0.0 --port ${WSGI_PORT} --root-path /api/v1 --reload
