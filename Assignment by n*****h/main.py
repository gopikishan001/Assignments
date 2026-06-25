import json
from pathlib import Path

import yaml
import os

from modules.sanity_check import validate_resume_file
from modules.text_extractor import extract_text
from modules.llm_call import ResumeParserLLM


def load_config(config_path = "config.yaml"):

    config_file = Path(config_path)
    with open(config_file, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def get_resume_files(resume_folder, allowed_extensions):

    resume_path = Path(resume_folder)
    files = []

    for file in os.listdir(resume_path):
        file = Path(resume_folder, file)
        if file.is_file() and file.suffix.lower() in allowed_extensions :
            files.append(file)

    return sorted(files)


def save_json(data, output_path):

    output_file = Path(output_path)
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file)


def main():

    print("Resume Parser \n\n")
    
    config = load_config()

    allowed_extensions = [ext.lower() for ext in config["supported_extensions"]]
    resume_folder = config["paths"]["resume_folder"]
    max_size_mb = config["processing"]["max_file_size_mb"]
    output_file = config["paths"]["output_file"]
    failed_output_file = config["paths"]["failed_output_file"]
    max_extracted_chars = config["processing"]["max_extracted_chars"]

    llm_parser = ResumeParserLLM(config=config)

    resume_files = get_resume_files(resume_folder, allowed_extensions)

    print(f"Found {len(resume_files)} resume(s)")

    results = []
    failed_results = []

    for index, resume_file in enumerate(resume_files, start=1):

        print(f"\n{index} {resume_file.name}")

        if True :
        # try:

            validate_resume_file(str(resume_file), allowed_extensions, max_size_mb)
            text = extract_text(str(resume_file))

            print(f"Extracted {len(text):,} characters")
            if len(text) > max_extracted_chars:
                raise ValueError( f"Extracted text exceeds limit ({len(text):,} > {max_extracted_chars:,})")

            parsed_json = (llm_parser.parse_resume(text))

            results.append(
                {
                    "_file": resume_file.name,
                    "_path": str(resume_file),
                    "_status": "success",
                    "data": parsed_json
                }
            )

            print("Success")

        # except Exception as error:
        #     print(f"Failed: {str(error)}")

        #     failed_results.append(
        #         {
        #             "_file": resume_file.name,
        #             "_path": str(resume_file),
        #             "_status": "failed",
        #             "_error": str(error)
        #         }
        #     )

    save_json(results, output_file)
    save_json(failed_results, failed_output_file)

    print("\n\n")
    print(f"Successful : {len(results)}")
    print(f"Failed     : {len(failed_results)}")
    print(f"Output     : {output_file}")
    print(f"Failures   : {failed_output_file}")

if __name__ == "__main__":
    main()