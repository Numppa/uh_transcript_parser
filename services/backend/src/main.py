import io
import os
import subprocess
import tempfile

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import Response
from fastapi.responses import StreamingResponse

from .document import Document


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://localhost:80"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/parse")
def parse(file: UploadFile = File(...)):
    try:
        contents = file.file.read()

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as input_pdf:
            input_pdf.write(contents)
            input_pdf.close()

            subprocess.run(f"pdftotext -layout {input_pdf.name}", shell=True)

            input_txt = input_pdf.name.replace(".pdf", ".txt")
            os.remove(input_pdf.name)

            with open(input_txt, "r") as f:
                content = f.readlines()
                f.close()

            os.remove(input_txt)

            doc = Document(content)
            doc.parse()

        filename, csv_string = doc.get_csv()

        if doc.credits != doc.total_credits_check:
            filename = "X_" + filename

        stream = io.StringIO()
        stream.write(csv_string)
        response = StreamingResponse(content=iter(stream.getvalue()), media_type="text/csv")
        response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
        response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
        return response

    except Exception as e:
        print(e)
        return Response(status_code=500)
