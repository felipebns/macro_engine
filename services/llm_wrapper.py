from urllib import response

from services.config import OPENAI_KEY
from services.prompts import (
    analyse_risk_prompt,
    generate_output_json_prompt,
    generate_output_json_self_critique_prompt,
    generate_report_prompt,
    parse_input_prompt,
)
from openai import OpenAI
import json

class LLM_Wrapper:
    def __init__(self, model: str = "gpt-5-mini") -> None:
        self.url = OPENAI_KEY
        self.client = OpenAI(api_key=OPENAI_KEY)
        self.model = model

    def _call_llm(self, system_prompt: str, user_input: str) -> str:
        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
            )
        except Exception as exc:
            raise RuntimeError("Error during LLM processing.") from exc
        
        return response.output_text

    def parse_input(self, user_scenery: str) -> dict:
        print("Starting to parse user input and fetch macro metrics...")
        response = self._call_llm(parse_input_prompt, user_scenery)
        return json.loads(response)

    def analyse_risk(self, context: dict) -> dict:
        print("Analysing risks based on the provided context...")
        response = self._call_llm(analyse_risk_prompt, json.dumps(context))
        return json.loads(response)

    def generate_json(self, risks: dict, context: dict) -> dict:
        print("Generating final JSON output...")
        payload = {
            "context": context,
            "risks": risks,
        }
        response = self._call_llm(generate_output_json_prompt, json.dumps(payload))
        draft_json = json.loads(response)

        critique_payload = {
            "context": context,
            "risks": risks,
            "draft_json": draft_json,
        }
        critique_response = self._call_llm(
            generate_output_json_self_critique_prompt,
            json.dumps(critique_payload),
        )
        try:
            return json.loads(critique_response)
        except json.JSONDecodeError:
            return draft_json
    
    def generate_report(self, final_json: dict) -> str:
        print("Generating markdown report...")
        response = self._call_llm(generate_report_prompt, json.dumps(final_json))
        return response



