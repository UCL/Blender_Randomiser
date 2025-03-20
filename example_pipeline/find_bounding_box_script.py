import cv2
import numpy as np
import os

def find_connected_components(image_path, output_dir):
    # Read the image
    image = cv2.imread(image_path)
    
    # Check if image is loaded properly
    if image is None:
        print(f"Warning: Unable to read image {image_path}")
        return 0, []
    
    # Get image dimensions
    image_height, image_width = image.shape[:2]
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold the image to create a binary image
    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    
    # Find connected components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
    
    # Initialize a list to store bounding boxes
    bounding_boxes = []
    
    for i in range(1, num_labels):  # Skip the background label 0
        x_min = stats[i, cv2.CC_STAT_LEFT]
        y_min = stats[i, cv2.CC_STAT_TOP]
        width = stats[i, cv2.CC_STAT_WIDTH]
        height = stats[i, cv2.CC_STAT_HEIGHT]
        
        # Convert to center coordinates and dimensions
        x_center = x_min + width / 2
        y_center = y_min + height / 2
        
        # Convert to ratios
        x_center /= image_width
        y_center /= image_height
        width /= image_width
        height /= image_height
        
        bounding_boxes.append((x_center, y_center, width, height))
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create the output file path
    base_name = os.path.basename(image_path)
    output_file = os.path.join(output_dir, os.path.splitext(base_name)[0] + '.txt')
    
    # Write results to a text file
    with open(output_file, 'w') as f:
        for x_center, y_center, width, height in bounding_boxes:
            f.write(f"0 {x_center:.8f} {y_center:.8f} {width:.8f} {height:.8f}\n")
    
    return num_labels - 1, bounding_boxes  # Subtract 1 to exclude the background

def process_all_images(input_dir, output_dir):
    """
    Processes all PNG images in input_dir and saves bounding box annotations in output_dir.
    """
    # Ensure input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} does not exist.")
        return
    
    # Get all PNG images in the directory
    image_files = [f for f in os.listdir(input_dir) if f.endswith('.png')]
    
    # Process each image
    for image_file in image_files:
        image_path = os.path.join(input_dir, image_file)
        num_items, bounding_boxes = find_connected_components(image_path, output_dir)
        
        print(f"Processed {image_file}: {num_items} objects detected.")
    
    print("Processing complete.")

# Example usage
input_directory = '../output_files/seg_images'
output_directory = '../labels'
process_all_images(input_directory, output_directory)
