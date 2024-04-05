from pdf2image import convert_from_path

def pdf_to_png(pdf_path, output_folder=None, prefix=None):
    """
    Convert a PDF file to PNG images.

    Args:
        pdf_path (str): Path to the PDF file.
        output_folder (str): Folder to save the PNG images. If None, images will be saved in the current directory.
        prefix (str): Prefix for the output PNG files.

    Returns:
        list: List of paths to the saved PNG images.
    """
    images = convert_from_path(pdf_path)

    if output_folder is None:
        output_folder = "."

    if prefix is None:
        prefix = ""

    png_paths = []
    for i, image in enumerate(images):
        png_path = f"{output_folder}/{prefix}page_{i+1}.png"
        image.save(png_path, "PNG")
        png_paths.append(png_path)

    return png_paths

# Example usage:
pdf_path = "example.pdf"
output_folder = "output_images"
prefix = "converted_"
png_paths = pdf_to_png(pdf_path, output_folder, prefix)
print("PNG images saved at:")
for png_path in png_paths:
    print(png_path)
