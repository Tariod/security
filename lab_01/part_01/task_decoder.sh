#!/usr/bin/env bash

cat task_encoded.txt | base64 -d | base64 -d
