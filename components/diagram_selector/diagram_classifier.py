"""
Simple Diagram Classifier
Developer: Hatem Soliman
Purpose: Analyze meeting transcripts and determine diagram types
"""

def analyze_meeting(transcript, api_key, project_id, endpoint_url):
  """
  Simple function to analyze meeting transcript and suggest diagram type.
  
  Args:
    transcript: Text from meeting
    
  Returns:
    Dictionary with diagram type and reasoning
  """
  """
  # Convert to lowercase for easier matching
  text = transcript.lower()
  
  # Simple keyword matching
  if "class" in text or "object" in text or "inheritance" in text:
    return {
      "diagram_type": "UML Class Diagram",
      "reasoning": "Meeting discusses classes and objects"
    }
  
  elif "sequence" in text or "flow" in text or "step" in text:
    return {
      "diagram_type": "UML Sequence Diagram", 
      "reasoning": "Meeting discusses process flow and steps"
    }
  
  elif "process" in text or "workflow" in text or "decision" in text:
    return {
      "diagram_type": "Flowchart",
      "reasoning": "Meeting discusses business processes"
    }
  
  elif "component" in text or "system" in text or "architecture" in text:
    return {
      "diagram_type": "Component Diagram",
      "reasoning": "Meeting discusses system components"
    }
  
  elif "user" in text or "actor" in text or "requirement" in text:
    return {
      "diagram_type": "Use Case Diagram",
      "reasoning": "Meeting discusses user requirements"
    }
  
  else:
    return {
      "diagram_type": "Flowchart",
      "reasoning": "Default choice - general process"
    }
  """

  # Get IAM token
  token_resp = requests.post(
    "https://iam.cloud.ibm.com/identity/token",
    data={
      "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
      "apikey": api_key
    }
  )
  access_token = token_resp.json()["access_token"]

  # Prepare prompt
  prompt = f"""
  Analyze this meeting transcript and determine the most appropriate diagram type:

  \"{transcript}\"

  Choose from the supported UML diagrams: Sequence diagram, Usecase diagram, Class diagram, Object diagram, Activity diagram, Component diagram, Deployment diagram, State diagram, Timing diagram, ER diagram

  Provide your response in this exact JSON format:
  {{
    "diagram_type": "chosen_diagram_type",
    "confidence": 0.85,
    "reasoning": "explanation of why this diagram fits",
    "keywords": ["keyword1", "keyword2", "keyword3"]
  }}
  """

# Example usage
if __name__ == "__main__":
  # Test with a sample transcript
  # sample = "We discussed the User class with attributes and methods"
  # result = analyze_meeting(sample)
  # print(f"Input: {sample}")
  # print(f"Result: {result['diagram_type']} - {result['reasoning']}")
  transcript = "We discussed the user authentication flow and the steps for login and permission checking."
  api_key = "YOUR_API_KEY"
  project_id = "YOUR_PROJECT_ID"
  endpoint_url = "https://eu-de.ml.cloud.ibm.com"

  result = analyze_meeting(transcript, api_key, project_id, endpoint_url)
  print(result)