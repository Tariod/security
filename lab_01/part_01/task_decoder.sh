#!/usr/bin/env bash

cat encoded.txt | base64 -d | base64 -d
