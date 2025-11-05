from PIL import Image
import os
import glob

def compress_animated_webp(input_path, output_path, quality=80, resize_ratio=1.0, duration=None):
    """
    Compress an animated WebP file by adjusting quality, resizing, or frame duration.
    
    Args:
        input_path (str): Path to input animated WebP file.
        output_path (str): Path to save compressed WebP file.
        quality (int): WebP quality (0-100, lower = more compression, default=80).
        resize_ratio (float): Ratio to resize frames (e.g., 0.5 for half size, default=1.0).
        duration (int): Frame duration in milliseconds (optional, overrides original).
    """
    try:
        # Open the animated WebP file
        img = Image.open(input_path)
        
        # Check if the file is animated
        if not hasattr(img, 'is_animated') or not img.is_animated:
            print(f"Skipping {input_path}: Not an animated WebP.")
            return False
        
        # Get frames
        frames = []
        for frame in range(img.n_frames):
            img.seek(frame)
            frame_img = img.copy()
            
            # Resize frame if resize_ratio != 1.0
            if resize_ratio != 1.0:
                new_size = (int(frame_img.width * resize_ratio), int(frame_img.height * resize_ratio))
                frame_img = frame_img.resize(new_size, Image.Resampling.LANCZOS)
            
            frames.append(frame_img)
        
        # Get original duration or use provided duration
        frame_duration = duration if duration is not None else img.info.get('duration', 100)
        
        # Save compressed animated WebP
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            format='WEBP',
            quality=quality,
            method=6,
            loop=0,
            duration=frame_duration,
            minimize_size=True
        )
        
        # Print file sizes
        original_size = os.path.getsize(input_path) / 1024  # KB
        compressed_size = os.path.getsize(output_path) / 1024  # KB
        print(f"Processed {os.path.basename(input_path)}:")
        print(f"  Original size: {original_size:.2f} KB")
        print(f"  Compressed size: {compressed_size:.2f} KB")
        print(f"  Compression ratio: {(original_size - compressed_size) / original_size * 100:.2f}%")
        return True
        
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def process_multiple_webp(input_dir, output_dir, quality=80, resize_ratio=1.0, duration=None):
    """
    Compress all animated WebP files in input_dir and save to output_dir with base names.
    
    Args:
        input_dir (str): Directory containing input WebP files.
        output_dir (str): Directory to save compressed WebP files.
        quality (int): WebP quality (0-100).
        resize_ratio (float): Ratio to resize frames.
        duration (int): Frame duration in milliseconds (optional).
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Find all WebP files in input directory
    webp_files = glob.glob(os.path.join(input_dir, "*.webp"))
    
    if not webp_files:
        print(f"No WebP files found in {input_dir}")
        return
    
    print(f"Found {len(webp_files)} WebP files to process.")
    
    # Process each WebP file
    for input_path in webp_files:
        # Get base name (filename without extension)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        # Define output path with same base name
        output_path = os.path.join(output_dir, f"{base_name}.webp")
        
        # Compress the file
        compress_animated_webp(input_path, output_path, quality, resize_ratio, duration)

if __name__ == "__main__":
    # example usage (or remove it)
    input_directory = "input_dir"
    output_directory = "output_dir"
    process_multiple_webp(input_directory, output_directory, quality=10, resize_ratio=0.9, duration=20)

