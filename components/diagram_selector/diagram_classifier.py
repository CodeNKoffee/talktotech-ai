"""
Simple Diagram Classifier
Developer: Hatem Soliman
Purpose: Analyze meeting transcripts and determine diagram types
"""

import json
import replicate

# Per user instruction, use the Replicate client with a hardcoded token.
# Dabour's token
replicate_client = replicate.Client(api_token="r8_UFdwKaSNK8dV7EN1lqccgQCtjJNxhYt2mJ6No")

# Hatem's token
# replicate_client = replicate.Client(api_token="r8_ZuNi8fo4buhXhahu9G0487TZ5ZXE3Tf3csKRW")

# Simple in-memory counter that resets with the Python process (i.e. the
# browser session described by the user).  The first call returns
# ``meeting_001``, the second ``meeting_002`` and so on.
_MEETING_COUNTER: int = 0


def _next_meeting_id() -> str:
  """Generate the next incremental meeting ID for the current session."""
  global _MEETING_COUNTER
  _MEETING_COUNTER += 1
  return f"meeting_{_MEETING_COUNTER:03d}"

def analyze_meeting(transcript: str) -> dict:
  """
  Analyzes a meeting transcript to suggest a diagram type, title, and keywords using Replicate.
  
  Args:
    transcript: Text from the meeting.
    
  Returns:
    A dictionary containing the full meeting object.
  """
  prompt = f"""You are an expert at what diagrams are most suitable for a given meeting transcript.

1. Read the following meeting transcript.
2. Decide which diagram(s) is most suitable *from this list of UML diagrams* and write it in the array field "output_diagrams" (use the exact names). You can choose up to 3 diagrams 
    if you find that more than 1 is suitable with high confidence. Be very careful not to output more than 3 diagrams and at the same time not to output too many diagrams
    which may not be needed. For example if they are mentioned very briefly, they should not be included in the result:
  • Sequence Diagram
  • Usecase Diagram
  • Class Diagram
  • Component Diagram
  • Flowchart Diagram
  • ER Diagram

3. Propose a concise, descriptive title in the field "title".
4. Extract 3-6 relevant keywords in the field "keywords".

Transcript (verbatim, do not rewrite):
{transcript.strip()}

Return **only** a JSON object with this exact structure and no extra keys:
{{
  "title": "<generated_title>",
  "output_diagram": ["diagram1", "diagram2 (if applicable)", "diagram3 (if applicable)"],
  "keywords": ["keyword1", "keyword2", "keyword3"]
}}

Do not include an "id" or the full transcript – those will be added by the calling code."""

  # Call the Granite model via Replicate
  output_iterator = replicate_client.run(
    "ibm-granite/granite-3.3-8b-instruct",
    input={
      "prompt": prompt,
      "temperature": 0.3,
      "max_tokens": 400,
      "top_p": 0.6,   # High top_p to ensure the model is not too conservative meaning it will creates a larger shortlist of potential words. The output can be more creative and diverse because the model has more "good" options to choose from. It's a safe value that prevents the model from getting stuck while still ensuring relevance. While a low top_p (like 0.2): This creates a very small, exclusive shortlist of only the most likely words. The output will be much more predictable, safe, and often repetitive.
    },
  )
  
  generated_text = "".join(output_iterator).strip()

  # Clean potential markdown fences from the model's output
  if generated_text.startswith("```json"):
    generated_text = generated_text[7:-3].strip()
  
  try:
    ai_data = json.loads(generated_text)
  except json.JSONDecodeError:
    print(f"Warning: Model returned non-JSON output: {generated_text}")
    ai_data = {}

  # Assemble the final meeting object
  meeting_obj = {
    "id": _next_meeting_id(),
    "title": ai_data.get("title", "Untitled Meeting"),
    "transcript": transcript.strip(),
    "output_diagram": ai_data.get("output_diagram", []),
    "keywords": ai_data.get("keywords", []),
  }

  return meeting_obj