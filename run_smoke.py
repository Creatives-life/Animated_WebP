# run_smoke.py
import sys
from PIL import features

def main():
    ok = features.check("webp")
    print("Pillow WebP support:", ok)
    if not ok:
        print("ERROR: Pillow does not have WebP support.")
        sys.exit(2)
    # Try importing app and Animated_WebP
    try:
        import app
        import Animated_WebP
    except Exception as e:
        print("Import failed:", e)
        sys.exit(3)
    print("Imports OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
