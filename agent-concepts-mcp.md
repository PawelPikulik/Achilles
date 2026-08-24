# Agent Concepts and MCP Basics — Explainer

## What Is an Agent, and What Is a Workflow?

Anthropic draws a clean line between **workflows** and **agents**. A **workflow** is a system where an LLM and tools are orchestrated through *predefined code paths*. The developer decides the sequence: first do this, then check that, then call this tool. The LLM is a step in a script the human wrote.

An **agent** is a system where the LLM *dynamically directs its own process and tool usage*. The developer gives the LLM a goal and tools, but the LLM decides which tool to call when, whether to loop, and when to stop. The difference is who controls the branching logic: in a workflow, the human wrote the `if` statements; in an agent, the LLM writes them at runtime.

## Classifying My FL-04 Pipeline

My FL-04 pipeline — the "Three Roads" stack selection — is a **workflow**, not an agent.

I gave the LLM four constraints and asked for three stack options. Then I pressure-tested each option with four predefined questions: what breaks, what do I maintain, can I finish in two weeks, does it show my work well. Finally, I made the decision. The LLM did not decide which option to pick, which questions to ask, or whether to loop back. It followed my script: generate → evaluate → decide. Every branch was predefined by me.

If this were an agent, I would have given the LLM the goal ("pick a stack for my portfolio") and tools (web search for hosting prices, file reader for my code, comparison formatter), and let it decide which tool to use, when to stop, and which option to recommend. The *process* would have been LLM-directed, not human-directed.

## What Is MCP?

MCP — the **Model Context Protocol** — is an open standard for connecting AI applications to external systems. The official analogy is USB-C: a standardized way to connect AI apps to data sources, tools, and workflows. Before MCP, every integration was bespoke. MCP replaces this with a single protocol: build an MCP server once, and any MCP-compatible client — Claude Desktop, Claude Code, Cursor, VS Code Copilot — can use it.

## MCP's Three Primitives

MCP defines three core primitives that an MCP server can expose to a client:

1. **Tools** — Functions the client calls to perform actions. My filesystem server exposes three: `read_file`, `list_directory`, `write_file`. Tools are the "do something" primitive.

2. **Resources** — Data sources the client reads, usually identified by a URI (e.g., `file:///home/user/doc.txt`). Resources are passive data, distinct from active tools.

3. **Prompts** — Reusable prompt templates the server exposes, such as "Summarize this code file." Prompts give the client pre-tested ways to interact with the domain.

My server implements only **tools**; the protocol supports all three.

## Evidence: Three Tasks Chat Alone Could Not Do

I built an MCP filesystem server (`mcp_server.py`) using Python's official MCP SDK and connected a test client (`mcp_client_test.py`) via stdio transport. I ran three tasks chat alone could never do:

**Task 1: Read a local file.** The client called `read_file` on `README.md`. Chat cannot read local files unless I paste their contents into the window. The MCP server granted direct, structured access without copy-pasting.

**Task 2: List directory contents.** The client called `list_directory` on the repo root. Chat cannot browse directories; I would have to run `dir`, copy the output, and paste it. The MCP server automated this discovery.

**Task 3: Write a new file.** The client called `write_file` to create `mcp_test_output.txt`. Chat cannot create files on my machine. It can suggest contents, but I must manually open an editor, paste, and save. The MCP server wrote the file directly with one tool call.

All three tasks ran through the same protocol: JSON-RPC request → server execution → structured result. The protocol was the bridge.

## What My FL-04 Workflow Would Need to Become an Agent

My FL-04 pipeline could become an agent if I handed control to the LLM. Here is what would change:

**Current state (workflow):** I defined the four evaluation questions. I decided which option to pick. The LLM generated content on my command.

**Agent upgrade:** I would give the LLM a goal — "evaluate three stack options and pick the best one for my portfolio" — and three tools: a web-search tool for hosting prices, a file-reader tool for inspecting my existing code, and a comparison-table tool. The LLM would decide which tool to use when. It might read my files first, then search, then compare — or it might search first, read second, then decide the order was wrong and loop back. The LLM would control the branching, not me.

The critical difference is **who owns the uncertainty**. In my workflow, there was no uncertainty — I knew exactly which four questions to ask. An agent is useful when the path is unknown; a workflow is better when the path is known and must be repeatable. My portfolio stack decision was a known path, so a workflow was correct. But if I were evaluating ten unknown hosting providers against five unknown frameworks, an agent would save me from writing the evaluation script myself.

---

*Evidence: `mcp_test_evidence.txt` and `mcp_test_output.txt` in this repo show the three tool calls running through the MCP filesystem server.*
