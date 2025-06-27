# TalkToTech

## AI & Automation Unpacked Hackathon Submission

This repository showcases AI-powered automation solutions developed during the **IBM AI & Automation Unpacked Hackathon**. Our project focuses on leveraging **IBM Granite models**, accessible via open-source platforms or **IBM watsonx.ai**, to create innovative tools that enhance efficiency and transform business processes.

---

## 🚀 The Challenge

The hackathon's core objective was to design and build proof-of-concept AI solutions using IBM Granite models (including Granite 3.3 for reasoning and speech, and Granite 4.0 Tiny for long-context tasks). These models are designed for enterprise applications, enabling automation, enhanced decision-making, and innovation across various domains.

---

## ✨ Our Solution

*(This section will be detailed by your team, outlining your specific project idea, its features, and how it utilizes IBM Granite models to solve a particular problem, e.g., a smart meeting summarizer or a diagram generator.)*

### Team Members

* **Ahmed Dabour**
* **Hatem Soliman**
* **Layla Khaled**
* **Salma Tarek Soliman**
* **Yasmeen Tarek**

### 🎯 Your Solution: Smart Meeting-to-Diagram Generator

Your merged idea combining **Smart Meeting Recap/Notes** with **Diagram Generator** is brilliant because:

#### **Why This Solution Stands Out:**

1. **Multi-Modal Granite Integration**: You're leveraging multiple Granite models effectively:
   - **Granite Speech 8B** for speech-to-text (meeting transcription)
   - **Granite 3.3 8B Instruct** for reasoning and summarization
   - **Granite Code** for code generation
   - **Granite Vision** for diagram interpretation

2. **Real Business Value**: This directly addresses the hackathon's goal of "streamlining everyday business processes" - meetings are a universal pain point in business!

3. **Technical Innovation**: The workflow you've designed is sophisticated:

   ```text
   Speech → Text → Analysis → Diagram Selection → Code Generation → Visual Output
   ```

### 🏗️ **Modular Development Strategy**

Our approach focuses on **independent, modular components** that can be developed and tested separately:

#### **Why Modular Development?**
- **Independent Testing**: Each team member can test their component without waiting for others
- **Cloud-First**: Components can be tested online (watsonx.ai) without heavy downloads
- **Progress Tracking**: Local IDE development with GitHub commits for version control
- **Easy Integration**: Components can be connected later without major refactoring

#### **Project Structure**
```
talk-to-tech-ibm/
├── components/
│   ├── speech_to_text/          # Ahmed Dabour
│   │   ├── granite_speech.py
│   │   ├── test_speech.py
│   │   └── README.md
│   ├── diagram_selector/        # Hatem Soliman
│   │   ├── granite_reasoning.py
│   │   ├── diagram_classifier.py
│   │   ├── test_classifier.py
│   │   └── README.md
│   ├── code_generator/          # Salma Tarek Soliman
│   │   ├── granite_code.py
│   │   ├── uml_generator.py
│   │   ├── test_generator.py
│   │   └── README.md
│   ├── diagram_renderer/        # Layla Khaled
│   │   ├── plantuml_renderer.py
│   │   ├── diagram_templates.py
│   │   ├── test_renderer.py
│   │   └── README.md
│   └── vision_processor/        # Yasmeen Tarek
│       ├── granite_vision.py
│       ├── image_analyzer.py
│       ├── test_vision.py
│       └── README.md
├── integration/
│   ├── orchestrator.py          # Main workflow coordinator
│   ├── api_connector.py         # watsonx.ai API management
│   └── test_integration.py
├── data/
│   ├── sample_meetings/         # Test meeting transcripts
│   ├── sample_diagrams/         # Expected outputs
│   └── config/
│       └── watsonx_config.json  # API credentials (gitignored)
├── docs/
│   ├── api_documentation.md
│   ├── setup_guide.md
│   └── testing_guide.md
├── requirements.txt
├── .gitignore
└── README.md
```

#### **Development Workflow**
1. **Independent Development**: Each team member works on their component
2. **Cloud Testing**: Use watsonx.ai Prompt Lab for AI model testing
3. **Local Development**: Write code in local IDE with minimal dependencies
4. **GitHub Tracking**: Regular commits to track progress
5. **Integration Testing**: Connect components when ready

---

## 🛠️ Technologies Used

* **IBM Granite Models:** Leveraging their capabilities for text generation, reasoning, summarization, and potentially speech-to-text.
* **IBM watsonx.ai:** The cloud-based platform for accessing and experimenting with Granite models via Prompt Lab, API, and SDK.
* **[Potentially] Open-source platforms:** Such as Hugging Face for model access, Ollama for local inference, or the BeeAI Agentic Framework for building intelligent agents.
* *(Add any other specific tools, frameworks, or programming languages relevant to your project, e.g., Python, LangChain, etc.)*

---

## 📝 Getting Started

To explore or run components of this project:

### Prerequisites

* Familiarity with **IBM Granite models** and their applications.
* Understanding of **IBM watsonx.ai** for cloud-based model interaction.
* Basic concepts of **AI automation** and **Large Language Models (LLMs)**.
* *(Specify any required programming languages or development environments.)*

### Installation & Setup

*(Provide clear instructions on how to set up and run your specific solution. This might include API key configuration, environment variables, and dependency installation.)*

For general hackathon guidelines on using IBM Granite, please refer to the **AI & Automation Unpacked Hackathon Guide PDF**. This guide covers:

* Accessing Granite models on Hugging Face or via Ollama for local execution.
* Using IBM watsonx.ai's Prompt Lab and programmatic access (API/SDK).
* System requirements for local model inference (e.g., 32 GB RAM, GPU).

---

## 💡 Use Cases Addressed

*(Based on your team's project, briefly describe the specific business process or industry challenge your solution aims to automate or improve. Referencing the example use cases from the hackathon guide, such as "Smart Meeting Summarizer" or "AI Workflow Orchestrator," can be helpful.)*

---

## ⚠️ Data Compliance Notice

In adherence to the hackathon guidelines, all data used in this project complies with responsible AI practices. We have ensured:

* No company confidential or unauthorized data.
* No client data or Personally Identifiable Information (PI).
* No data obtained from social media.
* Publicly available data, where terms permit commercial use, is documented.

---

## 🔗 Resources

* [IBM Granite Official Page](https://www.ibm.com/granite)
* [IBM Granite Documentation (IBM Developer)](https://developer.ibm.com/components/granite-models/)
* [IBM watsonx.ai Platform](https://dataplatform.cloud.ibm.com/wx/home?context=wx)
* [BeeAI Agentic Framework GitHub (if used)](https://github.com/IBM/BeeAI)
* *(Add links to any other significant external resources or documentation relevant to your specific implementation.)*

---

## License

MIT License

Copyright (c) 2024 TalkToTech Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---