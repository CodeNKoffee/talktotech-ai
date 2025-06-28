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
    def __init__(self, plantuml_jar_path: str = None, output_dir: str = "./output"):
        """Initialize the SVGConverter with PlantUML JAR path and output directory."""

        abs_path = os.path.abspath("../lib/plantuml-1.2025.3.jar")
        if os.path.exists(abs_path):
            plantuml_jar_path = abs_path
            
        if plantuml_jar_path is None:
            plantuml_jar_path = os.path.join(os.path.dirname(__file__), "..", "lib", "plantuml-1.2025.3.jar")
    
        self.plantuml_jar_path = plantuml_jar_path
        self.output_dir = output_dir
        self.jvm_started = False
        self.jar_available = self._check_jar_availability()
        
        # Try to download JAR if not available
        if not self.jar_available:
            print("PlantUML JAR not found, attempting to download...")
            self.jar_available = self._download_plantuml_jar()
        
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
                print(f"Starting JVM with PlantUML JAR: {self.plantuml_jar_path}")
                jpype.startJVM(
                    classpath=[self.plantuml_jar_path],
                    jvmpath=jpype.getDefaultJVMPath(),
                    convertStrings=True
                )
                self.jvm_started = True
                print("JVM started successfully")
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

        # Method 2: Try command-line Java with JAR
        result = self._convert_with_java_command(plantuml_code, output_file)
        if result["success"]:
            return result

        # Method 3: Try online PlantUML server as last resort
        result = self._convert_with_online_server(plantuml_code, output_file)
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
            output_stream = FileOutputStream(output_file)
            reader.outputImage(output_stream, FileFormatOption(FileFormat.SVG))
            output_stream.close()
            
            # Verify the file was created and read its content
            if os.path.exists(output_file):
                with open(output_file, "r", encoding="utf-8") as f:
                    svg_content = f.read()
                    
                return {
                    "success": True,
                    "output_file": output_file,
                    "svg_content": svg_content,
                    "errors": []
                }
            else:
                return {"success": False, "errors": ["SVG file was not created"]}
                
        except Exception as e:
            return {"success": False, "errors": [f"JPype conversion failed: {str(e)}"]}

    def _convert_with_java_command(self, plantuml_code: str, output_file: str) -> dict:
        """Convert using Java command line with PlantUML JAR."""
        if not self.jar_available:
            return {"success": False, "errors": ["PlantUML JAR not available"]}

        try:
            # Create temporary file for PlantUML input
            with tempfile.NamedTemporaryFile(mode='w', suffix='.puml', delete=False) as temp_file:
                temp_file.write(plantuml_code)
                temp_input = temp_file.name

            # Run Java command to generate SVG
            cmd = [
                'java', '-jar', self.plantuml_jar_path,
                '-tsvg', '-o', self.output_dir, temp_input
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Clean up temporary file
            os.unlink(temp_input)
            
            if result.returncode == 0 and os.path.exists(output_file):
                with open(output_file, "r", encoding="utf-8") as f:
                    svg_content = f.read()
                    
                return {
                    "success": True,
                    "output_file": output_file,
                    "svg_content": svg_content,
                    "errors": []
                }
            else:
                return {"success": False, "errors": [f"Java command failed: {result.stderr}"]}
                
        except Exception as e:
            return {"success": False, "errors": [f"Java command conversion failed: {str(e)}"]}

    def _convert_with_online_server(self, plantuml_code: str, output_file: str) -> dict:
        """Convert using PlantUML online server as last resort."""
        try:
            import base64
            import zlib
            
            # Encode PlantUML code for URL
            compressed = zlib.compress(plantuml_code.encode('utf-8'))
            encoded = base64.b64encode(compressed).decode('ascii')
            
            # Use PlantUML online server
            url = f"http://www.plantuml.com/plantuml/svg/{encoded}"
            
            print(f"Attempting to use online PlantUML server...")
            response = urllib.request.urlopen(url, timeout=10)
            svg_content = response.read().decode('utf-8')
            
            # Save to file
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(svg_content)
                
            return {
                "success": True,
                "output_file": output_file,
                "svg_content": svg_content,
                "errors": []
            }
            
        except Exception as e:
            return {"success": False, "errors": [f"Online server conversion failed: {str(e)}"]}

    def __del__(self):
        """Shutdown JVM when the object is destroyed."""
        if self.jvm_started and jpype.isJVMStarted():
            jpype.shutdownJVM()