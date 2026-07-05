# Phase 5 Learning Guide — Mac AI Onboarding Toolkit

> **How to use this file:** Read a section, open the folder in Cursor/VS Code,
> run the commands, try the exercises. One folder per session is plenty.
> The goal is *muscle memory*, not finishing fast.

---

## Quick Decision Guide — When to Use Which Folder

```
One model call, max control          → 01 (Claude)  03 (OpenAI)
Real-time X/Twitter data             → 16 (Grok)
Many providers, one key              → 04 (OpenRouter)
Composable chains, provider-swap     → 05 (LangChain)
Loops / retries / branching flow     → 06 (LangGraph)
Role-based multi-agent teams         → 07 (CrewAI)
Local vector search + RAG            → 08 (ChromaDB)
Local models, free, private          → 09 (Ollama) or 18 (Qwen native client)
Typed JSON output from any LLM       → 10 (Structured Outputs)
Expose LLM logic as HTTP API         → 11 (FastAPI)
Quick demo UI, no HTML               → 12 (Streamlit / Gradio)
Open model catalog + hosted API      → 13 (HuggingFace)
Give your tools to Claude Code       → 14 (MCP Server)
Regression-test your LLM app        → 15 (Evals)
Enterprise Azure compliance          → 17 (Azure OpenAI)  ← lowest priority
```

---

## 3-Stage Learning Path

### Stage 1 — Activate (run the code as-is)

Start with zero-cost folders first, then unlock the rest with keys.

**Zero cost — Ollama already running:**
```bash
cd 09_ollama_mlx_local && uv run python example.py
cd 18_qwen_local       && uv run python example.py
```

**Add `ANTHROPIC_API_KEY` to each folder's `.env` → unlocks 8 folders:**
```bash
# copy .env.example then add your key once:
for d in 01 05 06 07 08 10 11 12 15; do
  cp ${d}_*/.env.example ${d}_*/.env
done
# then edit each .env and add: ANTHROPIC_API_KEY=sk-ant-...
```

**Run all mocked tests (no key needed) to confirm everything works:**
```bash
for d in */; do
  [ -f "$d/pyproject.toml" ] && (cd "$d" && uv run pytest tests/ -q 2>&1 | tail -1)
done
```

### Stage 2 — Break and Rebuild (where real learning happens)

For each folder, make ONE change, observe the result, revert.
Specific exercises are in each folder's section below.

### Stage 3 — Combine Folders (capstone projects)

| Mini-project | Folders | What you build |
|---|---|---|
| Typed RAG API | 08 + 10 + 11 | FastAPI that retrieves docs → returns structured JSON |
| Local eval harness | 18 + 15 | Judge Qwen output locally, zero API cost |
| Research crew with UI | 07 + 12 | CrewAI backend behind a Streamlit frontend |
| MCP tool for your notes | 14 + 08 | MCP server that does RAG over your own markdown files |
| Multi-model A/B dashboard | 04 + 12 | Gradio UI comparing Claude vs GPT vs Grok side by side |

---

## Folder Cheatsheets + Hands-On Exercises

---

### 01 — Anthropic SDK `claude-haiku-4-5-20251001`

**What it does:** Raw `client.messages.create()` — the baseline everything else builds on.

**Key patterns:**
```python
# Basic
response = client.messages.create(model=MODEL, max_tokens=256,
    messages=[{"role": "user", "content": "Hello"}])
print(response.content[0].text)

# Streaming
with client.messages.stream(...) as stream:
    for text in stream.text_stream: print(text, end="")

# Tool use
response = client.messages.create(tools=[{...}], tool_choice={"type": "auto"}, ...)
if response.stop_reason == "tool_use":
    tool_block = next(b for b in response.content if b.type == "tool_use")
```

**Exercises:**
1. **Model swap:** Change `MODEL` to `"claude-opus-4-8"`. Notice the latency difference.
   Then swap back to haiku. This is your cost/quality dial.
2. **System prompt:** Add `system="Reply only in haiku poetry."` to `messages.create`.
   Run `demo_basic()`. Try removing the system prompt — what changes?
3. **Multi-turn:** In `demo_tool_use()`, after getting the tool result, append both the
   assistant response and a `{"role": "user", "content": "What about London?"}` message
   and call `create()` again. You've built a conversation.

---

### 02 — Google ADK

**What it does:** Google's `Agent + Runner` pattern for Gemini-based agents with sessions.

**Key pattern:**
```python
agent = Agent(name="helper", model="gemini-2.0-flash", instruction="...", tools=[])
runner = Runner(app_name="demo", agent=agent, session_service=InMemorySessionService())
session = runner.session_service.create_session_sync(app_name="demo", user_id="u1")
for event in runner.run(user_id="u1", session_id=session.id, new_message=...):
    if event.is_final_response(): print(event.content.parts[0].text)
```

**Exercises:**
1. **Add a tool:** In `demo_tool_use()`, add a second tool (e.g. `get_news`) to the agent's
   `tools=[]` list. Observe how the agent decides which tool to call.
2. **Session memory:** Make two sequential `runner.run()` calls in the same session.
   Ask "My name is Himanshu" then "What's my name?" — the agent should remember.
3. **Instruction tuning:** Change the `instruction=` string to make the agent reply only
   in bullet points. Run the demo and observe the format change.

---

### 03 — OpenAI SDK

**What it does:** `client.chat.completions.create()` + streaming + tool_use. The pattern
that 04/16/17 all inherit via base_url swap.

**Key patterns:**
```python
# Chat
response = client.chat.completions.create(model=MODEL, messages=[...])
reply = response.choices[0].message.content

# Stream (v2 context manager)
with client.chat.completions.stream(...) as stream:
    for event in stream:
        delta = event.choices[0].delta.content
        if delta: print(delta, end="")

# Tool detection
if response.choices[0].finish_reason == "tool_calls":
    call = response.choices[0].message.tool_calls[0]
    args = json.loads(call.function.arguments)
```

**Exercises:**
1. **Provider swap preview:** Change `base_url` and `api_key` to use Ollama:
   ```python
   client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
   MODEL = "qwen2.5-coder:14b"
   ```
   The rest of the code runs unchanged. This is the portability promise.
2. **Parallel tool calls:** Add `parallel_tool_calls=True` to `create()`. Ask
   "What's the weather in Paris AND Tokyo?" — observe two tool_calls in the response.
3. **Temperature sweep:** Run `demo_basic()` in a loop with `temperature` from 0.0 to 1.5.
   Print each reply. Notice when output starts getting creative vs deterministic.

---

### 04 — OpenRouter

**What it does:** One `OPENROUTER_API_KEY` → access to Anthropic, OpenAI, Mistral, Llama,
etc. via a single OpenAI-compatible endpoint.

**Key pattern:**
```python
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)
# Then: client.chat.completions.create(model="anthropic/claude-haiku-4-5", ...)
```

**Exercises:**
1. **A/B compare:** Run `demo_ab_compare()`. Add a third model (e.g.
   `"mistralai/mistral-7b-instruct"`) to the comparison. Compare speed and quality.
2. **Free models:** Check `openrouter.ai/models?filter=free` — add a free model slug
   to `demo_basic()`. Zero cost, great for prototyping.
3. **Fallback pattern:** Wrap `demo_basic()` in a try/except. If the primary model
   raises an exception, fall back to a cheaper model. This is OpenRouter's killer use case.

---

### 05 — LangChain

**What it does:** LCEL `model | parser` chains, `InMemoryVectorStore` retrieval,
provider-swap in one line.

**Key patterns:**
```python
# LCEL chain
chain = ChatAnthropic(model=MODEL) | StrOutputParser()
reply = chain.invoke([HumanMessage(content="Hello")])

# Provider swap (one line change)
chain = ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

# RAG
store = InMemoryVectorStore(embedding=_HashEmbeddings())
store.add_texts(["doc 1", "doc 2"])
docs = store.similarity_search("query", k=2)
```

**Exercises:**
1. **Chain extension:** Pipe a second prompt into the chain:
   ```python
   summary_prompt = ChatPromptTemplate.from_template("Summarize in 5 words: {text}")
   chain = ChatAnthropic(model=MODEL) | StrOutputParser() | summary_prompt | ChatAnthropic(model=MODEL) | StrOutputParser()
   ```
   This is a two-step chain. Observe how LangChain threads data through.
2. **Real embeddings swap:** Replace `_HashEmbeddings` with `OllamaEmbeddings` from
   `langchain_community.embeddings` (Ollama already running). Retrieval quality improves.
3. **Stream a chain:** Call `chain.stream(...)` instead of `chain.invoke(...)`. Iterate
   and print each chunk. LCEL makes streaming transparent.

---

### 06 — LangGraph

**What it does:** `StateGraph` with nodes and edges. `MessagesState` for automatic
message accumulation. `tools_condition` for ReAct loops.

**Key pattern:**
```python
graph = StateGraph(MessagesState)
graph.add_node("llm", llm_node)
graph.add_node("tools", ToolNode([get_weather]))
graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", tools_condition)  # routes back to llm or END
graph.add_edge("tools", "llm")
app = graph.compile()
result = app.invoke({"messages": [HumanMessage("What's the weather?")]})
```

**Exercises:**
1. **Add a node:** Add a `format_node` after `llm` that uppercases the final message.
   Add `graph.add_edge("llm", "format")` and `graph.add_edge("format", END)`.
   This teaches you how nodes chain.
2. **Human-in-the-loop:** Add `interrupt_before=["tools"]` to `graph.compile()`.
   The graph will pause before calling the tool — you can inspect state then resume
   with `app.invoke(None, config=config)`.
3. **Persistent checkpointing:** Add `MemorySaver` checkpointer to `compile()`. Run the
   same graph twice with the same `thread_id` in config. The second run picks up where
   the first left off — this is LangGraph's killer feature.

---

### 07 — CrewAI

**What it does:** Role-based agents. `Agent(role, goal, backstory)` + `Task(description,
expected_output, agent)` + `Crew(agents, tasks, process=Process.sequential)`.

**Key pattern:**
```python
researcher = Agent(role="Researcher", goal="...", backstory="...", llm=LLM(model=MODEL))
writer = Agent(role="Writer", ...)
task1 = Task(description="Research {topic}", expected_output="...", agent=researcher)
task2 = Task(description="Write article", expected_output="...", agent=writer)
crew = Crew(agents=[researcher, writer], tasks=[task1, task2])
result = crew.kickoff(inputs={"topic": "AI safety"})
```

**Exercises:**
1. **Swap to local model:** In `demo_research_write_crew()`, change the LLM to:
   ```python
   LLM(model="ollama/qwen2.5-coder:14b", base_url="http://localhost:11434")
   ```
   Zero API cost. Compare output quality vs Haiku.
2. **Add a third agent:** Add a `Reviewer` agent with `role="Editor"` that checks
   the writer's output for clarity. Add a third task. Run the 3-agent crew.
3. **Hierarchical process:** Change `process=Process.sequential` to
   `process=Process.hierarchical` and add a `manager_llm=LLM(...)`. A manager agent
   now delegates tasks dynamically instead of following a fixed sequence.

---

### 08 — ChromaDB RAG

**What it does:** `EphemeralClient()` → `get_or_create_collection()` → `upsert()` docs
→ `query()` by text → feed top-K chunks to Claude.

**Key pattern:**
```python
client = chromadb.EphemeralClient()
coll = client.get_or_create_collection("docs")
coll.upsert(documents=["doc..."], ids=["1"])
results = coll.query(query_texts=["search term"], n_results=3)
context = "\n".join(results["documents"][0])
# Feed context into Claude prompt
```

**Exercises:**
1. **Your own docs:** Replace `SAMPLE_DOCS` with 5 sentences from a Wikipedia article
   you care about. Query it with related questions. Observe what retrieves correctly and
   what misses — this teaches you chunking intuition.
2. **Persistent storage:** Change `EphemeralClient()` to
   `chromadb.PersistentClient(path="./chroma_db")`. Run once to populate, comment out
   upsert, run again — data persists across restarts.
3. **n_results tuning:** Change `n_results` from 3 to 1 and to 5. Run `demo_rag()` and
   compare Claude's answers. More context isn't always better — hallucination vs recall
   tradeoff.

---

### 09 — Ollama / MLX Local

**What it does:** OpenAI SDK pointing at `localhost:11434/v1`. Zero API key, zero cost.
Same code as folder 03 — only `base_url` and `api_key="ollama"` differ.

**Key pattern:**
```python
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
# All chat/stream/embed patterns identical to OpenAI SDK
```

**Exercises:**
1. **Model comparison:** Run `demo_basic()` with both `qwen2.5-coder:14b` and
   `gemma4:12b`. Ask the same coding question. Which is faster? Which is more correct?
2. **Embeddings for RAG:** Call `demo_embeddings()` and print `len(vec)`. Then use that
   vector in a cosine similarity against another embedding. This is the raw vector math
   folder 08 abstracts away.
3. **Concurrent requests:** Run `demo_basic()` in two Python threads simultaneously.
   Ollama handles concurrency — observe if the second request waits or runs in parallel
   (depends on `OLLAMA_NUM_PARALLEL` env var).

---

### 10 — Structured Outputs

**What it does:** Two patterns to get typed Pydantic objects from LLMs — no parsing,
no regex, validated data guaranteed.

**Key patterns:**
```python
# Native: tool_use forces the schema
response = client.messages.create(tools=[{"input_schema": MyModel.model_json_schema()}],
    tool_choice={"type": "tool", "name": "my_tool"}, ...)
obj = MyModel.model_validate(next(b for b in response.content if b.type=="tool_use").input)

# Instructor: wraps client, auto-retries on ValidationError
iclient = instructor.from_anthropic(anthropic.Anthropic())
obj = iclient.messages.create(response_model=MyModel, messages=[...])
```

**Exercises:**
1. **Design your own schema:** Create a `ProductReview(BaseModel)` with fields
   `sentiment: Literal["positive","negative","neutral"]`, `score: int = Field(ge=1,le=5)`,
   `key_points: list[str]`. Run both native and Instructor patterns with a real review.
2. **Force a validation error:** Add `price: float = Field(gt=0)` to a model. Ask the
   LLM for a product with price=-5. Watch Instructor retry automatically. Add
   `max_retries=1` to see it fail fast.
3. **OpenAI swap:** Change Instructor to:
   ```python
   import openai, instructor
   iclient = instructor.from_openai(openai.OpenAI(base_url="...", api_key="ollama"))
   ```
   Same Pydantic model, local model. Zero cost structured outputs.

---

### 11 — FastAPI Serving

**What it does:** `app.py` exposes `GET /health`, `POST /chat`, `POST /chat/stream` (SSE).
Tested with `TestClient`; API-tested with Bruno `api.bru`.

**Key pattern:**
```python
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    c = get_client()
    response = c.messages.create(model=MODEL, ...)
    return ChatResponse(reply=response.content[0].text, ...)
```

**Exercises:**
1. **Add an endpoint:** Add `POST /summarize` that takes `{"text": "...", "max_words": 50}`
   and returns `{"summary": "..."}`. Write the Pydantic request/response models first.
   Test with Bruno — add a new request to `api.bru`.
2. **Middleware:** Add request logging middleware:
   ```python
   @app.middleware("http")
   async def log_requests(request, call_next):
       print(f"{request.method} {request.url}")
       return await call_next(request)
   ```
   Run the server and hit an endpoint — watch the log.
3. **Rate limiting:** Add a simple in-memory counter. If more than 5 requests per minute,
   return `HTTPException(status_code=429)`. This is the first step toward production.

---

### 12 — Streamlit + Gradio

**What it does:** `streamlit_app.py` = `st.chat_input` loop with session state.
`gradio_app.py` = `gr.ChatInterface(fn=respond)`. Both import `chat_once()` from
`example.py`.

**Exercises:**
1. **Streamlit sidebar:** Add `st.sidebar.selectbox("Model", ["haiku","sonnet"])` to
   `streamlit_app.py`. Pass the selection to `chat_once()` as the model. Live model
   switching in the UI.
2. **Gradio streaming:** Change `gradio_app.py` to use `chat_stream()` from `example.py`.
   In Gradio, streaming requires `gr.ChatInterface(fn=stream_respond)` where the function
   yields chunks. See Gradio docs for the generator pattern.
3. **Deploy to HF Spaces:** Create a free HuggingFace Space (gradio type). Upload
   `gradio_app.py`, `example.py`, and a `requirements.txt`. Your app is live in minutes.
   (Set `ANTHROPIC_API_KEY` as an HF Space secret.)

---

### 13 — HuggingFace

**What it does:** `InferenceClient` for hosted API calls (needs `HF_TOKEN`).
`demo_local_pipeline()` for on-device sentiment (MPS on Mac).

**Key pattern:**
```python
from huggingface_hub import InferenceClient
client = InferenceClient(token=HF_TOKEN)
result = client.chat_completion(model="...", messages=[{"role":"user","content":"..."}])
```

**Exercises:**
1. **Browse models:** Run `demo_list_models(limit=10)`. Pick one, change `CHAT_MODEL`
   to it. Run `demo_chat_completion()`. Some models require Pro tier — you'll get a 402.
2. **Local pipeline (first run):** Run `demo_local_pipeline("I hate Mondays")`. It
   downloads ~67 MB on first run. Observe `label` and `score`. Try a nuanced sentence
   — when does the model get it wrong?
3. **Custom pipeline task:** Change `"sentiment-analysis"` to `"text-classification"` or
   `"zero-shot-classification"` with a different model. HuggingFace has 100+ task types.

---

### 14 — MCP Servers

**What it does:** `FastMCP` server with `@mcp.tool()` and `@mcp.resource()`. Register
once in `~/.claude/settings.json` — every MCP client can call your tools.

**Key pattern:**
```python
mcp = FastMCP("my_server")

@mcp.tool()
def my_tool(input: str) -> str:
    """Description used by the LLM to decide when to call this."""
    return f"Result: {input}"

if __name__ == "__main__":
    mcp.run()   # stdio transport (what Claude Code uses)
```

**Exercises:**
1. **Register with Claude Code:** Add the server to `~/.claude/settings.json` (path shown
   in the README). Restart Claude Code. Type "what's the weather in Mumbai?" in a new
   conversation — Claude Code should call your `get_weather` tool.
2. **Add your own tool:** Add a `@mcp.tool()` that reads a specific local file and returns
   its content. This turns Claude Code into a tool that knows your own notes/docs.
3. **Add an SSE server:** Change `mcp.run()` to `mcp.run(transport="sse")`. Now the server
   runs over HTTP and can be called from a browser or curl. Test with:
   ```bash
   curl http://127.0.0.1:8000/sse
   ```

---

### 15 — Evals & Testing

**What it does:** Three evaluation tiers:
- Tier 1: rule-based assertions (free, instant)
- Tier 2: LLM-as-judge scoring (flexible, costs tokens)
- Tier 3: parametrized golden dataset (regression suite)

**Key pattern:**
```python
# The system under test
def summarize(text, client=None) -> str: ...

# Tier 1 — deterministic
def test_summary_length(): assert len(summarize(long_text, mock)) < len(long_text)

# Tier 2 — LLM judge
def test_judge_score(): assert judge_summary(original, summary) >= 3

# Tier 3 — golden dataset
@pytest.mark.parametrize("text,expected", GOLDEN_SENTIMENT)
def test_golden(text, expected): assert classify_sentiment(text) == expected
```

**Exercises:**
1. **Build your own golden dataset:** Create 5 `(input, expected_sentiment)` pairs from
   real product reviews you've seen. Run Tier 3 with them. How many does the model get
   right without any prompting? Adjust the system prompt until it passes all 5.
2. **Regression guard:** Change a model constant (e.g. swap haiku for a worse model).
   Run the full test suite. Which tests break? This is the value of evals — catching
   silent quality degradation.
3. **LangSmith tracing:** Set `LANGSMITH_API_KEY` and `LANGSMITH_TRACING=true` in `.env`.
   Run `demo_summarize()`. Go to `smith.langchain.com` — you'll see the trace with input,
   output, latency, and token count logged automatically.

---

### 16 — Grok (xAI)

**What it does:** OpenAI SDK + `base_url="https://api.x.ai/v1"` + `XAI_API_KEY`.
Identical code to folder 03 — only credentials differ. Switching cost: 1.

**Key pattern:**
```python
client = OpenAI(base_url="https://api.x.ai/v1", api_key=XAI_API_KEY)
# All chat/stream/tool patterns identical to OpenAI SDK (folder 03)
```

**Exercises:**
1. **Side-by-side comparison:** Ask the same question to Grok (`grok-3-mini`) and
   Claude Haiku (`01`). Same prompt, compare: latency, style, factual accuracy.
2. **Don't confuse Grok with Groq:** Change `base_url` to Groq's endpoint
   (`https://api.groq.com/openai/v1`), `api_key` to `GROQ_API_KEY`, and `model` to
   `"llama-3.3-70b-versatile"`. Same code, different company, much faster inference.
3. **Current events:** Ask Grok a question about something from this week's news. Compare
   to Claude (which has a training cutoff). This shows Grok's real-time X data advantage.

---

### 17 — Azure OpenAI

**What it does:** `AzureOpenAI(azure_endpoint, api_key, api_version)`. Your deployment
name (not the model slug) goes in `model=`. Everything else identical to folder 03.

**Key pattern:**
```python
client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,   # https://my-resource.openai.azure.com/
    api_key=AZURE_API_KEY,
    api_version="2025-01-01-preview",
)
response = client.chat.completions.create(model=DEPLOYMENT, ...)
# DEPLOYMENT = your deployment name in Azure AI Studio, e.g. "gpt-4o-mini"
```

**Exercises:**
1. **Deployment name trap:** Try using `"gpt-4o-mini"` as the `model=` string (the
   OpenAI model slug, not your deployment name). Observe the 404 error. Fix by using
   your actual Azure deployment name. This is the #1 Azure gotcha.
2. **Auth swap:** Replace `api_key=` with Azure AD auth:
   ```python
   from azure.identity import DefaultAzureCredential, get_bearer_token_provider
   token_provider = get_bearer_token_provider(DefaultAzureCredential(), "...")
   client = AzureOpenAI(azure_ad_token_provider=token_provider, ...)
   ```
   Keyless auth — safer for production. (Needs `azure-identity` package.)
3. **Content filtering:** Azure adds content moderation on top of the model. Send a
   borderline prompt (e.g. asking about security vulnerabilities). Compare the response
   to direct OpenAI on the same prompt. Notice the Azure filter layer.

---

### 18 — Qwen Local (native ollama client)

**What it does:** `ollama.Client().chat()` — the native Python API vs folder 09's
OpenAI shim. Access to Ollama-specific fields: `eval_count`, `load_duration`, etc.

**Key pattern:**
```python
import ollama
client = ollama.Client()
response = client.chat(model="qwen2.5-coder:14b",
    messages=[{"role":"user","content":"..."}])
print(response.message.content)
print(f"tokens/s: {response.eval_count / response.eval_duration * 1e9:.0f}")
```

**Exercises:**
1. **Token speed measurement:** After `demo_basic()`, print
   `response.eval_count / (response.eval_duration / 1e9)` — this gives tokens/second.
   Compare `qwen2.5-coder:14b` vs `gemma4:12b` on the same prompt. Benchmark your Mac.
2. **Format=json:** Add `format="json"` to `client.chat()`. Ask the model to describe
   itself. The response will be valid JSON — no schema enforcement, just raw JSON mode.
3. **Thinking mode:** Some Qwen models support `think=True`. Try:
   ```python
   response = client.chat(model="qwen3:8b", messages=[...], think="high")
   ```
   The response will have a reasoning prefix before the answer. Compare to `think=False`.

---

## Mini-Project Walkthrough: Typed RAG API

**Folders used:** 08 (ChromaDB) + 10 (Structured Outputs) + 11 (FastAPI)

**What you build:** An API endpoint that:
1. Takes a `{"question": "..."}` POST request
2. Retrieves top-3 relevant chunks from ChromaDB
3. Asks Claude to answer using only those chunks
4. Returns a typed `{"answer": "...", "sources": [...], "confidence": "high|medium|low"}`

**Steps:**
1. In `11_fastapi_serving/app.py`, add `chromadb` and `pydantic` imports.
2. Create a `RagResponse(BaseModel)` with `answer`, `sources: list[str]`, `confidence`.
3. Add `POST /rag` that initialises a ChromaDB collection with 5 sample docs, queries it,
   and returns a `RagResponse`.
4. Add `ANTHROPIC_API_KEY` to `.env`. Run: `uv run uvicorn app:app --reload`.
5. Test with Bruno.

This is a real production pattern. Once it works, swap ChromaDB for Pinecone (cloud) by
changing one import — everything else stays the same.

---

## Phase 6+ Roadmap

When Phase 5 feels fluent (you can navigate any folder without reading the README), move to:

| Phase | Topic | Prereqs |
|---|---|---|
| 6 | Fine-tuning + LoRA | 13 (HF), 18 (local models) |
| 7 | Production agents (memory, auth, rate-limit) | 06 (LangGraph), 11 (FastAPI) |
| 8 | Deployment (Modal, Fly.io, Railway) | 11 (FastAPI) |
| 9 | LlamaIndex (retrieval-first framing) | 08 (ChromaDB), 05 (LangChain) |
| 10 | Evaluation at scale (LangSmith datasets) | 15 (Evals) |

**Signal you're ready for Phase 6:** You can complete the Mini-Project above from scratch
in under 30 minutes without looking at the individual READMEs.

---

*Last updated: July 2026 · All code tested on MacBook Pro M4 Pro, 24 GB RAM, Python 3.12*
