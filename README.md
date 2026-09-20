## Will Ryan

Senior Machine Learning Engineer at DraftKings, previously Salesforce. I work on production ML
and agentic systems — recommendation, retrieval, and the infrastructure that keeps them honest.
Most of what I build is an attempt to find out whether something actually works, so a fair amount
of it ends up written up as negative results.

Lately I've been interested in two questions: where small models lose information they were
already given, and how far an autonomous agent can be pushed before the bounds have to come from
the system rather than from the model.

---

**[guild](https://github.com/willryan1/guild)** · Python, Postgres

An autonomous internet holding company: agents that discover, validate, and operate digital
businesses. Event-driven, hard-bounded campaigns, a permission model that denies rather than
prompts, and every state transition written to the database. 16 architecture decision records,
269 tests.

**[retention-headroom](https://github.com/willryan1/retention-headroom)** · Python, PyTorch

When an LLM's context is pruned to a budget, does selecting chunks by causal contribution beat
selecting by attention? Measured on Qwen3-0.6B over LongBench QA against hindsight oracles and a
pre-registered threshold. The answer is *barely* — and the more useful finding is that the gap
which made this look promising in the first place was an artifact of a weak baseline.

**[NeuroSpace](https://github.com/willryan1/NeuroSpace)** · Python, TypeScript, Solidity

Decentralized LLM inference with verifiable provenance — prompts and responses stored on IPFS,
transaction hashes recorded on Base. FastAPI backend, React frontend, local model serving.

**[brain](https://github.com/willryan1/brain)** · Python, PyTorch

A sketch of four principles of biological cognition in ~400 lines: predictive world model,
episodic memory, curiosity-driven exploration, and wake/sleep consolidation. Runs on a laptop CPU.

---

The older repositories here — [ML-Algorithms](https://github.com/willryan1/ML-Algorithms),
[FirstNN](https://github.com/willryan1/FirstNN),
[Java-Neural-Net](https://github.com/willryan1/Java-Neural-Net) — are me learning the fundamentals
by implementing them from scratch without libraries, mostly between 2019 and 2020.
