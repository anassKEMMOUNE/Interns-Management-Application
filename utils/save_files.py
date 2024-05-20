import os
def save_files(files):
    # Define the directory to save the files
    upload_directory = os.path.abspath("Resumes") 
    print("upload_directory ",upload_directory)

    # Empty the directory
    for file_name in os.listdir(upload_directory):
        file_path = os.path.join(upload_directory, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    # Save new files
    for file in files:
        file.save(os.path.join(upload_directory, file.filename))