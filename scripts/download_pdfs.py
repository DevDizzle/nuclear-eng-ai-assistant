import urllib.request

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

docs = {
    "Turkey_Point_LAR_280_Fire_Protection.pdf": "https://www.nrc.gov/docs/ML2503/ML25035A194.pdf",
    "Turkey_Point_LAR_ITS_Conversion.pdf": "https://www.nrc.gov/docs/ML2309/ML23094A184.pdf",
    "Turkey_Point_LAR_274_Digital_Suspension.pdf": "https://www.nrc.gov/docs/ML2317/ML23179A161.pdf",
    "Turkey_Point_EPU_Attachment_1.pdf": "https://www.nrc.gov/docs/ML1035/ML103560167.pdf"
}

for name, url in docs.items():
    print(f"Downloading {name}...")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response, open(f"data/sample_documents/{name}", 'wb') as out_file:
            data = response.read()
            out_file.write(data)
            print(f"Saved {len(data)} bytes")
    except Exception as e:
        print(f"Failed: {e}")
