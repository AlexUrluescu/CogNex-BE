

class Utils():
    def getFilesNameFromADirectory(self):
        if not filename.lower().endswith('.pdf'):
            return "Not a PDF file", 400
    
        # Get the full path of the requested PDF file
        file_path = os.path.join(pdf_directory, filename)
        
        # Check if the file exists
        if not os.path.isfile(file_path):
            return "PDF not found", 404
        
        file = send_from_directory(pdf_directory, filename)
        
        # Serve the PDF file
        return file