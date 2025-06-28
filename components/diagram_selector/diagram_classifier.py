"""
Simple Diagram Classifier
Developer: Hatem Soliman
Purpose: Analyze meeting transcripts and determine diagram types
"""

import json
import requests

# Simple in-memory counter that resets with the Python process (i.e. the
# browser session described by the user).  The first call returns
# ``meeting_001``, the second ``meeting_002`` and so on.
_MEETING_COUNTER: int = 0


def _next_meeting_id() -> str:
  """Generate the next incremental meeting ID for the current session."""
  global _MEETING_COUNTER
  _MEETING_COUNTER += 1
  return f"meeting_{_MEETING_COUNTER:03d}"

def analyze_meeting(transcript, api_key, project_id, endpoint_url):
  """
  Simple function to analyze meeting transcript and suggest diagram type.
  
  Args:
    transcript: Text from meeting
    
  Returns:
    Dictionary with diagram type and reasoning
  """
  # ------------------------------------------------------------------
  # 1) Obtain an IBM access token (fixed header for form data)
  # ------------------------------------------------------------------
  token_resp = requests.post(
    "https://iam.cloud.ibm.com/identity/token",
    data={
      "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
      "apikey": api_key,
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"},
  )
  token_resp.raise_for_status()
  access_token = token_resp.json().get("access_token")

  # ------------------------------------------------------------------
  # 2) Craft the prompt so Granite 3.3-8b-instruct returns the fields we
  #    need *except* the meeting ID and transcript (added in code below).
  # ------------------------------------------------------------------
  prompt = f"""You are an expert at what diagrams are most suitable for a given meeting transcript.

1. Read the following meeting transcript.
2. Decide which diagram is most suitable *from this list of UML diagrams* and write it in the field "output_diagram" (use the exact name):
  • Sequence Diagram
  • Usecase Diagram
  • Class Diagram
  • Object Diagram
  • Component Diagram
  • Deployment Diagram
  • State Diagram
  • Timing Diagram
  • Flowchart Diagram
  • Activity Diagram
  • ER Diagram

3. Propose a concise, descriptive title in the field "title".
4. Extract 3-6 relevant keywords in the field "keywords".

Transcript (verbatim, do not rewrite):
{transcript.strip()}

Return **only** a JSON object with this exact structure and no extra keys:
{{
  "title": "<generated_title>",
  "output_diagram": "<one_of_the_supported_diagrams>",
  "keywords": ["keyword1", "keyword2", "keyword3"]
}}

Do not include an "id" or the full transcript – those will be added by the calling code."""

  # ------------------------------------------------------------------
  # 3) Call the Granite model endpoint. Only minimal request code is
  #    included; adjust 'endpoint_url' and result parsing as needed.
  # ------------------------------------------------------------------
  completion_resp = requests.post(
    endpoint_url,
    json={
      "model_id": "ibm-granite/granite-3.3-8b-instruct",
      "input": [
        {"role": "user", "content": prompt}
      ],
      "parameters": {
        "max_tokens": 512,
        "temperature": 0.2,
        "top_p": 0.9,
      },
    },
    headers={
      "Authorization": f"Bearer {access_token}",
      "Content-Type": "application/json",
      "X-IBM-Project-Id": project_id,
    },
  )
  completion_resp.raise_for_status()

  # The Granite endpoint returns a list of results; adjust if your schema
  # differs. We expect the generated text to be the JSON we asked for.
  generated_text = completion_resp.json()["results"][0]["generated_text"]
  ai_data = json.loads(generated_text)

  # ------------------------------------------------------------------
  # 4) Assemble the final meeting object that matches SAMPLE_MEETINGS.
  # ------------------------------------------------------------------
  meeting_obj = {
    "id": _next_meeting_id(),
    "title": ai_data.get("title", "Untitled Meeting"),
    "transcript": transcript.strip(),
    "output_diagram": ai_data.get("output_diagram", "Flowchart"),
    "keywords": ai_data.get("keywords", []),
  }

  return meeting_obj