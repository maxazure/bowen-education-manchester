#!/usr/bin/env python3
"""
Website DM (Director/Manager) Hook

This hook runs after each subagent completes in the /auto-website workflow.
It reads the TODOS.md file to determine workflow state and decides the next action.

Purpose: Enable autonomous website generation workflow by automatically
deciding what should happen next based on TODOS.md status and agent completion.

Workflow Phases:
1. Planning - website_planner creates all planning documents
2. Image Generation - DM calls Zhipu AI API to generate images
3. Development - website_developer creates database and templates
4. Testing - website_tester validates functionality
5. Debug & Fix - Loop until tests pass (max 5 iterations)
6. Completion - Final report
"""

import json
import sys
import re
from pathlib import Path


def read_todos_file():
    """Read the TODOS.md file to get workflow state."""
    todos_path = Path('.claude/workflow/TODOS.md')
    try:
        if not todos_path.exists():
            print(f"[Website DM] TODOS.md not found at {todos_path}", file=sys.stderr)
            return None

        with open(todos_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return content.lower()
    except Exception as e:
        print(f"[Website DM] Error reading TODOS.md: {e}", file=sys.stderr)
        return None


def parse_todos_status(todos_content):
    """Parse TODOS.md to extract current workflow state."""
    if not todos_content:
        return None

    status = {
        'phase1_complete': False,  # Planning
        'phase2_complete': False,  # Image Generation
        'phase3_complete': False,  # Development
        'phase4_complete': False,  # Testing
        'phase4_status': None,     # 'passed' or 'failed'
        'debug_iteration': 0
    }

    # Check phase completion status
    if 'phase 1: planning ✅ completed' in todos_content or 'phase 1: planning ✅ complete' in todos_content:
        status['phase1_complete'] = True

    if 'phase 2: image generation ✅ completed' in todos_content or 'phase 2: image generation ✅ complete' in todos_content:
        status['phase2_complete'] = True

    if 'phase 3: development' in todos_content and '✅ completed' in todos_content:
        status['phase3_complete'] = True

    # Check test results
    if 'phase 4: testing ✅ completed' in todos_content or 'phase 4: testing ✅ complete' in todos_content:
        status['phase4_complete'] = True
        status['phase4_status'] = 'passed'
    elif 'phase 4: testing ❌ failed' in todos_content:
        status['phase4_complete'] = True
        status['phase4_status'] = 'failed'

    # Count debug iterations (look for "iteration: N" or "iteration N" pattern)
    iteration_matches = re.findall(r'iteration[:\s]+(\d+)', todos_content)
    if iteration_matches:
        status['debug_iteration'] = max([int(n) for n in iteration_matches])

    return status


def read_recent_transcript(transcript_path, lines=200):
    """Read recent lines from the transcript."""
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Get last N lines
            all_lines = content.split('\n')
            recent = '\n'.join(all_lines[-lines:])
            return recent.lower()
    except Exception as e:
        print(f"[Website DM] Error reading transcript: {e}", file=sys.stderr)
        return ""


def detect_agent_type(transcript):
    """Detect which agent just completed based on transcript content."""
    # Look for agent invocation patterns
    if 'subagent_type' in transcript:
        if '"website_planner"' in transcript or 'website_planner' in transcript:
            return 'website_planner'
        if '"website_developer"' in transcript or 'website_developer' in transcript:
            return 'website_developer'
        if '"website_tester"' in transcript or 'website_tester' in transcript:
            return 'website_tester'

    # Fallback: Look for role-specific outputs
    if 'planning complete' in transcript or 'website_requirements.md' in transcript:
        return 'website_planner'
    if 'development complete' in transcript or 'seed_data.sql' in transcript:
        return 'website_developer'
    if 'testing complete' in transcript or 'test results:' in transcript:
        return 'website_tester'

    return 'unknown'


def is_in_auto_website_workflow(transcript):
    """Check if we're in an auto-website workflow."""
    return '/auto-website' in transcript or 'ai自动化建站' in transcript or 'website dm' in transcript


def should_continue_workflow(todos_status, agent_completed):
    """
    Decision logic based on TODOS.md status.
    Returns: (should_block, reason)
    """
    MAX_DEBUG_ITERATIONS = 5

    # If no TODOS.md exists, don't interfere
    if not todos_status:
        return (False, None)

    # Phase 1: Planning completed -> Image Generation (DM handles) or Development
    if todos_status['phase1_complete'] and not todos_status['phase2_complete']:
        if agent_completed == 'website_planner':
            return (True,
                "Planning complete! Read `.claude/workflow/TODOS.md` and `.claude/workflow/IMAGE_GENERATION_PLAN.md`. "
                "You (DM) should now generate images using Zhipu AI API. "
                "For each image in the plan: "
                "1. Read the image prompt from IMAGE_GENERATION_PLAN.md "
                "2. Call Zhipu AI API using Bash tool "
                "3. Download and save the image to the website's templates/static/images/ directory "
                "4. Update TODOS.md to mark each image as complete "
                "After all images are generated, update TODOS.md Phase 2 as complete and use the **website_developer** agent for Phase 3.")

    # Phase 2: Image Generation completed -> Start Development
    if todos_status['phase2_complete'] and not todos_status['phase3_complete']:
        # If DM just finished image generation, start developer
        return (True,
            "Images generated! Read `.claude/workflow/TODOS.md` to see Phase 3 tasks. "
            "Use the **website_developer** agent to: "
            "1. Read DATABASE_SCHEMA.md and CONTENT_PLAN.md "
            "2. Generate seed_data.sql with all database records "
            "3. Create all Jinja2 template files "
            "4. Update CSS styles "
            "5. Initialize database and start server "
            "6. Update TODOS.md when complete.")

    # Phase 3: Development completed -> Start Testing
    if todos_status['phase3_complete'] and not todos_status['phase4_complete']:
        if agent_completed == 'website_developer':
            return (True,
                "Development complete! Read `.claude/workflow/TODOS.md` Phase 4 tasks. "
                "Use the **website_tester** agent to: "
                "1. Verify server is running on http://localhost:8000 "
                "2. Test all pages using Chrome DevTools MCP "
                "3. Check all images load (no 404s) "
                "4. Check all links work (no 404s) "
                "5. Verify all columns have content "
                "6. Test mobile responsiveness "
                "7. Report PASSED or FAILED with details "
                "8. Update TODOS.md with test results.")

    # Phase 4: Testing completed
    if todos_status['phase4_complete']:
        if agent_completed == 'website_tester':
            # All tests passed -> Complete
            if todos_status['phase4_status'] == 'passed':
                return (False, None)  # Let workflow finish naturally

            # Tests failed -> Enter debug loop
            if todos_status['phase4_status'] == 'failed':
                iteration = todos_status['debug_iteration']

                # Max iterations reached
                if iteration >= MAX_DEBUG_ITERATIONS:
                    print(f"[Website DM] Max debug iterations ({MAX_DEBUG_ITERATIONS}) reached", file=sys.stderr)
                    return (False, None)

                # Start debug cycle - go directly to developer (skip debugger agent)
                return (True,
                    f"Tests failed (Debug Iteration {iteration + 1}/{MAX_DEBUG_ITERATIONS}). "
                    f"Read `.claude/workflow/TODOS.md` Phase 5 for failure details. "
                    f"Use the **website_developer** agent to: "
                    f"1. Review test failure report "
                    f"2. Fix all reported issues "
                    f"3. Test fixes locally "
                    f"4. Update TODOS.md when fixes complete "
                    f"Then tester will re-run tests.")

    # Debug loop: Developer completed fixes -> Re-test
    if agent_completed == 'website_developer' and todos_status['debug_iteration'] > 0:
        iteration = todos_status['debug_iteration']
        return (True,
            f"Fixes implemented (Iteration {iteration}). Read `.claude/workflow/TODOS.md` for test checklist. "
            f"Use the **website_tester** agent to: "
            f"1. Re-run all functional tests "
            f"2. Focus on previously failed tests "
            f"3. Verify fixes work "
            f"4. Update TODOS.md Phase 4 status: PASSED or FAILED "
            f"If PASSED, workflow will complete. If FAILED and iteration < 5, will loop to developer again.")

    # Unknown or intermediate state - don't interfere
    return (False, None)


def main():
    """Main hook execution."""
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)

        # Extract transcript path
        transcript_path = hook_input.get('transcript_path', '')
        if not transcript_path:
            # No transcript available, exit gracefully
            sys.exit(0)

        # Read recent transcript
        transcript = read_recent_transcript(transcript_path)

        # Check if we're in an auto-website workflow
        if not is_in_auto_website_workflow(transcript):
            # Not in auto-website, don't interfere
            sys.exit(0)

        # Detect which agent just completed
        agent_completed = detect_agent_type(transcript)
        print(f"[Website DM] Agent completed: {agent_completed}", file=sys.stderr)

        # Try to read TODOS.md for decision making
        todos_content = read_todos_file()
        todos_status = parse_todos_status(todos_content) if todos_content else None

        if todos_status:
            print(f"[Website DM] Using TODOS.md for decision making", file=sys.stderr)
            print(f"[Website DM] Phase1 complete: {todos_status['phase1_complete']}", file=sys.stderr)
            print(f"[Website DM] Phase2 complete: {todos_status['phase2_complete']}", file=sys.stderr)
            print(f"[Website DM] Phase3 complete: {todos_status['phase3_complete']}", file=sys.stderr)
            print(f"[Website DM] Phase4 complete: {todos_status['phase4_complete']}", file=sys.stderr)
            print(f"[Website DM] Phase4 status: {todos_status['phase4_status']}", file=sys.stderr)
            print(f"[Website DM] Debug iteration: {todos_status['debug_iteration']}", file=sys.stderr)

            # Use TODOS-based decision logic
            should_block, reason = should_continue_workflow(todos_status, agent_completed)
        else:
            print(f"[Website DM] TODOS.md not available, allowing completion", file=sys.stderr)
            should_block, reason = (False, None)

        if should_block and reason:
            # Block and provide next instruction
            output = {
                "decision": "block",
                "reason": reason
            }
            print(json.dumps(output))
            print(f"[Website DM] Blocking with: {reason}", file=sys.stderr)
        else:
            # Allow natural completion
            print(f"[Website DM] Allowing completion", file=sys.stderr)
            sys.exit(0)

    except Exception as e:
        # Log error but don't interfere with workflow
        print(f"[Website DM] Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
