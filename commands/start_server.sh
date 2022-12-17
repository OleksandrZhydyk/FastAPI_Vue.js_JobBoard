#!/bin/bash

uvicorn main:app --host 0.0.0.0 --port ${WSGI_PORT} --reload
