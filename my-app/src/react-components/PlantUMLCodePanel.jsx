import React from 'react';

const PlantUMLCodePanel = () => {
  const placeholderCode = `@startuml
class ClassName {
  -attribute1: Type
  +method1(): ReturnType
  #method2(param: Type): void
}

class AnotherClass {
  -attribute2: Type
  +method3(): ReturnType
}

ClassName --> AnotherClass : association
@enduml`;

  return (
    <div className="plantuml-code-container">
      <div className="panel-header">
        <h3>PlantUML Code</h3>
      </div>
      <div className="code-editor">
        <pre className="code-content">
          <code>{placeholderCode}</code>
        </pre>
      </div>
    </div>
  );
};

export default PlantUMLCodePanel;
