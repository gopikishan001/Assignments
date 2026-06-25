import json
import time
from pathlib import Path

from openai import OpenAI


class ResumeParserLLM:

    def __init__(self, config: dict):

        provider_name = config["provider"]
        provider = config["providers"][provider_name]

        self.model = provider["model"]
        self.client = OpenAI(api_key=provider["api_key"],base_url=provider["base_url"], timeout=config["processing"]["timeout_seconds"])

        self.max_tokens = config["processing"]["max_tokens"]
        self.temperature = config["processing"]["temperature"]

        self.retry_limit = config["processing"]["retry_limit"]
        self.retry_delay = config["processing"]["retry_delay"]

        self.system_prompt = self._load_file(config["prompts"]["system_prompt_file"])
        self.user_prompt_template = self._load_file(config["prompts"]["user_prompt_file"])

    @staticmethod
    def _load_file(filepath: str) -> str:

        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {filepath}")

        return path.read_text(encoding="utf-8")

    @staticmethod
    def _clean_response(raw_response):
        raw_response = raw_response.strip()
        if raw_response.startswith("```json"): raw_response = raw_response[7:]
        if raw_response.startswith("```"): raw_response = raw_response[3:]
        if raw_response.endswith("```"): raw_response = raw_response[:-3]

        return raw_response.strip()

    @staticmethod
    def _validate_json(parsed_json: dict):

        if not isinstance(parsed_json, dict):
            raise ValueError("LLM response is not a JSON object")

        return True

    def parse_resume(self, resume_text):
        
        prompt = self.user_prompt_template + resume_text
        last_error = None

        for attempt in range(1, self.retry_limit + 1):
            
            try:
                response = self.client.chat.completions.create(
                        model=self.model,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        messages=[
                            {
                                "role": "system",
                                "content": self.system_prompt
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )
                
                raw_response = response.choices[0].message.content
                cleaned_response = self._clean_response(raw_response)

                parsed_json = json.loads(cleaned_response)
                self._validate_json(parsed_json)

                return parsed_json

            except Exception as error:

                last_error = error
                print(f"[LLM Retry {attempt}/{self.retry_limit}] {str(error)}")

                if attempt < self.retry_limit:
                    wait_time = self.retry_delay * (2 ** (attempt - 1))
                    time.sleep(wait_time)

        raise RuntimeError(f"Failed after {self.retry_limit} attempts. Last error: {last_error}")