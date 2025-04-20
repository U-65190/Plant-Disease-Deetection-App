from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import PlainTextResponse
import shutil
import subprocess

app = FastAPI()

@app.post("/upload", response_class=PlainTextResponse)
async def upload_file(
    crop: str = Form(...),
    image: UploadFile = File(...)
):
    # Save the uploaded file
    with open("input.jpg", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Choose script based on crop
    script_map = {
        "apple": "apple_script.py",
        "cherry": "cherry_script.py",
        "corn": "corn_script.py",
        "grape": "grape_script.py"
    }

    script_name = script_map.get(crop)
    if not script_name:
        return "Invalid crop selection."

    # Run the corresponding script
    try:
        if(script_name== "apple_script.py"): 
            result = subprocess.check_output(["python", r'prediction scripts\testing_apple.py'], stderr=subprocess.STDOUT, text=True)
        elif(script_name== "cherry_script.py"): 
            result = subprocess.check_output(["python", r'prediction scripts\testing_cherry.py'], stderr=subprocess.STDOUT, text=True)
        elif(script_name== "corn_script.py"): 
            result = subprocess.check_output(["python", r'prediction scripts\testing_corn.py'], stderr=subprocess.STDOUT, text=True)
        elif(script_name== "grape_script.py"): 
            result = subprocess.check_output(["python", r'prediction scripts\testing_grape.py'], stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Script error:\n{e.output}"
