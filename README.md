# Self-Prompting AI Agent with Gemini-Claude Collaboration

This project implements an AI agent that leverages both Google's Gemini and Anthropic's Claude APIs to create a sophisticated prompt generation and evaluation system. Gemini generates creative prompts which are then processed by Claude, creating a unique synergy between the two AI models for mutation, vectoring, probing and discovery.

## Features

- Gemini-powered prompt generation
- Claude-powered response generation and evaluation
- Cross-model analysis and feedback
- Historical prompt and evaluation tracking
- Dynamic prompt evolution based on both models' insights
- Detailed analysis from both AI perspectives

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/kinzozi/CollaborativeAI.git
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with your API keys:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

Run the agent from Unix CLI / Terminal:
```
python3 self_prompting_agent.py
```

The agent will start an interactive session where you can:
- Enter topics for prompt generation
- See Gemini's generated prompts
- View Claude's responses
- Get evaluations from both AI models
- See how the models learn from each other
- Type 'quit' to exit

## How it Works

1. User provides a topic
2. Gemini generates a creative prompt based on the topic and previous interactions
3. Claude processes the Gemini-generated prompt and creates a response
4. Claude evaluates the effectiveness of Gemini's prompt
5. Gemini analyzes the interaction and provides insights
6. Both models learn from each interaction to improve future prompts
7. This creates a continuous learning loop where both models contribute to better results

## Model Roles

### Gemini
- Generates creative and contextual prompts
- Analyzes the interaction between its prompts and Claude's responses
- Provides insights for improvement

### Claude
- Processes Gemini's prompts
- Generates detailed responses
- Evaluates prompt effectiveness
- Provides feedback for prompt improvement 
