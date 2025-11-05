# Animated WebP Webapp

Small Flask web app to compress animated WebP files and download the compressed result.

## Features
- Upload .webp files (single or multiple)
- Compress (quality / resize options)
- Download compressed files

## Quick start (local)
1. Install system libs (Ubuntu/Debian/Kali):
   ```bash
   sudo apt update
   sudo apt install -y python3-venv python3-dev libwebp-dev libjpeg-dev zlib1g-dev libpng-dev
