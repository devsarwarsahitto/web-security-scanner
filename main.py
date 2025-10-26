#!/usr/bin/env python3

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from datetime import datetime

import config
from utils.banner import (print_banner, print_info, print_success, 
                         print_error, print_warning)
from utils.logger import ScanLogger
from utils.network import NetworkUtils
from scanners.host_enumerator import HostEnumerator
from scanners.env_scanner import EnvScanner
from scanners.security_scanner import SecurityScanner

class SecurityScannerTool:
    def __init__(self, args):
        self.args = args
        self.targets = []
        self.logger = ScanLogger(args.output)
        self.host_enumerator = HostEnumerator(threads=args.threads)
        self.env_scanner = EnvScanner()
        self.security_scanner = SecurityScanner()
    
    def run(self):
        print_banner()
        
        self._gather_targets()
        
        if not self.targets:
            print_error("No targets found to scan. Please provide valid targets.")
            return
        
        print_info(f"Total targets to scan: {len(self.targets)}")
        print_info(f"Thread count: {self.args.threads}")
        print_info(f"Starting scan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print_warning("Please ensure you have authorization to scan these targets!")
        print("")
        
        self._scan_targets()
        
        self._generate_reports()
        
        self._print_summary()
    
    def _gather_targets(self):
        print_info("Gathering targets...")
        
        if self.args.ip_range:
            targets = self.host_enumerator.enumerate_ip_range(self.args.ip_range)
            self.targets.extend(targets)
        
        if self.args.asn:
            targets = self.host_enumerator.enumerate_asn(self.args.asn)
            self.targets.extend(targets)
        
        if self.args.domain:
            targets = self.host_enumerator.enumerate_domain(self.args.domain)
            self.targets.extend(targets)
        
        if self.args.target:
            target = NetworkUtils.normalize_url(self.args.target)
            self.targets.append(target)
        
        if self.args.file:
            targets = self.host_enumerator.load_from_file(self.args.file)
            self.targets.extend(targets)
        
        self.targets = list(set(self.targets))
        
        for target in self.targets:
            self.logger.add_target(target)
    
    def _scan_targets(self):
        print_info("Starting vulnerability scan...")
        
        with ThreadPoolExecutor(max_workers=self.args.threads) as executor:
            futures = {executor.submit(self._scan_single_target, target): target 
                      for target in self.targets}
            
            with tqdm(total=len(self.targets), desc="Scanning", 
                     unit="target", ncols=100) as pbar:
                for future in as_completed(futures):
                    pbar.update(1)
                    try:
                        future.result()
                    except Exception as e:
                        target = futures[future]
                        print_error(f"Error scanning {target}: {e}")
    
    def _scan_single_target(self, target):
        try:
            if self.args.env_only or self.args.all:
                env_results = self.env_scanner.scan_target(target)
                for vuln in env_results:
                    self.logger.add_vulnerability(vuln)
            
            if self.args.security_only or self.args.all:
                sec_results = self.security_scanner.scan_target(target)
                for vuln in sec_results:
                    self.logger.add_vulnerability(vuln)
            
            if not self.args.env_only and not self.args.security_only and not self.args.all:
                env_results = self.env_scanner.scan_target(target)
                sec_results = self.security_scanner.scan_target(target)
                
                for vuln in env_results + sec_results:
                    self.logger.add_vulnerability(vuln)
            
        except Exception as e:
            print_error(f"Error scanning {target}: {e}")
    
    def _generate_reports(self):
        print("")
        print_info("Generating reports...")
        
        json_file = self.logger.save_json_report()
        print_success(f"JSON report saved: {json_file}")
        
        text_file = self.logger.save_text_report()
        print_success(f"Text report saved: {text_file}")
    
    def _print_summary(self):
        print("")
        print_info("="*80)
        print_info("SCAN SUMMARY")
        print_info("="*80)
        
        stats = self.logger.get_statistics()
        
        print_success(f"Total Targets Scanned: {stats['total_targets']}")
        print_success(f"Vulnerable Targets: {stats['vulnerable_targets']}")
        print("")
        print_warning(f"Exposed .env Files: {stats['env_files_found']}")
        print_warning(f"Exposed Git Directories: {stats['git_exposed']}")
        print_warning(f"Backup Files Found: {stats['backup_files_found']}")
        print_warning(f"Admin Panels Found: {stats['admin_panels_found']}")
        print("")
        print_info(f"Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print_info("="*80)
        print("")
        print_success(f"Developed by {config.AUTHOR}")
        print_success(f"GitHub: {config.GITHUB}")
        print("")

def main():
    parser = argparse.ArgumentParser(
        description=f"Security Scanner v{config.VERSION} - Advanced Web Security Scanner by {config.AUTHOR}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  Scan a single target:
    python main.py -t example.com
  
  Scan IP range:
    python main.py -r 192.168.1.0/24
  
  Scan from file:
    python main.py -f targets.txt
  
  Scan domain with subdomain enumeration:
    python main.py -d example.com
  
  Only scan for .env files:
    python main.py -t example.com --env-only
  
  Full security scan with custom threads:
    python main.py -t example.com --all --threads 20

Author: {config.AUTHOR}
GitHub: {config.GITHUB}
        """
    )
    
    target_group = parser.add_argument_group('Target Options')
    target_group.add_argument('-t', '--target', help='Single target URL or IP')
    target_group.add_argument('-r', '--ip-range', help='IP range in CIDR notation (e.g., 192.168.1.0/24)')
    target_group.add_argument('-a', '--asn', help='Autonomous System Number (e.g., AS15169)')
    target_group.add_argument('-d', '--domain', help='Domain to enumerate and scan')
    target_group.add_argument('-f', '--file', help='File containing list of targets')
    
    scan_group = parser.add_argument_group('Scan Options')
    scan_group.add_argument('--env-only', action='store_true', 
                           help='Only scan for .env files')
    scan_group.add_argument('--security-only', action='store_true', 
                           help='Only run security checks (no .env scan)')
    scan_group.add_argument('--all', action='store_true', 
                           help='Run all scan types (default if no scan type specified)')
    
    config_group = parser.add_argument_group('Configuration Options')
    config_group.add_argument('--threads', type=int, default=config.DEFAULT_THREADS, 
                             help=f'Number of threads (default: {config.DEFAULT_THREADS})')
    config_group.add_argument('--timeout', type=int, default=config.DEFAULT_TIMEOUT, 
                             help=f'Request timeout in seconds (default: {config.DEFAULT_TIMEOUT})')
    config_group.add_argument('-o', '--output', 
                             default=datetime.now().strftime("scan_%Y%m%d_%H%M%S"),
                             help='Output filename prefix for reports')
    
    parser.add_argument('-v', '--version', action='version', 
                       version=f'Security Scanner v{config.VERSION} by {config.AUTHOR}')
    
    if len(sys.argv) == 1:
        print_banner()
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    
    if not any([args.target, args.ip_range, args.asn, args.domain, args.file]):
        print_error("Error: No target specified. Use -t, -r, -a, -d, or -f")
        parser.print_help()
        sys.exit(1)
    
    config.DEFAULT_TIMEOUT = args.timeout
    
    scanner = SecurityScannerTool(args)
    
    try:
        scanner.run()
    except KeyboardInterrupt:
        print("")
        print_warning("Scan interrupted by user")
        print_info("Saving partial results...")
        scanner._generate_reports()
        sys.exit(0)
    except Exception as e:
        print_error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
