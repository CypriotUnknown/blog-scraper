# Blog scraper

## Overview

This application publishes the scraped data to a Redis client. It also stores the scraped data in JSON format. If you want to publish to redis either place a file named `redis-conf.json` inside the main blog folder; or you can optionally specify the path to this configuration file using the `CONFIG_PATH` environment variable. The output file is located at `articles.json`.

## Configuration

### JSON Configuration File

The application can use a JSON configuration file to specify connection details. The fields `username` and `password` are optional. The JSON file should contain the following fields:

```json
{
  "host": "<string>",
  "port": <int>,
  "username": "<string>",
  "password": "<string>"
}