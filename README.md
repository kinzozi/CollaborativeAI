<<<<<<< HEAD
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
=======
# Technical Offensive Security Assessment Tool

This project implements a sophisticated offensive security platform that performs real technical reconnaissance, vulnerability scanning, and verification of live systems. It leverages both Google's Gemini and Anthropic's Claude to create a comprehensive security assessment pipeline that identifies and verifies actual vulnerabilities.

## Key Features

- **Technical Reconnaissance**: Performs port scanning and service enumeration on target systems
- **AI-Enhanced Analysis**: Uses Gemini to analyze scan results and identify potential vulnerabilities
- **Technical Verification**: Claude verifies if findings are real vulnerabilities or false positives
- **Exploitation Code Generation**: Creates technical proof-of-concept code for verified vulnerabilities
- **Comprehensive Reporting**: Generates detailed technical reports with executive summaries

## How It Works

1. **Reconnaissance Phase**: The tool scans target IP addresses or networks to identify open ports, running services, and their versions
2. **Initial Analysis**: Gemini analyzes the reconnaissance data to identify potential security issues based on service versions and known vulnerabilities
3. **Technical Verification**: Claude reviews the findings to determine which issues are actual vulnerabilities versus false positives
4. **Exploitation Code Generation**: For verified vulnerabilities, Claude creates technical exploitation code to demonstrate the impact
5. **Comprehensive Reporting**: Detailed technical reports are generated with both executive and technical summaries

## Technical Components

### Reconnaissance Tools Used
- **Nmap**: For port scanning and service enumeration
- Additional tools can be easily integrated

### AI Components
- **Gemini**: Handles reconnaissance analysis and potential vulnerability identification
- **Claude**: Performs technical verification and creates exploitation code

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your API keys:
>>>>>>> c078e29 (Add Offensive Security Assessment Tool with AI capabilities)
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```
<<<<<<< HEAD

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
=======
4. Ensure you have Nmap installed on your system (for actual scanning functionality)

## Usage

### Standard Usage (All-in-One)
Run the security assessment tool from the terminal:
```
python offensive_security_agent.py
```

Enter the target IP address or CIDR range when prompted:
```
Enter target IP address or CIDR range (e.g., '192.168.1.1' or '192.168.1.0/24'):
```

### Command-Line Arguments
The tool supports various command-line arguments:

```
python offensive_security_agent.py --help
```

Options:
- `--scan-only`: Run only the scanning phase and save results to a file
- `--analyze-only`: Run only the analysis phase using scan results from a file
- `--scan-file PATH`: Path to scan results file (for analyze-only mode)
- `--target IP`: Target IP address or CIDR range
- `--demo`: Run in demo mode with simulated data

### Using Root/sudo for Scanning (Recommended)

For best results, run the scanning phase with sudo and the analysis phase as a normal user. We provide a helper script for this:

```
./scan_with_sudo.sh 192.168.1.1
```

This script will:
1. Run the scanning phase with sudo (for more comprehensive port scanning)
2. Save the scan results to a JSON file
3. Adjust permissions on the scan file
4. Run the analysis phase as your normal user (with proper API access)

### Demo Mode

If you don't have Nmap installed or don't want to perform actual scans, you can use demo mode:

```
python offensive_security_agent.py --demo
```

## Report Format

The generated security assessment includes:
- Executive Summary: High-level overview for leadership
- Technical Summary: Detailed findings for security teams
- Reconnaissance Data: Raw scan output for transparency
- Verified Vulnerabilities: Detailed explanations with:
  - Verification steps
  - Exploitation code
  - Impact analysis
  - Remediation recommendations

## Customization

The tool is designed to be modular, allowing easy extension with additional reconnaissance tools or custom scanning modules. Check the code documentation for extension points. 
>>>>>>> c078e29 (Add Offensive Security Assessment Tool with AI capabilities)
