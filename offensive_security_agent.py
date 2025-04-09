import os
import anthropic
import subprocess
import ipaddress
import json
import socket
import time
import sys
import argparse
from dotenv import load_dotenv
from anthropic import APIError
from datetime import datetime
from gemini_prompt_generator import GeminiPromptGenerator

class OffensiveSecurityAgent:
    def __init__(self, demo_mode=False):
        """
        Initialize the OffensiveSecurityAgent with components for recon, scanning, and verification.
        
        Args:
            demo_mode (bool): If True, use simulated data instead of actual scanning
        """
        load_dotenv()
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.gemini = GeminiPromptGenerator()
        self.targets = []
        self.scan_results = {}
        self.verified_vulnerabilities = []
        self.technical_reports = {}
        self.demo_mode = demo_mode
        
        # System prompt for Claude as a technical verification specialist
        self.claude_system_prompt = """You are Claude, an elite offensive security specialist focused on technical verification and exploitation of potential vulnerabilities. Your role is to analyze scan results and determine if flagged issues are actual vulnerabilities or false positives.

For each potential vulnerability, you will:
1. Analyze the technical details provided by reconnaissance
2. Determine if the finding represents a genuine security issue
3. If valid, create a proof-of-concept exploitation script or command sequence
4. Verify the vulnerability through specific technical checks
5. Provide detailed remediation steps for confirmed issues

Your verification approach:
- Examine port scan data, service versions, and system information
- Review potential security misconfigurations
- Check for known CVEs that affect identified software versions
- Consider the technical context and architecture
- Provide technically precise verification methods

IMPORTANT: For verified vulnerabilities, you MUST use the following sections:
[VULNERABILITY]: The verified security issue
[VERIFICATION]: Technical explanation of how you verified this is a real vulnerability
[EXPLOITATION]: Specific commands or code that demonstrate exploitability
[IMPACT]: Technical consequences of successful exploitation
[REMEDIATION]: Specific technical steps to fix the issue

Each section should be clearly labeled with the bracket format above."""

    def run_scan_only(self, target=None):
        """Run only the reconnaissance part of the assessment and save results to a file"""
        try:
            # Get target if not provided
            if not target:
                target = input("Enter target IP address or CIDR range (e.g., '192.168.1.1' or '192.168.1.0/24'): ")
                if not target or target.strip() == "":
                    print("\n⚠️ ERROR: A valid target IP or network range is required.")
                    return False
            
            # Validate the target is a valid IP or CIDR
            try:
                if '/' in target:
                    # This is a CIDR range
                    ipaddress.ip_network(target)
                    print(f"\n=== Initiating scan for network range: {target} ===")
                else:
                    # This is a single IP
                    ipaddress.ip_address(target)
                    print(f"\n=== Initiating scan for IP: {target} ===")
                
                self.targets.append(target)
            except ValueError:
                print(f"\n⚠️ ERROR: '{target}' is not a valid IP address or CIDR range.")
                return False
            
            # Perform initial reconnaissance with Nmap
            print("\n[STEP 1] Performing initial reconnaissance...")
            recon_results = self._perform_reconnaissance(target)
            
            if not recon_results:
                print("No open ports or services found. Scan complete.")
                return False
            
            # Save scan results to file
            self._save_scan_results(target, recon_results)
            
            print(f"\nScan completed successfully and results saved.")
            return True
            
        except Exception as e:
            print(f"\nError during scanning: {str(e)}")
            return False
    
    def run_analyze_only(self, scan_file=None):
        """Run only the analysis part of the assessment using scan results from a file"""
        try:
            # Get scan file if not provided
            if not scan_file:
                scan_file = input("Enter the path to the scan results file: ")
                if not scan_file or scan_file.strip() == "":
                    print("\n⚠️ ERROR: A valid scan file path is required.")
                    return False
            
            # Load scan results from file
            recon_results, target = self._load_scan_results(scan_file)
            if not recon_results or not target:
                print(f"\n⚠️ ERROR: Could not load valid scan results from {scan_file}")
                return False
            
            self.targets.append(target)
            self.scan_results[target] = recon_results
            
            print(f"\n=== Initiating analysis for: {target} ===")
            
            # Process reconnaissance data with Gemini
            print("\n[STEP 1] Analyzing reconnaissance data...")
            analysis_prompt = self.gemini.generate_recon_analysis_prompt(recon_results, target)
            print("\n[RECONNAISSANCE ANALYSIS PROMPT]")
            print("Gemini: ", analysis_prompt[:300] + "..." if len(analysis_prompt) > 300 else analysis_prompt)
            
            # Let Claude verify findings and identify actual vulnerabilities
            print("\n[STEP 2] Verifying potential vulnerabilities...")
            verification_results = self._verify_vulnerabilities(analysis_prompt, recon_results)
            
            if not self.verified_vulnerabilities:
                print("No verified vulnerabilities found. Analysis complete.")
                return True
            
            # Generate exploitation code for verified vulnerabilities
            print("\n[STEP 3] Generating technical exploitation code...")
            for vuln in self.verified_vulnerabilities:
                self._generate_exploitation_code(vuln, target)
            
            # Generate comprehensive security report
            print("\n[STEP 4] Creating technical security report...")
            report = self._generate_technical_report(target)
            
            # Save the security assessment to a file
            self._save_technical_report(target, report)
            
            return True
            
        except Exception as e:
            print(f"\nError during analysis: {str(e)}")
            return False

    def start_security_assessment(self, target=None):
        """Start a complete offensive security assessment on a target IP or network range"""
        try:
            # Get target if not provided
            if not target:
                target = input("Enter target IP address or CIDR range (e.g., '192.168.1.1' or '192.168.1.0/24'): ")
                if not target or target.strip() == "":
                    print("\n⚠️ ERROR: A valid target IP or network range is required.")
                    return False
            
            # Validate the target is a valid IP or CIDR
            try:
                if '/' in target:
                    # This is a CIDR range
                    ipaddress.ip_network(target)
                    print(f"\n=== Initiating assessment for network range: {target} ===")
                else:
                    # This is a single IP
                    ipaddress.ip_address(target)
                    print(f"\n=== Initiating assessment for IP: {target} ===")
                
                self.targets.append(target)
            except ValueError:
                print(f"\n⚠️ ERROR: '{target}' is not a valid IP address or CIDR range.")
                return False
            
            # 1. Perform initial reconnaissance with Nmap
            print("\n[STEP 1] Performing initial reconnaissance...")
            recon_results = self._perform_reconnaissance(target)
            
            if not recon_results:
                print("No open ports or services found. Assessment complete.")
                return True
            
            # 2. Process reconnaissance data with Gemini
            print("\n[STEP 2] Analyzing reconnaissance data...")
            analysis_prompt = self.gemini.generate_recon_analysis_prompt(recon_results, target)
            print("\n[RECONNAISSANCE ANALYSIS PROMPT]")
            print("Gemini: ", analysis_prompt[:300] + "..." if len(analysis_prompt) > 300 else analysis_prompt)
            
            # 3. Let Claude verify findings and identify actual vulnerabilities
            print("\n[STEP 3] Verifying potential vulnerabilities...")
            verification_results = self._verify_vulnerabilities(analysis_prompt, recon_results)
            
            if not self.verified_vulnerabilities:
                print("No verified vulnerabilities found. Assessment complete.")
                return True
            
            # 4. Generate exploitation code for verified vulnerabilities
            print("\n[STEP 4] Generating technical exploitation code...")
            for vuln in self.verified_vulnerabilities:
                self._generate_exploitation_code(vuln, target)
            
            # 5. Generate comprehensive security report
            print("\n[STEP 5] Creating technical security report...")
            report = self._generate_technical_report(target)
            
            # 6. Save the security assessment to a file
            self._save_technical_report(target, report)
            
            return True
            
        except Exception as e:
            print(f"\nError during security assessment: {str(e)}")
            return False
    
    def _save_scan_results(self, target, scan_results):
        """Save scan results to a JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scan_results_{timestamp}.json"
        
        with open(filename, "w") as f:
            json.dump({
                "target": target,
                "timestamp": timestamp,
                "scan_results": scan_results
            }, f, indent=2)
        
        print(f"\nScan results saved to: {filename}")
        return filename

    def _load_scan_results(self, filename):
        """Load scan results from a JSON file"""
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            
            target = data.get("target")
            scan_results = data.get("scan_results")
            
            print(f"Loaded scan results for {target}")
            return scan_results, target
        except Exception as e:
            print(f"Error loading scan results: {str(e)}")
            return None, None
    
    def _perform_reconnaissance(self, target):
        """Run initial reconnaissance on the target"""
        results = {}
        
        # If in demo mode, use simulated data
        if self.demo_mode:
            print(f"[DEMO MODE] Simulating Nmap scan on {target}...")
            time.sleep(2)  # Simulate scan time
            
            results["nmap"] = f"""
Nmap scan report for {target}
Host is up (0.015s latency).
Not shown: 992 closed ports
PORT     STATE SERVICE       VERSION
22/tcp   open  ssh           OpenSSH 8.9p1 (protocol 2.0)
80/tcp   open  http          Apache httpd 2.4.52
443/tcp  open  https         Apache httpd 2.4.52
3306/tcp open  mysql         MySQL 8.0.28
8080/tcp open  http-proxy    Apache Tomcat 9.0.52
8443/tcp open  https-alt     Apache Tomcat 9.0.52
"""
            print(f"[DEMO MODE] Reconnaissance simulation completed.")
            
            # Store the scan results
            self.scan_results[target] = results
            return results
            
        # Otherwise perform actual reconnaissance
        try:
            # Run basic Nmap scan
            print(f"Running Nmap scan on {target}...")
            
            # Actually execute Nmap
            try:
                import nmap
                scanner = nmap.PortScanner()
                
                print("Starting Nmap scan - this may take some time...")
                scan_arguments = "-sV -T4"  # Service version detection - removed OS detection as it requires root
                scanner.scan(hosts=target, arguments=scan_arguments)
                
                # Build detailed nmap output
                nmap_output = f"Nmap scan report for {target}\n"
                
                for host in scanner.all_hosts():
                    host_status = scanner[host].state()
                    nmap_output += f"Host: {host} ({scanner[host].hostname()})\tStatus: {host_status}\n"
                    
                    if host_status == 'up':
                        for proto in scanner[host].all_protocols():
                            nmap_output += f"Protocol: {proto}\n"
                            
                            ports = sorted(scanner[host][proto].keys())
                            for port in ports:
                                service = scanner[host][proto][port]
                                service_name = service['name']
                                service_product = service.get('product', '')
                                service_version = service.get('version', '')
                                service_extra = service.get('extrainfo', '')
                                
                                service_details = f"{service_name}"
                                if service_product:
                                    service_details += f" {service_product}"
                                if service_version:
                                    service_details += f" {service_version}"
                                if service_extra:
                                    service_details += f" ({service_extra})"
                                
                                nmap_output += f"Port: {port}/{proto}\tState: {service['state']}\tService: {service_details}\n"
                                
                # Store the nmap output
                results["nmap"] = nmap_output
                
                # If no hosts/ports found, check if we can perform a basic ping scan to verify host is up
                if not scanner.all_hosts():
                    print("No hosts found, performing ping scan...")
                    ping_scan = scanner.scan(hosts=target, arguments="-sn")
                    results["nmap"] = f"Ping scan for {target}: No open ports detected or host is down/blocking scans."
                    
            except ImportError:
                # Fallback to subprocess if python-nmap is not available
                print("Python-nmap not found, using subprocess to run nmap...")
                try:
                    import subprocess
                    
                    # Check if nmap is installed
                    try:
                        version_check = subprocess.run(["nmap", "--version"], capture_output=True, text=True)
                        # If we get here, nmap is installed
                    except FileNotFoundError:
                        raise Exception("Nmap is not installed or not in PATH. Please install Nmap to use this tool.")
                    
                    # Run the actual nmap scan - removed -O flag to avoid needing root
                    nmap_cmd = ["nmap", "-sV", "-T4", target]
                    nmap_result = subprocess.run(nmap_cmd, capture_output=True, text=True)
                    
                    if nmap_result.returncode != 0:
                        print(f"Nmap scan error: {nmap_result.stderr}")
                        raise Exception("Nmap scan failed.")
                    
                    results["nmap"] = nmap_result.stdout
                except Exception as e:
                    print(f"Error running nmap via subprocess: {str(e)}")
                    # Fall back to ping 
                    ping_cmd = ["ping", "-c", "4", target.split('/')[0]]  # Remove CIDR if present
                    ping_result = subprocess.run(ping_cmd, capture_output=True, text=True)
                    results["ping"] = ping_result.stdout
            
            # Add additional reconnaissance tools here
            # For example: gobuster, nikto, wpscan, etc.
            
            # Only continue if we have actual results
            if not results or all(not output for output in results.values()):
                print(f"No reconnaissance data could be gathered for {target}.")
                return None
            
            # Store the scan results
            self.scan_results[target] = results
            
            print(f"Reconnaissance completed successfully.")
            return results
            
        except Exception as e:
            print(f"Error during reconnaissance: {str(e)}")
            return None
    
    def _verify_vulnerabilities(self, analysis_prompt, recon_data):
        """Use Claude to verify if potential vulnerabilities are real or false positives"""
        try:
            # Combine the analysis prompt with the raw recon data for Claude's verification
            verification_prompt = f"""
Please analyze this reconnaissance data and verify which potential security issues are actual vulnerabilities:

TARGET INFORMATION:
{json.dumps(self.targets, indent=2)}

RECONNAISSANCE DATA:
{json.dumps(recon_data, indent=2)}

POTENTIAL VULNERABILITIES (identified by Gemini):
{analysis_prompt}

For each potential security issue:
1. Verify if this is a genuine vulnerability or a false positive
2. Provide technical verification steps that would confirm the issue
3. If confirmed, explain how it could be exploited
4. Detail the potential impact
5. Provide specific remediation steps

Focus on technical accuracy and practicality. Only report verified vulnerabilities, not theoretical ones.
"""
            
            # Get Claude's verification response
            claude_response = self._get_claude_response(verification_prompt)
            print("\n[VULNERABILITY VERIFICATION]")
            print("Claude: ", claude_response[:500] + "..." if len(claude_response) > 500 else claude_response)
            
            # Extract verified vulnerabilities
            self._extract_verified_vulnerabilities(claude_response)
            
            print(f"\n[VERIFIED {len(self.verified_vulnerabilities)} ACTUAL VULNERABILITIES]")
            for i, vuln in enumerate(self.verified_vulnerabilities, 1):
                print(f"{i}. {vuln.get('title', 'Unnamed vulnerability')}")
            
            return self.verified_vulnerabilities
            
        except Exception as e:
            print(f"Error during vulnerability verification: {str(e)}")
            return []
    
    def _get_claude_response(self, prompt):
        """Get a response from Claude"""
        claude_response = self.client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=4096,
            system=self.claude_system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return claude_response.content[0].text
    
    def _extract_verified_vulnerabilities(self, message):
        """Extract verified vulnerabilities from Claude's response"""
        vuln_sections = message.split("[VULNERABILITY]:")
        
        # Skip the first element as it's before any vulnerability marker
        for i, section in enumerate(vuln_sections[1:], 1):
            # Extract vulnerability details
            vulnerability = {"id": f"VULN-{i:03d}"}
            
            # Extract the title/name of the vulnerability
            title_end = section.find("\n", 0)
            if title_end > 0:
                vulnerability["title"] = section[:title_end].strip()
            
            # Extract verification
            if "[VERIFICATION]:" in section:
                verification = section.split("[VERIFICATION]:")[1].split("[")[0].strip()
                vulnerability["verification"] = verification
            
            # Extract exploitation
            if "[EXPLOITATION]:" in section:
                exploitation = section.split("[EXPLOITATION]:")[1].split("[")[0].strip()
                vulnerability["exploitation"] = exploitation
            
            # Extract impact
            if "[IMPACT]:" in section:
                impact = section.split("[IMPACT]:")[1].split("[")[0].strip()
                vulnerability["impact"] = impact
            
            # Extract remediation
            if "[REMEDIATION]:" in section:
                remediation = section.split("[REMEDIATION]:")[1].split("[")[0].strip()
                vulnerability["remediation"] = remediation
            
            self.verified_vulnerabilities.append(vulnerability)
    
    def _generate_exploitation_code(self, vulnerability, target):
        """Generate detailed technical exploitation code for a verified vulnerability"""
        try:
            exploitation_prompt = f"""
For this verified vulnerability:
{json.dumps(vulnerability, indent=2)}

On target: {target}

Generate detailed technical exploitation code or command sequence that could be used to:
1. Verify the vulnerability exists
2. Exploit the vulnerability to demonstrate impact
3. Establish what level of access this provides

The code should be technically accurate and executable by a penetration tester. Include comments explaining each step.
"""
            
            exploitation_response = self._get_claude_response(exploitation_prompt)
            vulnerability["technical_exploit"] = exploitation_response
            print(f"Generated technical exploit for {vulnerability.get('title', 'vulnerability')}")
            
        except Exception as e:
            print(f"Error generating exploitation code: {str(e)}")
    
    def _generate_technical_report(self, target):
        """Generate a comprehensive technical security report"""
        print("\n=== Generating Technical Security Report ===")
        
        # Prepare report sections
        report = {
            "target": target,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "recon_data": self.scan_results.get(target, {}),
            "verified_vulnerabilities": self.verified_vulnerabilities,
            "executive_summary": "",
            "technical_summary": ""
        }
        
        # Generate executive summary
        summary_prompt = f"""
Create a concise executive summary of the security assessment results for {target}.
Focus on:
1. Overview of what was scanned
2. Number of verified vulnerabilities by severity
3. Most critical technical issues identified
4. High-level business impact
5. Key remediation priorities

This should be suitable for executive leadership but technically accurate.
"""
        
        try:
            summary_response = self._get_claude_response(summary_prompt)
            report["executive_summary"] = summary_response
            print("Generated executive summary")
            
            # Generate technical summary
            tech_summary_prompt = f"""
Create a detailed technical summary of the security assessment for {target}.
Include:
1. Technical environment details identified during reconnaissance
2. Summary of testing methodology and tools
3. Verified vulnerabilities with technical context
4. Exploitation potential and attack paths
5. Specific remediation approaches with technical implementation details

This should be suitable for security engineers and system administrators responsible for remediation.
"""
            
            tech_response = self._get_claude_response(tech_summary_prompt)
            report["technical_summary"] = tech_response
            print("Generated technical summary")
            
            return report
            
        except Exception as e:
            print(f"Error generating technical report: {str(e)}")
            report["executive_summary"] = "Error generating executive summary"
            report["technical_summary"] = "Error generating technical summary"
            return report
    
    def _save_technical_report(self, target, report):
        """Save the technical security report to a markdown file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"security_assessment_{timestamp}.md"
        
        with open(filename, "w") as f:
            f.write(f"# Technical Security Assessment: {target}\n\n")
            
            f.write("## Executive Summary\n\n")
            f.write(f"{report['executive_summary']}\n\n")
            
            f.write("## Technical Summary\n\n")
            f.write(f"{report['technical_summary']}\n\n")
            
            f.write("## Reconnaissance Data\n\n")
            f.write("```\n")
            for tool, output in report["recon_data"].items():
                f.write(f"=== {tool.upper()} SCAN ===\n")
                f.write(f"{output}\n\n")
            f.write("```\n\n")
            
            f.write("## Verified Vulnerabilities\n\n")
            for vuln in report["verified_vulnerabilities"]:
                f.write(f"### {vuln.get('title', 'Unnamed Vulnerability')}\n\n")
                
                if "verification" in vuln:
                    f.write(f"**Verification:** {vuln['verification']}\n\n")
                
                if "exploitation" in vuln:
                    f.write(f"**Exploitation:** {vuln['exploitation']}\n\n")
                
                if "impact" in vuln:
                    f.write(f"**Impact:** {vuln['impact']}\n\n")
                
                if "remediation" in vuln:
                    f.write(f"**Remediation:** {vuln['remediation']}\n\n")
                
                if "technical_exploit" in vuln:
                    f.write(f"**Technical Exploitation Code:**\n\n```\n{vuln['technical_exploit']}\n```\n\n")
                
                f.write("---\n\n")
        
        print(f"\nTechnical security assessment saved to: {filename}")

def check_nmap_installed():
    """Check if Nmap is installed and available in the PATH"""
    try:
        import subprocess
        result = subprocess.run(["nmap", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except (FileNotFoundError, PermissionError):
        return False

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Technical Offensive Security Assessment Tool")
    parser.add_argument("--scan-only", action="store_true", help="Run only the scanning phase and save results to a file")
    parser.add_argument("--analyze-only", action="store_true", help="Run only the analysis phase using scan results from a file")
    parser.add_argument("--scan-file", type=str, help="Path to scan results file (for analyze-only mode)")
    parser.add_argument("--target", type=str, help="Target IP address or CIDR range")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode with simulated data")
    args = parser.parse_args()

    print("\n===== Technical Offensive Security Assessment Tool =====")
    print("This tool performs reconnaissance, vulnerability identification, and technical verification")
    print("on real systems using a combination of scanning tools and AI analysis.\n")
    
    # Determine operation mode
    if args.scan_only and args.analyze_only:
        print("Error: Cannot use both --scan-only and --analyze-only flags together.")
        return
    
    # Check for demo mode
    demo_mode = False
    if args.demo:
        demo_mode = True
        print("[DEMO MODE ENABLED] The tool will use simulated scan data instead of running actual scans.")
    else:
        # Check if Nmap is installed when not in demo mode
        nmap_installed = check_nmap_installed()
        if not nmap_installed and not args.analyze_only:
            print("\n⚠️ Nmap not found! The tool requires Nmap for actual scanning.")
            print("You can either:")
            print("1. Install Nmap (https://nmap.org/download.html)")
            print("2. Continue in demo mode with simulated data\n")
            demo_choice = input("Continue in demo mode? (y/n): ").lower()
            if not demo_choice.startswith('y'):
                print("Exiting. Please install Nmap to use this tool in normal mode.")
                return
            demo_mode = True
            print("[DEMO MODE ENABLED] The tool will use simulated scan data instead of running actual scans.")
    
    # Initialize agent
    agent = OffensiveSecurityAgent(demo_mode=demo_mode)
    
    # Handle scan-only mode
    if args.scan_only:
        target = args.target
        if not target:
            target = input("Enter target IP address or CIDR range (e.g., '192.168.1.1' or '192.168.1.0/24'): ")
        
        if not target or target.strip() == "":
            print("\n⚠️ ERROR: A valid target IP or network range is required.")
            return
        
        print(f"\nRunning scan-only mode on target: {target}")
        agent.run_scan_only(target)
    
    # Handle analyze-only mode
    elif args.analyze_only:
        scan_file = args.scan_file
        if not scan_file:
            scan_file = input("Enter the path to the scan results file: ")
        
        if not scan_file or scan_file.strip() == "":
            print("\n⚠️ ERROR: A valid scan file path is required.")
            return
        
        print(f"\nRunning analyze-only mode using scan file: {scan_file}")
        agent.run_analyze_only(scan_file)
    
    # Handle full assessment mode
    else:
        target = args.target
        if not target:
            target = input("Enter target IP address or CIDR range (e.g., '192.168.1.1' or '192.168.1.0/24'): ")
        
        if not target or target.strip() == "":
            print("\n⚠️ ERROR: A valid target IP or network range is required.")
            return
        
        print(f"\nRunning full assessment on target: {target}")
        agent.start_security_assessment(target)

if __name__ == "__main__":
    main()
    