"""
Meeting data management using AI-powered diagram classification.
Integrates with diagram_classifier to analyze meeting transcripts and determine diagram types.
"""

import sys
import os

# Add the diagram_selector directory to the path so we can import diagram_classifier
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'diagram_selector'))

from diagram_classifier import analyze_meeting

# Storage for processed meetings
PROCESSED_MEETINGS = []

def process_meeting_transcript(transcript: str) -> dict:
    """
    Process a meeting transcript using AI-powered diagram classification.
    
    Args:
        transcript: Raw meeting transcript text
        
    Returns:
        A dictionary containing the processed meeting data with AI-generated insights
    """
    meeting_data = analyze_meeting(transcript)
    PROCESSED_MEETINGS.append(meeting_data)
    return meeting_data

def get_meeting_by_id(meeting_id: str) -> dict:
    """Get a specific meeting by ID from processed meetings"""
    return next((meeting for meeting in PROCESSED_MEETINGS if meeting["id"] == meeting_id), None)

def get_meetings_by_diagram_type(diagram_type: str) -> list:
    """Get all processed meetings that generate a specific diagram type"""
    return [meeting for meeting in PROCESSED_MEETINGS 
            if diagram_type in meeting.get("output_diagram", [])]

def get_all_diagram_types() -> list:
    """Get list of all unique diagram types from processed meetings"""
    diagram_types = set()
    for meeting in PROCESSED_MEETINGS:
        diagram_types.update(meeting.get("output_diagram", []))
    return list(diagram_types)

def get_all_processed_meetings() -> list:
    """Get all processed meetings"""
    return PROCESSED_MEETINGS.copy()

def clear_processed_meetings():
    """Clear all processed meetings (useful for testing or reset)"""
    global PROCESSED_MEETINGS
    PROCESSED_MEETINGS = []

def get_meetings_by_keyword(keyword: str) -> list:
    """Get all meetings that contain a specific keyword"""
    return [meeting for meeting in PROCESSED_MEETINGS 
            if keyword.lower() in [kw.lower() for kw in meeting.get("keywords", [])]]
