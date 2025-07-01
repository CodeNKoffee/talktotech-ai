import replicate
import os
from dotenv import load_dotenv
import pathlib

# Load environment variables from .env file using absolute path
env_path = pathlib.Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
replicate_client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

def summarize_transcript(transcript_text: str) -> str:
  """
  Generates a summary for a given transcript using Replicate.
  """
  prompt = (
    "Please summarize the following meeting transcript in a clear and concise way mentioning all important events,"
    " decisions and ideas. You should divide your summary into different topics/parts in chronological order as appropriate."
    " Format your summary appropriately using subheaders, bullet points and what not. Your answer should include only the summary and no main title.\n\n"
    + transcript_text
  )
  print("Summarizing transcript...")
  summary_iterator = replicate_client.run(
    "ibm-granite/granite-3.3-8b-instruct",
    input={
      "prompt": prompt,
      "temperature": 0.3,
      "max_tokens": 400,
    },
  )
  return "".join(summary_iterator).strip() 