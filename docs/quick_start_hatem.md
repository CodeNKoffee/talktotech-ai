# Quick Start Guide - Hatem's Diagram Selector Component

## 🚀 Immediate Next Steps

### 1. Set Up Your Environment (5 minutes)

```bash
# Clone the repository (if not already done)
git clone <your-repo-url>
cd talk-to-tech-ibm

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install minimal dependencies
pip install -r requirements.txt
```

### 2. Test Your Component Locally (10 minutes)

```bash
# Navigate to your component
cd components/diagram_selector

# Run the classifier directly
python diagram_classifier.py

# Run unit tests
python -m pytest test_classifier.py -v
```

### 3. Set Up IBM Cloud Account (15 minutes)

1. Go to: https://www.ibm.com/account/reg/us-en/signup?formid=urx-53809
2. Create IBM Cloud account with your hackathon email
3. Access watsonx.ai: https://dataplatform.cloud.ibm.com/wx/home?context=wx
4. Select "Dallas" region when prompted

### 4. Experiment with Prompt Lab (30 minutes)

1. Click "Open Prompt Lab" in watsonx.ai
2. Change model to "Granite 3.3 8B Instruct"
3. Test this prompt:

   ```text
   Analyze this meeting transcript and determine the most appropriate diagram type:
   
   "We discussed the user authentication flow. When a user logs in, the system first validates their credentials, then checks their permissions, and finally grants access to the appropriate modules."
   
   Choose from: UML Class Diagram, UML Sequence Diagram, Flowchart, Component Diagram, Use Case Diagram, Activity Diagram
   
   Provide your reasoning and confidence level.
   ```

## 🧪 Testing Strategy

### Independent Testing (No Dependencies)

```python
# Test with sample data
from diagram_classifier import DiagramClassifier

classifier = DiagramClassifier()
result = classifier.analyze_content("Your meeting transcript here")
print(f"Recommended: {result.diagram_type}")
print(f"Confidence: {result.confidence}")
print(f"Reasoning: {result.reasoning}")
```

### Sample Data Testing

```python
import json

# Load sample meetings
with open('data/sample_meetings/sample_transcripts.json', 'r') as f:
    samples = json.load(f)['sample_meetings']

# Test each sample
for meeting in samples:
    result = classifier.analyze_content(meeting['transcript'])
    print(f"{meeting['title']}: {result.diagram_type} (confidence: {result.confidence:.2f})")
```

## 🔄 Development Workflow

### Day 1: Foundation
- ✅ Set up local environment
- ✅ Test component independently
- ✅ Set up IBM Cloud account
- ✅ Experiment with Prompt Lab

### Day 2: Enhancement

- 🔄 Improve classification logic
- 🔄 Add more diagram types if needed
- 🔄 Test with more sample data
- 🔄 Document your findings

### Day 3: Integration Preparation

- 🔄 Create API integration layer
- 🔄 Coordinate with team members
- 🔄 Prepare for component integration

## 💡 Tips for Success

### Resource Management

- **Use Prompt Lab extensively** - it's included in your $100 credits
- **Cache results** - avoid redundant API calls
- **Monitor credit usage** - you'll get alerts at 25%, 50%, 80%

### Code Quality
- **Write tests first** - ensures your logic works
- **Use type hints** - makes integration easier
- **Document your decisions** - helps team understand your approach

### Team Coordination

- **Commit regularly** - track your progress
- **Share sample outputs** - helps team understand your component
- **Coordinate interfaces** - ensure your output matches team expectations

## 🎯 Expected Output Format

Your component should return:

```json
{
  "diagram_type": "UML Sequence Diagram",
  "confidence": 0.85,
  "reasoning": "Meeting focuses on process flows and interactions with keywords: sequence, interaction, flow. UML Sequence Diagram shows message exchanges and timing.",
  "keywords": ["sequence", "interaction", "flow", "process"]
}
```

## 🆘 Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're in the right directory
2. **Test failures**: Check that sample data matches expected outputs
3. **API access issues**: Verify IBM Cloud account setup
4. **Credit exhaustion**: Monitor usage and optimize API calls

### Getting Help

- Check the main README.md for project overview
- Review team member READMEs for integration points
- Use the sample data for testing edge cases

## 📊 Success Metrics

Track these metrics:

- **Accuracy**: How often your recommendations match expected diagrams
- **Confidence**: Average confidence scores for recommendations
- **Coverage**: How many different diagram types you can identify
- **Performance**: Response time and resource usage
