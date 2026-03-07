from google.cloud import documentai
from google.api_core.client_options import ClientOptions

def get_or_create_processor(project_id, location):
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    parent = client.common_location_path(project_id, location)
    
    # List processors
    processors = client.list_processors(parent=parent)
    for p in processors:
        if p.type_ == "OCR_PROCESSOR":
            return p.name
            
    # Create processor
    processor = documentai.Processor(
        display_name="nuclear-ocr",
        type_="OCR_PROCESSOR"
    )
    request = documentai.CreateProcessorRequest(
        parent=parent,
        processor=processor
    )
    p = client.create_processor(request=request)
    return p.name

if __name__ == "__main__":
    print(get_or_create_processor("profitscout-lx6bb", "us"))
