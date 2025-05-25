#!/bin/bash
python3 src/main.py /blog/tom/
cd public && python3 -m http.server 8888