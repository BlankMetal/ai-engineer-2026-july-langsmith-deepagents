"""Interactive human-in-the-loop review for the workshop notebook.

Drives a Deep Agent through its HITL interrupts by prompting for a decision
(approve / edit / reject) on each pending tool call, then resuming the graph.
Intended for interactive notebook use: it calls input(), which blocks until the
user responds, so execution pauses in the cell until a decision is entered.
"""

from langgraph.types import Command


def review_interrupts(agent, result, config):
    """Interactively review pending tool calls until the graph finishes.

    Loops while the result carries an interrupt, prompting the user to approve,
    edit, or reject each requested tool call, then resumes the agent. Choices
    are guarded against each tool's allowed_decisions.

    Args:
        agent: The compiled Deep Agent (with a checkpointer) to resume.
        result: The result from the initial invoke that may carry an interrupt.
        config: The run config carrying the thread_id, reused on each resume.

    Returns:
        The final result dict after all interrupts are resolved.
    """
    while result.get("__interrupt__"):
        request = result["__interrupt__"][0].value
        decisions = []
        for action, review in zip(request["action_requests"], request["review_configs"]):
            allowed = review["allowed_decisions"]
            print(f"\nTool call awaiting review: {action['name']}")
            print(f"   Args: {action['args']}")
            choice = input(f"   Decision {allowed} (default: approve) > ").strip().lower() or "approve"

            if choice == "edit" and "edit" in allowed:
                new_content = input("   New file content > ")
                decisions.append({
                    "type": "edit",
                    "edited_action": {"name": action["name"], "args": {**action["args"], "content": new_content}},
                })
            elif choice == "reject" and "reject" in allowed:
                message = input("   Reason (optional) > ").strip()
                decisions.append({"type": "reject", "message": message or "Rejected by the user."})
            else:
                decisions.append({"type": "approve"})

        result = agent.invoke(Command(resume={"decisions": decisions}), config=config)

    return result
