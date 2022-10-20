#!/bin/bash

docker build -t shape_encdec_app . \
&& docker run -d --name encode_decode -p 8000:8000 shape_encdec_app
