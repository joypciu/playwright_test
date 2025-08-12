from jira import JIRA
import pytest
import os
from functools import wraps
import time
import datetime
import sys

def log_message(message, level="INFO"):
    """Custom logging that always shows output"""
    prefix = {
        "INFO": "ℹ️ ",
        "SUCCESS": "✅",
        "ERROR": "❌",
        "WARNING": "⚠️ ",
        "DEBUG": "🔍"
    }.get(level, "• ")
    
    # Print to stdout and flush immediately
    print(f"{prefix} {message}", flush=True)
    sys.stdout.flush()

def test_jira_connection():
    """Test the Jira connection before running tests"""
    log_message("="*80, "INFO")
    log_message("STARTING JIRA CONNECTION TEST", "INFO")
    log_message("="*80, "INFO")
    
    try:
        log_message("Step 1: Initializing Jira client...", "INFO")
        jira = get_jira_client()
        log_message("Step 1: Jira client initialized successfully", "SUCCESS")
        
        log_message("Step 2: Testing server info...", "INFO")
        try:
            server_info = jira.server_info()
            log_message("Step 2: Connected to Jira server", "SUCCESS")
            log_message(f"   - Server Version: {server_info.get('version', 'Unknown')}", "INFO")
            log_message(f"   - Build Number: {server_info.get('buildNumber', 'Unknown')}", "INFO")
        except Exception as e:
            log_message(f"Step 2: Could not get server info: {str(e)}", "WARNING")
        
        log_message("Step 3: Testing project access...", "INFO")
        try:
            project = jira.project("KAN")
            log_message("Step 3: Found project KAN", "SUCCESS")
            log_message(f"   - Project Name: {project.name}", "INFO")
            log_message(f"   - Project Key: {project.key}", "INFO")
            log_message(f"   - Project Lead: {getattr(project, 'lead', 'Unknown')}", "INFO")
        except Exception as e:
            log_message(f"Step 3: Could not access project KAN: {str(e)}", "ERROR")
            log_message("   Trying to list all available projects...", "INFO")
            try:
                projects = jira.projects()
                log_message(f"   Found {len(projects)} projects:", "INFO")
                for proj in projects[:10]:  # Show first 10
                    log_message(f"     - {proj.key}: {proj.name}", "INFO")
            except Exception as pe:
                log_message(f"   Could not list projects: {str(pe)}", "ERROR")
        
        log_message("Step 4: Testing issue access...", "INFO")
        issues_found = []
        issue_ids = ["KAN-1", "KAN-2", "KAN-3"]
        
        for i, issue_id in enumerate(issue_ids, 1):
            log_message(f"   4.{i}: Checking {issue_id}...", "INFO")
            
            # Method 1: Direct access
            try:
                log_message(f"      Method 1 - Direct access: jira.issue('{issue_id}')", "DEBUG")
                issue = jira.issue(issue_id)
                log_message(f"      SUCCESS: Found {issue_id}", "SUCCESS")
                log_message(f"         - Summary: {issue.fields.summary}", "INFO")
                log_message(f"         - Status: {issue.fields.status.name}", "INFO")
                log_message(f"         - Reporter: {issue.fields.reporter.displayName}", "INFO")
                log_message(f"         - Created: {issue.fields.created}", "INFO")
                issues_found.append(issue)
                continue
            except Exception as e:
                log_message(f"      Method 1 failed: {str(e)}", "ERROR")
                
            # Method 2: Search
            try:
                log_message(f"      Method 2 - JQL search: 'key = {issue_id}'", "DEBUG")
                search_results = jira.search_issues(f'key = {issue_id}')
                if search_results:
                    issue = search_results[0]
                    log_message(f"      SUCCESS: Found {issue_id} via search", "SUCCESS")
                    log_message(f"         - Summary: {issue.fields.summary}", "INFO")
                    log_message(f"         - Status: {issue.fields.status.name}", "INFO")
                    issues_found.append(issue)
                    continue
                else:
                    log_message(f"      Method 2: No search results for {issue_id}", "ERROR")
            except Exception as se:
                log_message(f"      Method 2 failed: {str(se)}", "ERROR")
        
        log_message("Step 5: Listing all issues in KAN project...", "INFO")
        try:
            all_issues = jira.search_issues('project = KAN ORDER BY key ASC', maxResults=50)
            log_message(f"Step 5: Found {len(all_issues)} total issues in KAN project:", "SUCCESS")
            for issue in all_issues:
                log_message(f"   - {issue.key}: {issue.fields.summary} [{issue.fields.status.name}]", "INFO")
        except Exception as e:
            log_message(f"Step 5: Could not list KAN project issues: {str(e)}", "ERROR")
            
        log_message("Step 6: Testing comment functionality...", "INFO")
        if issues_found:
            test_issue = issues_found[0]
            try:
                log_message(f"Testing comment on {test_issue.key}...", "INFO")
                test_comment = f"🧪 Test comment from pytest - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                jira.add_comment(test_issue, test_comment)
                log_message(f"Step 6: Successfully added test comment to {test_issue.key}", "SUCCESS")
            except Exception as e:
                log_message(f"Step 6: Could not add comment: {str(e)}", "ERROR")
        else:
            log_message("Step 6: Skipped - no issues available for testing", "WARNING")
            
        log_message("="*80, "INFO")
        log_message("📊 JIRA CONNECTION TEST RESULTS:", "INFO")
        log_message(f"   - Issues found: {len(issues_found)}", "INFO")
        log_message(f"   - Expected issues: {len(issue_ids)}", "INFO")
        if len(issues_found) > 0:
            log_message("JIRA INTEGRATION: WORKING", "SUCCESS")
        else:
            log_message("JIRA INTEGRATION: PARTIAL (no test issues found)", "WARNING")
        log_message("="*80, "INFO")
        
        return True
        
    except Exception as e:
        log_message("="*80, "INFO")
        log_message(f"JIRA CONNECTION TEST FAILED: {str(e)}", "ERROR")
        log_message("="*80, "INFO")
        raise

def get_jira_client():
    """Initialize and return Jira client"""
    log_message("🔧 INITIALIZING JIRA CLIENT:", "INFO")
    
    username = os.getenv("JIRA_USERNAME")
    token = os.getenv("JIRA_TOKEN")
    
    log_message("   - Checking environment variables...", "INFO")
    if not username:
        log_message("   JIRA_USERNAME environment variable is not set", "ERROR")
        raise ValueError("JIRA_USERNAME environment variable must be set")
    else:
        log_message(f"   JIRA_USERNAME: {username}", "SUCCESS")
    
    if not token:
        log_message("   JIRA_TOKEN environment variable is not set", "ERROR")
        raise ValueError("JIRA_TOKEN environment variable must be set")
    else:
        log_message(f"   JIRA_TOKEN: {'*' * (len(token)-4) + token[-4:]} (masked)", "SUCCESS")
    
    server_url = "https://usmanjoy.atlassian.net"
    log_message(f"   - Connecting to: {server_url}", "INFO")
    
    try:
        jira_client = JIRA(
            server=server_url,
            basic_auth=(username, token)
        )
        log_message("   JIRA client created successfully", "SUCCESS")
        return jira_client
    except Exception as e:
        log_message(f"   Failed to create JIRA client: {str(e)}", "ERROR")
        raise

def jira_issue(issue_id, summary=None):
    """Decorator to link test with Jira issue"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log_message("="*60, "INFO")
            log_message("🚀 JIRA INTEGRATION START", "INFO")
            log_message("="*60, "INFO")
            log_message(f"Target Issue: {issue_id}", "INFO")
            log_message(f"Test Function: {func.__name__}", "INFO")
            if summary:
                log_message(f"Description: {summary}", "INFO")
            
            start_time = time.time()
            
            try:
                log_message(f"▶️  Executing test: {func.__name__}", "INFO")
                result = func(*args, **kwargs)
                
                execution_time = time.time() - start_time
                status = "Pass"
                log_message(f"Test PASSED in {execution_time:.2f} seconds", "SUCCESS")
                
                log_message(f"📝 Updating Jira issue {issue_id}...", "INFO")
                try:
                    update_jira_status(issue_id, status, None, execution_time)
                    log_message(f"Successfully updated Jira issue {issue_id}", "SUCCESS")
                except Exception as jira_error:
                    log_message(f"Could not update Jira issue {issue_id}: {str(jira_error)}", "WARNING")
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                error_details = f"""
Error Type: {type(e).__name__}
Error Message: {str(e)}
Test Duration: {execution_time:.2f} seconds
"""
                status = "Fail"
                log_message(f"Test FAILED in {execution_time:.2f} seconds", "ERROR")
                log_message(f"Error: {str(e)}", "ERROR")
                
                log_message(f"📝 Updating Jira issue {issue_id} with failure...", "INFO")
                try:
                    update_jira_status(issue_id, status, error_details, execution_time)
                    log_message(f"Successfully updated Jira issue {issue_id} with failure", "SUCCESS")
                except Exception as jira_error:
                    log_message(f"Could not update Jira issue {issue_id}: {str(jira_error)}", "WARNING")
                
                raise
            finally:
                log_message("="*60, "INFO")
                log_message("🏁 JIRA INTEGRATION END", "INFO")
                log_message("="*60, "INFO")
            
        return wrapper
    return decorator

def update_jira_status(issue_id, status, error_message=None, execution_time=0):
    """Update Jira issue with test result"""
    log_message(f"📋 UPDATING JIRA ISSUE {issue_id}:", "INFO")
    
    try:
        log_message("   Step 1: Getting Jira client...", "INFO")
        jira = get_jira_client()
        log_message("   Step 1: Got Jira client", "SUCCESS")
        
        log_message(f"   Step 2: Finding issue {issue_id}...", "INFO")
        issue = None
        
        # Try direct access first
        try:
            issue = jira.issue(issue_id)
            log_message("   Step 2: Found issue via direct access", "SUCCESS")
        except Exception as direct_error:
            log_message(f"   Direct access failed: {str(direct_error)}", "WARNING")
            
            # Try search
            try:
                log_message("   Step 2b: Trying search method...", "INFO")
                search_results = jira.search_issues(f'key = {issue_id}')
                if search_results:
                    issue = search_results[0]
                    log_message("   Step 2b: Found issue via search", "SUCCESS")
                else:
                    raise Exception(f"Issue {issue_id} not found via search")
            except Exception as search_error:
                log_message(f"   Step 2b: Search failed: {str(search_error)}", "ERROR")
                raise Exception(f"Could not find issue {issue_id}")
        
        log_message("   Step 3: Creating comment...", "INFO")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment = f"""🤖 Automated Test Report
------------------------
📅 Date: {timestamp}
📊 Status: {'✅ PASS' if status == 'Pass' else '❌ FAIL'}
⏱️ Execution Time: {execution_time:.2f} seconds
🔍 Test Run Details:
- Test ID: {issue_id}
- Environment: Python Playwright Tests
- Test Framework: pytest
- Machine: {os.getenv('COMPUTERNAME', 'Unknown')}
"""
        if error_message:
            comment += f"\n❌ Error Details:\n{error_message}"
        
        log_message("   Step 4: Adding comment to issue...", "INFO")
        jira.add_comment(issue, comment)
        log_message("   Step 4: Comment added successfully", "SUCCESS")
        
        log_message(f"Successfully updated Jira issue {issue_id} with status: {status}", "SUCCESS")
        
    except Exception as e:
        log_message(f"Failed to update Jira issue {issue_id}: {str(e)}", "ERROR")
        log_message(f"   Full error: {type(e).__name__}: {str(e)}", "ERROR")
        raise