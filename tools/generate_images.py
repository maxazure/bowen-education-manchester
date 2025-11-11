#!/usr/bin/env python3
"""
Batch Image Generation Script
Uses Zhipu AI CogView-3-Flash API to generate images from JSON configuration

Usage:
    python generate_images.py [--config path/to/config.json]
    
    If --config is not provided, defaults to 'images.json' in current directory.

JSON Configuration File Structure:
----------------------------------
The configuration file should have the following structure:

{
  "output_dir": "templates/static/images",
  "images": [
    {
      "filename": "example-image.jpg",
      "prompt": "Detailed description of the image to generate...",
      "priority": "high|medium|low"
    },
    ...
  ]
}

Fields:
- output_dir (string, required): Directory path where generated images will be saved
- images (array, required): Array of image objects to generate

Image object fields:
- filename (string, required): The output filename for the generated image (e.g., "banner.jpg")
- prompt (string, required): Detailed text description for image generation
- priority (string, required): Generation priority - "high", "medium", or "low"

Example JSON structure:
{
  "output_dir": "templates/static/images",
  "images": [
    {
      "filename": "hero-banner.jpg",
      "prompt": "Beautiful beachfront cafe with ocean view, sunny day, modern interior",
      "priority": "high"
    },
    {
      "filename": "coffee-cup.jpg",
      "prompt": "Close-up of latte art in white ceramic cup",
      "priority": "medium"
    }
  ]
}
"""

import requests
import json
import time
import os
import argparse
from pathlib import Path

# Configuration
API_KEY = os.getenv("ZHIPU_KEY", "")
if not API_KEY:
    print("[ERROR] ZHIPU_KEY environment variable is not set!")
    print("Please set it using: export ZHIPU_KEY='your-api-key' (Linux/Mac)")
    print("or: $env:ZHIPU_KEY='your-api-key' (PowerShell)")
    exit(1)

# Configuration
API_KEY = os.getenv("ZHIPU_KEY", "")
if not API_KEY:
    print("[ERROR] ZHIPU_KEY environment variable is not set!")
    print("Please set it using: export ZHIPU_KEY='your-api-key' (Linux/Mac)")
    print("or: $env:ZHIPU_KEY='your-api-key' (PowerShell)")
    exit(1)

API_ENDPOINT = "https://open.bigmodel.cn/api/paas/v4/images/generations"
MODEL = "cogview-4"


def load_images_config(config_file):
    """
    Load image definitions from JSON configuration file
    
    Args:
        config_file (str): Path to the JSON configuration file
        
    Returns:
        tuple: (output_dir: Path, images: list of tuples (filename, prompt, priority))
        
    Raises:
        FileNotFoundError: If configuration file doesn't exist
        json.JSONDecodeError: If JSON is invalid
        KeyError: If required fields are missing
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Validate output_dir field
        if 'output_dir' not in config:
            raise KeyError("JSON file must contain an 'output_dir' field")
        
        output_dir = Path(config['output_dir'])
        
        # Validate images array
        if 'images' not in config:
            raise KeyError("JSON file must contain an 'images' array")
        
        images = []
        for idx, item in enumerate(config['images']):
            # Validate required fields
            if 'filename' not in item:
                raise KeyError(f"Image at index {idx} missing 'filename' field")
            if 'prompt' not in item:
                raise KeyError(f"Image at index {idx} missing 'prompt' field")
            if 'priority' not in item:
                raise KeyError(f"Image at index {idx} missing 'priority' field")
            
            # Validate priority value
            if item['priority'] not in ['high', 'medium', 'low']:
                raise ValueError(f"Image '{item['filename']}' has invalid priority: {item['priority']}")
            
            images.append((item['filename'], item['prompt'], item['priority']))
        
        return output_dir, images
    
    except FileNotFoundError:
        print(f"[ERROR] Configuration file '{config_file}' not found!")
        print(f"Please create {config_file} with the structure described in the script header.")
        raise
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in '{config_file}': {e}")
        raise
    except (KeyError, ValueError) as e:
        print(f"[ERROR] Configuration error: {e}")
        raise





def generate_image(filename, prompt, priority, output_dir):
    """Generate a single image using Zhipu AI API"""
    print(f"\n{'='*80}")
    print(f"Generating: {filename}")
    print(f"Priority: {priority}")
    print(f"Prompt: {prompt[:100]}...")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "size": "1920x1088"
    }

    try:
        # Call API
        print("Calling API...")
        response = requests.post(API_ENDPOINT, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()

        # Extract image URL
        if "data" in result and len(result["data"]) > 0:
            image_url = result["data"][0]["url"]
            print(f"Image URL received: {image_url[:80]}...")

            # Download image
            print("Downloading image...")
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()

            # Save image
            output_path = output_dir / filename
            with open(output_path, "wb") as f:
                f.write(img_response.content)

            file_size = os.path.getsize(output_path) / 1024  # KB
            print(f"[SUCCESS] Saved to {filename} ({file_size:.1f} KB)")
            return True
        else:
            print(f"[ERROR] No image URL in response")
            print(f"Response: {result}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False


def main():
    """Main batch generation function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Batch image generation using Zhipu AI CogView-3-Flash API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python generate_images.py
  python generate_images.py --config my_images.json
  python generate_images.py --config /path/to/config.json
        '''
    )
    parser.add_argument(
        '--config',
        type=str,
        default='images.json',
        help='Path to JSON configuration file (default: images.json)'
    )
    
    args = parser.parse_args()
    config_file = args.config
    
    print("="*80)
    print("Batch Image Generation - Zhipu AI CogView")
    print("="*80)
    print(f"Model: {MODEL}")
    print(f"Configuration file: {config_file}")
    
    # Load image definitions from JSON file
    try:
        output_dir, images = load_images_config(config_file)
    except Exception as e:
        print(f"\n[FATAL] Failed to load configuration: {e}")
        return
    
    print(f"Total images to generate: {len(images)}")
    print(f"Output directory: {output_dir}")
    print("="*80)

    # Create output directory if not exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Sort by priority (high -> medium -> low)
    priority_order = {"high": 0, "medium": 1, "low": 2}
    sorted_images = sorted(images, key=lambda x: priority_order.get(x[2], 1))

    # Track progress
    total = len(sorted_images)
    success_count = 0
    failed_images = []

    # Generate each image
    for idx, (filename, prompt, priority) in enumerate(sorted_images, start=1):
        print(f"\n[{idx}/{total}] Processing: {filename}")

        # Skip if already exists
        if (output_dir / filename).exists():
            print(f"[SKIP]  Skipped - file already exists")
            success_count += 1
            continue

        # Generate image
        if generate_image(filename, prompt, priority, output_dir):
            success_count += 1
        else:
            failed_images.append(filename)

        # Rate limiting - wait 2 seconds between requests
        if idx < total:
            print("Waiting 2 seconds before next request...")
            time.sleep(2)

    # Summary
    print("\n" + "="*80)
    print("GENERATION COMPLETE!")
    print("="*80)
    print(f"Total images: {total}")
    print(f"Successfully generated: {success_count}")
    print(f"Failed: {len(failed_images)}")

    if failed_images:
        print(f"\nFailed images:")
        for filename in failed_images:
            print(f"  - {filename}")
    else:
        print("\n[OK] All images generated successfully!")

    print("="*80)


if __name__ == "__main__":
    main()
