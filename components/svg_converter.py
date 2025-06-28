import jpype
import jpype.imports
from jpype.types import *
import os
from pathlib import Path
from typing import Dict, List

class SVGConverter:
    def __init__(self, plantuml_jar_path: str = "./lib/plantuml-1.2025.3.jar", output_dir: str = "./output"):
        """Initialize the SVGConverter with PlantUML JAR path and output directory."""
        self.plantuml_jar_path = plantuml_jar_path
        self.output_dir = output_dir
        self.jvm_started = False
        self.start_jvm()  # Start JVM on initialization

    def start_jvm(self):
        """Start the JVM with PlantUML classpath."""
        if not self.jvm_started:
            try:
                jpype.startJVM(
                    classpath=[self.plantuml_jar_path],
                    jvmpath=jpype.getDefaultJVMPath(),
                    convertStrings=True
                )
                self.jvm_started = True
            except Exception as e:
                raise RuntimeError(f"Failed to start JVM: {str(e)}")

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
        """Convert PlantUML code to SVG format."""
        errors = []
        output_file = os.path.join(self.output_dir, "diagram.svg")
        os.makedirs(self.output_dir, exist_ok=True)  # Ensure output directory exists

        if not self.validate_plantuml(plantuml_code):
            return {
                "success": False,
                "output_file": "",
                "errors": ["Invalid PlantUML code: Missing @startuml or @enduml"]
            }

        try:
            from net.sourceforge.plantuml import SourceStringReader, FileFormatOption, FileFormat
            from java.io import FileOutputStream
        except Exception as e:
             raise ImportError(f"Failed to import PlantUML classes: {str(e)}")

        try:
            reader = SourceStringReader(plantuml_code)
            with open(output_file, "wb") as f:
                output_stream = FileOutputStream(output_file)
                reader.outputImage(output_stream, FileFormatOption(FileFormat.SVG))
                output_stream.close()
            with open(output_file, "r", encoding="utf-8") as f:
                svg_content = f.read()
                output_file_path = output_file
        except jpype.JException as e:
            errors.append(f"PlantUML syntax error: {str(e)}")
        except Exception as e:
            errors.append(f"PlantUML error: {str(e)}")

        return {
            "success": not errors,
            "output_file": output_file if not errors else "",
            "svg_content": svg_content if not errors else "",
            "errors": errors
        }

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
    converter = SVGConverter()
    result = converter.convert_to_svg(plantuml_code)

    # Output result
    print(f"Status: {'Success' if result['success'] else 'Failed'}")
    print(f"SVG Content: {result['svg_content']}")
    print(f"Output file: {result['output_file']}")
    if result['errors']:
        print(f"Errors: {', '.join(result['errors'])}")