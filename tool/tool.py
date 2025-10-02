#!/usr/bin/env python3

import requests
import json
import argparse
from collections import Counter
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_load_balancer(url, num_requests):
    hostnames = []
    
    print(f"Sending {num_requests} requests to {url}...")
    
    for i in range(num_requests):
        try:
            response = requests.get(f"{url}/api/ping", verify=False, timeout=10)
            if response.status_code == 200:
                data = response.json()
                hostname = data.get('hostname', 'unknown')
                hostnames.append(hostname)
            else:
                print(f"  Request {i + 1} failed with status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"  Request {i + 1} failed: {str(e)}")
    
    hostname_counts = Counter(hostnames)
    unique_nodes = list(hostname_counts.keys())
    
    return {
        "total_requests": num_requests,
        "unique_nodes": unique_nodes,
        "node_request_counts": dict(hostname_counts),
        "available_nodes_count": len(unique_nodes)
    }

def print_results(results):
    """Print formatted results"""
    print("\n" + "="*60)
    print("LOAD BALANCER TEST RESULTS")
    print("="*60)

    print(f"\nNode Hostnames:")
    for i, hostname in enumerate(results['unique_nodes'], 1):
        print(f"  {i}. {hostname}")

    print(f"\nAvailable Nodes Count: \n  {results['available_nodes_count']}")
    
    print(f"\nRequests Handled by Each Node:")
    total_handled = sum(results['node_request_counts'].values())
    for hostname, count in results['node_request_counts'].items():
        percentage = (count / total_handled * 100) if total_handled > 0 else 0
        print(f"  {hostname}: {count} requests ({percentage:.1f}%)")

def main():
    parser = argparse.ArgumentParser(description='Test load balancer')
    parser.add_argument('--url', '-u', 
                       default='https://localhost:5000',
                       help='Load balancer URL (default: https://localhost:5000)')
    parser.add_argument('--requests', '-r', 
                       type=int, default=50,
                       help='Number of requests to send (default: 50)')
    args = parser.parse_args()
    
    results = test_load_balancer(args.url, args.requests)
    
    print_results(results)

if __name__ == "__main__":
    main()
