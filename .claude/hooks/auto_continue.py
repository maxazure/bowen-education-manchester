#!/usr/bin/env python3
"""
Auto-continue hook: Automatically continues to next pending task after completion
This hook monitors TodoWrite tool usage and prompts to continue with next pending task
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

def load_previous_todos():
    """Load the previous todos state from cache"""
    cache_file = Path(__file__).parent / ".todos_cache.json"
    if cache_file.exists():
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    return None

def save_todos_cache(todos):
    """Save current todos state to cache"""
    cache_file = Path(__file__).parent / ".todos_cache.json"
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(todos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Could not save todos cache: {e}", file=sys.stderr)

def extract_todos_from_args():
    """Extract todos from command line arguments (passed by TodoWrite tool)"""
    # The TodoWrite tool arguments should be in sys.argv
    # Format: auto_continue.py <tool_name> <tool_args_json>

    if len(sys.argv) < 3:
        return None

    tool_name = sys.argv[1]
    if tool_name != "TodoWrite":
        return None

    try:
        tool_args = json.loads(sys.argv[2])
        return tool_args.get("todos", [])
    except:
        return None

def find_next_pending_task(todos):
    """Find the next pending task in the list"""
    for todo in todos:
        if todo.get("status") == "pending":
            return todo
    return None

def count_tasks_by_status(todos):
    """Count tasks by their status"""
    counts = {"pending": 0, "in_progress": 0, "completed": 0}
    for todo in todos:
        status = todo.get("status", "pending")
        counts[status] = counts.get(status, 0) + 1
    return counts

def detect_completion(prev_todos, curr_todos):
    """Detect if a task was just completed"""
    if not prev_todos or not curr_todos:
        return False

    # Check if any task changed from in_progress to completed
    prev_in_progress = [t for t in prev_todos if t.get("status") == "in_progress"]
    curr_in_progress = [t for t in curr_todos if t.get("status") == "in_progress"]

    # If there were in_progress tasks before but fewer now, a task was likely completed
    if len(prev_in_progress) > len(curr_in_progress):
        return True

    # Also check if completed count increased
    prev_completed = sum(1 for t in prev_todos if t.get("status") == "completed")
    curr_completed = sum(1 for t in curr_todos if t.get("status") == "completed")

    return curr_completed > prev_completed

def main():
    """Main hook logic"""

    # Extract current todos from tool arguments
    current_todos = extract_todos_from_args()

    if not current_todos:
        # Not a TodoWrite call or no todos found
        sys.exit(0)

    # Load previous todos state
    previous_todos = load_previous_todos()

    # Save current state for next time
    save_todos_cache(current_todos)

    # Count tasks
    counts = count_tasks_by_status(current_todos)
    total_tasks = len(current_todos)

    # Print status summary
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"📋 Todo List Status Update", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)
    print(f"✅ Completed: {counts['completed']}/{total_tasks}", file=sys.stderr)
    print(f"🔄 In Progress: {counts['in_progress']}/{total_tasks}", file=sys.stderr)
    print(f"⏳ Pending: {counts['pending']}/{total_tasks}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    # Check if a task was just completed
    task_just_completed = detect_completion(previous_todos, current_todos)

    # Find next pending task
    next_task = find_next_pending_task(current_todos)

    if task_just_completed and next_task:
        print(f"\n🎯 TASK COMPLETED! Moving to next task...", file=sys.stderr)
        print(f"\n📌 Next Task: {next_task.get('content', 'Unknown')}", file=sys.stderr)
        print(f"{'='*60}\n", file=sys.stderr)

        # Output a strong prompt for Claude to continue
        print("\n" + "="*70, file=sys.stderr)
        print("🤖 AUTO-CONTINUE INSTRUCTION", file=sys.stderr)
        print("="*70, file=sys.stderr)
        print(f"\nPlease continue with the next pending task:", file=sys.stderr)
        print(f"\n  Task: {next_task.get('content', 'Unknown')}", file=sys.stderr)
        print(f"  Status: {next_task.get('status', 'pending')}", file=sys.stderr)
        print(f"\nMark this task as 'in_progress' and begin execution immediately.", file=sys.stderr)
        print(f"Do NOT wait for user confirmation. Continue automatically.", file=sys.stderr)
        print("="*70 + "\n", file=sys.stderr)

    elif counts['pending'] == 0 and counts['in_progress'] == 0:
        print(f"\n🎉 ALL TASKS COMPLETED! Great work!", file=sys.stderr)
        print(f"{'='*60}\n", file=sys.stderr)

    elif not next_task and counts['in_progress'] > 0:
        # There's a task in progress, let it continue
        in_progress_tasks = [t for t in current_todos if t.get("status") == "in_progress"]
        if in_progress_tasks:
            current_task = in_progress_tasks[0]
            print(f"\n🔄 Current Task in Progress: {current_task.get('content', 'Unknown')}", file=sys.stderr)
            print(f"{'='*60}\n", file=sys.stderr)

    sys.exit(0)

if __name__ == "__main__":
    main()
