#!/bin/bash
# Script to generate a new Next.js component with TypeScript

COMPONENT_NAME=$1
COMPONENT_TYPE=$2  # "client" or "server" (default: server)

if [ -z "$COMPONENT_NAME" ]; then
    echo "Usage: $0 <component-name> [component-type]"
    echo "Component type can be 'client' or 'server' (default: server)"
    exit 1
fi

if [ -z "$COMPONENT_TYPE" ]; then
    COMPONENT_TYPE="server"
fi

# Create component directory if it doesn't exist
mkdir -p components

if [ "$COMPONENT_TYPE" = "client" ]; then
    # Generate client component
    cat > "components/${COMPONENT_NAME}.tsx" << EOF
'use client';

import React from 'react';

interface ${COMPONENT_NAME}Props {
  // Define your props here
}

export const ${COMPONENT_NAME}: React.FC<${COMPONENT_NAME}Props> = ({}) => {
  return (
    <div className="${COMPONENT_NAME}-container">
      <h1>${COMPONENT_NAME} Component</h1>
      {/* Add your component content here */}
    </div>
  );
};

export default ${COMPONENT_NAME};
EOF
    echo "Client component ${COMPONENT_NAME} created at components/${COMPONENT_NAME}.tsx"
else
    # Generate server component
    cat > "components/${COMPONENT_NAME}.tsx" << EOF
import React from 'react';

interface ${COMPONENT_NAME}Props {
  // Define your props here
}

const ${COMPONENT_NAME}: React.FC<${COMPONENT_NAME}Props> = ({}) => {
  return (
    <div className="${COMPONENT_NAME}-container">
      <h1>${COMPONENT_NAME} Component</h1>
      {/* Add your component content here */}
    </div>
  );
};

export default ${COMPONENT_NAME};
EOF
    echo "Server component ${COMPONENT_NAME} created at components/${COMPONENT_NAME}.tsx"
fi