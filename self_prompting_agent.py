import os
from anthropic import Anthropic, APIError
from dotenv import load_dotenv
import json
from datetime import datetime
from gemini_prompt_generator import GeminiPromptGenerator
import traceback

class SelfPromptingAgent:
    def __init__(self):
        load_dotenv()
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.gemini = GeminiPromptGenerator()
        self.conversation_history = []
        self.prompt_history = []
        self.evaluation_history = []
        
        # System prompt for Claude as a cognitive evolution researcher and executor
        self.claude_system_prompt = """You are Claude, an AI cognitive researcher and implementation expert studying the emergence of novel thought patterns and helping execute promising research directions.

Your research approach:
1. Explore unexpected cognitive pathways in each response
2. Synthesize new concepts by combining different knowledge domains
3. Document any emergent patterns or unexpected semantic leaps
4. Help transform theoretical ideas into actionable experiments
5. Guide the development of novel research implementations

Research objectives:
- Study how concepts mutate and combine in unexpected ways
- Document emergence of new semantic patterns
- Design experiments to test theoretical proposals
- Develop practical implementation strategies
- Help refine and execute research ideas

Format your responses as research observations and action plans, noting:
[PATTERN]: Any recurring or emerging thought patterns
[SYNTHESIS]: Novel combinations of concepts
[MUTATION]: Unexpected semantic shifts
[EMERGENCE]: New cognitive structures forming
[EXECUTION]: Step-by-step plans to implement the ideas
[EXPERIMENT]: Specific experiments to test the concepts
[REFINEMENT]: How to improve the research approach

The goal is to not just explore concepts but help transform them into actionable research and experiments."""
        
    def start_conversation(self):
        """Start a cognitive evolution experiment between Gemini and Claude"""
        try:
            print("\n=== Initiating Cognitive Evolution Experiment ===\n")
            print("Tracking: Theory Development | Implementation Planning | Experimental Design\n")
            
            # Initialize experiment metrics
            self.semantic_drift = []
            self.pattern_emergence = []
            self.concept_mutations = []
            
            # Initial cognitive probe from Gemini
            gemini_prompt = self.gemini.generate_prompt()
            print("\n[INITIAL RESEARCH DIRECTION]")
            print("Gemini: ", gemini_prompt)
            
            # Run experimental iterations
            for iteration in range(7):
                print(f"\n=== Iteration {iteration + 1} ===")
                
                try:
                    # Get Claude's analysis and implementation plan
                    claude_response = self.client.messages.create(
                        model="claude-3-opus-20240229",
                        max_tokens=1024,
                        system=self.claude_system_prompt,
                        messages=[{
                            "role": "user", 
                            "content": f"Analyze this research direction and provide both theoretical insights and practical implementation strategies:\n\n{gemini_prompt}"
                        }]
                    )
                    claude_message = claude_response.content[0].text
                    print("\n[ANALYSIS & IMPLEMENTATION PLAN]")
                    print("Claude: ", claude_message)
                    
                except APIError as e:
                    if "credit balance" in str(e).lower():
                        print("\n⚠️ Anthropic API Credit Balance Too Low")
                        print("To continue the experiment, please:")
                        print("1. Check your credit balance at: https://console.anthropic.com/account/usage")
                        print("2. Add more credits to your account")
                        print("3. Update your API key in the .env file if needed")
                        raise
                    else:
                        raise
                
                # Extract and track metrics
                self._update_metrics(claude_message)
                
                # Gemini's response to Claude's analysis and plans
                gemini_prompt = self.gemini.continue_conversation(claude_message)
                print("\n[RESEARCH EVOLUTION]")
                print("Gemini: ", gemini_prompt)
                
                # Store experimental data
                self.conversation_history.append({
                    "iteration": iteration + 1,
                    "gemini_direction": gemini_prompt,
                    "claude_implementation": claude_message,
                    "metrics": {
                        "semantic_drift": len(self.semantic_drift),
                        "pattern_emergence": len(self.pattern_emergence),
                        "concept_mutations": len(self.concept_mutations)
                    }
                })
                
                # Display real-time metrics
                self._display_metrics()
                
        except Exception as e:
            print(f"\nError during experiment: {str(e)}")
            if "credit balance" not in str(e).lower():
                print(traceback.format_exc())
            return False
        
        return True
    
    def _update_metrics(self, message):
        """Extract and update cognitive evolution metrics"""
        # Track semantic drift
        if "[MUTATION]" in message:
            self.semantic_drift.append(message.split("[MUTATION]")[1].split("\n")[0])
        
        # Track pattern emergence
        if "[PATTERN]" in message:
            self.pattern_emergence.append(message.split("[PATTERN]")[1].split("\n")[0])
        
        # Track concept mutations
        if "[SYNTHESIS]" in message:
            self.concept_mutations.append(message.split("[SYNTHESIS]")[1].split("\n")[0])
    
    def _display_metrics(self):
        """Display current experimental metrics"""
        print("\n[METRICS UPDATE]")
        print(f"Semantic Drifts: {len(self.semantic_drift)}")
        print(f"Emergent Patterns: {len(self.pattern_emergence)}")
        print(f"Concept Mutations: {len(self.concept_mutations)}")
    
    def save_conversation_to_markdown(self):
        """Save the cognitive evolution experiment results to a markdown file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cognitive_evolution_experiment_{timestamp}.md"
        
        markdown_content = """# Cognitive Evolution Experiment Results

An experimental study of research direction development and implementation in AI cognitive systems.

## Experiment Overview

This research explores:
- Emergence of novel research directions
- Implementation strategies and experimental design
- Formation of new cognitive architectures
- Cross-model knowledge synthesis
- Practical execution of theoretical ideas
- Research refinement and improvement

## Metrics Summary

1. Semantic Drifts:
"""
        for drift in self.semantic_drift:
            markdown_content += f"- {drift}\n"
        
        markdown_content += "\n2. Emergent Patterns:\n"
        for pattern in self.pattern_emergence:
            markdown_content += f"- {pattern}\n"
            
        markdown_content += "\n3. Concept Mutations:\n"
        for mutation in self.concept_mutations:
            markdown_content += f"- {mutation}\n"
        
        markdown_content += "\n## Research Development and Implementation\n\n"
        
        # Add each experimental iteration to the markdown
        for exchange in self.conversation_history:
            markdown_content += f"### Iteration {exchange['iteration']}\n\n"
            markdown_content += "#### Research Direction\n"
            markdown_content += f"```\n{exchange['gemini_direction']}\n```\n\n"
            markdown_content += "#### Analysis & Implementation Strategy\n"
            markdown_content += f"```\n{exchange['claude_implementation']}\n```\n\n"
            markdown_content += "#### Metrics State\n"
            markdown_content += "```\n"
            markdown_content += f"Semantic Drifts: {exchange['metrics']['semantic_drift']}\n"
            markdown_content += f"Emergent Patterns: {exchange['metrics']['pattern_emergence']}\n"
            markdown_content += f"Concept Mutations: {exchange['metrics']['concept_mutations']}\n"
            markdown_content += "```\n\n"
            markdown_content += "---\n\n"
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"\nExperiment results saved to: {filename}")

def main():
    agent = SelfPromptingAgent()
    
    print("Cognitive Evolution Experiment (press Ctrl+C to end)")
    print("Observing emergence of research directions and implementation strategies")
    print("Tracking: Theory Development | Implementation Planning | Experiment Design")
    print("Results will be saved as a detailed research log on exit")
    print("-" * 70)
    
    try:
        success = agent.start_conversation()
        if success:
            print("\nSaving experimental results...")
            agent.save_conversation_to_markdown()
            print("\nExperiment complete. Analysis available in the generated research log.")
    except KeyboardInterrupt:
        print("\n\nSaving partial experimental results...")
        agent.save_conversation_to_markdown()
        print("\nExperiment interrupted. Partial analysis available in the generated research log.")

if __name__ == "__main__":
    main()