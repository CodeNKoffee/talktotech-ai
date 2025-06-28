import jpype
import jpype.imports
from jpype.types import *
import os
from pathlib import Path
from typing import Dict, List
import urllib.request
import tempfile
import subprocess

class SVGConverter:
    def __init__(self, plantuml_jar_path: str = "./lib/plantuml-1.2025.3.jar", output_dir: str = "./output"):
        """Initialize the SVGConverter with PlantUML JAR path and output directory."""
        self.plantuml_jar_path = plantuml_jar_path
        self.output_dir = output_dir
        self.jvm_started = False
        self.jar_available = self._check_jar_availability()
        
        # Only start JVM if JAR is available
        if self.jar_available:
            self.start_jvm()

    def _check_jar_availability(self) -> bool:
        """Check if the PlantUML JAR file exists."""
        return os.path.exists(self.plantuml_jar_path)

    def _download_plantuml_jar(self) -> bool:
        """Download PlantUML JAR if it doesn't exist."""
        if self.jar_available:
            return True
            
        try:
            # Create lib directory if it doesn't exist
            lib_dir = os.path.dirname(self.plantuml_jar_path)
            os.makedirs(lib_dir, exist_ok=True)
            
            # Download PlantUML JAR
            plantuml_url = "https://github.com/plantuml/plantuml/releases/download/v1.2025.3/plantuml-1.2025.3.jar"
            print(f"Downloading PlantUML JAR from {plantuml_url}...")
            urllib.request.urlretrieve(plantuml_url, self.plantuml_jar_path)
            
            if os.path.exists(self.plantuml_jar_path):
                self.jar_available = True
                print(f"PlantUML JAR downloaded successfully to {self.plantuml_jar_path}")
                return True
            else:
                print("Failed to download PlantUML JAR")
                return False
                
        except Exception as e:
            print(f"Error downloading PlantUML JAR: {str(e)}")
            return False

    def start_jvm(self):
        """Start the JVM with PlantUML classpath."""
        if not self.jvm_started and self.jar_available:
            try:
                jpype.startJVM(
                    classpath=[self.plantuml_jar_path],
                    jvmpath=jpype.getDefaultJVMPath(),
                    convertStrings=True
                )
                self.jvm_started = True
            except Exception as e:
                print(f"Warning: Failed to start JVM: {str(e)}")
                self.jvm_started = False

    def validate_plantuml(self, code: str) -> bool:
        """Basic validation of PlantUML code."""
        code = code.strip()
        if not code:
            return False
        if "@startuml" not in code.lower():
            return False
        if "@enduml" not in code.lower():
            return False
        return True

    def convert_to_svg(self, plantuml_code: str) -> dict:
        """Convert PlantUML code to SVG format using multiple fallback methods."""
        output_file = os.path.join(self.output_dir, "diagram.svg")
        os.makedirs(self.output_dir, exist_ok=True)  # Ensure output directory exists

        if not self.validate_plantuml(plantuml_code):
            return {
                "success": False,
                "output_file": "",
                "svg_content": "",
                "errors": ["Invalid PlantUML code: Missing @startuml or @enduml"]
            }

        # Method 1: Try JPype with PlantUML JAR (if available)
        result = self._convert_with_jpype(plantuml_code, output_file)
        if result["success"]:
            return result

        return {
            "success": False,
            "output_file": "",
            "svg_content": "",
            "errors": ["All conversion methods failed. Please ensure PlantUML is installed or JAR is available."]
        }

    def _convert_with_jpype(self, plantuml_code: str, output_file: str) -> dict:
        """Convert using JPype and PlantUML JAR."""
        if not self.jvm_started or not self.jar_available:
            return {"success": False, "errors": ["JVM not started or JAR not available"]}

        try:
            from net.sourceforge.plantuml import SourceStringReader, FileFormatOption, FileFormat
            from java.io import FileOutputStream
            
            reader = SourceStringReader(plantuml_code)
            with open(output_file, "wb") as f:
                output_stream = FileOutputStream(output_file)
                reader.outputImage(output_stream, FileFormatOption(FileFormat.SVG))
                output_stream.close()
            
            with open(output_file, "r", encoding="utf-8") as f:
                svg_content = f.read()
                
            return {
                "success": True,
                "output_file": output_file,
                "svg_content": svg_content,
                "errors": []
            }
        except Exception as e:
            return {"success": False, "errors": [f"JPype conversion failed: {str(e)}"]}

    def __del__(self):
        """Shutdown JVM when the object is destroyed."""
        if self.jvm_started and jpype.isJVMStarted():
            jpype.shutdownJVM()

if __name__ == "__main__":
    # Sample PlantUML code
    plantuml_code = """
    @startuml
    skinparam monochrome true
    skinparam shadowing false
    skinparam style strictuml

    participant User
    participant System

    User -> System : request
    activate System
    System --> User : response
    deactivate System

    note right of System : Interaction
    @enduml
    """

    # Create converter instance and convert
    print("Initializing SVG Converter...")
    converter = SVGConverter()
    
    print("Converting PlantUML to SVG...")
    result = converter.convert_to_svg(plantuml_code)

    # Output result
    print(f"\nConversion Status: {'Success' if result['success'] else 'Failed'}")
    
    if result['success']:
        print(f"Output file: {result['output_file']}")
        print(f"SVG content length: {len(result['svg_content'])} characters")
        print("First 200 characters of SVG:")
        print(result['svg_content'][:200] + "..." if len(result['svg_content']) > 200 else result['svg_content'])
    else:
        print("Errors encountered:")
        for error in result['errors']:
            print(f"  - {error}")