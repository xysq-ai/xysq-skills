"""
Load fixture_vault.json into a dedicated test bank on the local Hindsight.

Usage (run from backend worktree so .env autoloads):
    cd /Users/Ximi-Hoque/Workspace/xysq/backend-worktrees/recall-skill-library
    python /Users/Ximi-Hoque/Workspace/xysq/xysq-skills/evals/fixture/load_fixture.py

NOTE: Re-running this script may produce duplicate documents in fixture-eval-bank.
Hindsight deduplication is content-hash-based but not guaranteed across repeated
calls with the same content. Clear the bank manually if a clean slate is needed.
"""

import asyncio
import json
import os
import sys

# Allow backend imports from the worktree regardless of cwd.
BACKEND_ROOT = "/Users/Ximi-Hoque/Workspace/xysq/backend-worktrees/recall-skill-library"
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

# pydantic-settings loads .env from cwd; ensure we point at the right one.
os.chdir(BACKEND_ROOT)

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixture_vault.json")
TEST_BANK_ID = "fixture-eval-bank"


async def main() -> None:
    from memory.factory import get_memory_provider
    from services.memory import RetainPayload, retain_to_bank

    with open(FIXTURE_PATH) as f:
        vault = json.load(f)

    memories = vault["memories"]
    print(f"Loaded {len(memories)} memories from fixture vault.")
    print(f"Target bank: {TEST_BANK_ID}")
    print()

    provider = get_memory_provider()

    retained = 0
    errors = 0

    # Ensure the dedicated test bank exists before writing to it.
    # _create_bank is idempotent (409 = already exists is silently ignored).
    try:
        await provider._create_bank(TEST_BANK_ID, name=TEST_BANK_ID)
        print(f"Bank '{TEST_BANK_ID}' ready.")
    except Exception as exc:
        print(f"Bank init warning (may already exist): {exc}")
    print()

    for m in memories:
        payload = RetainPayload(
            content=m["content"],
            tags=[f"memory_kind:{m['memory_kind']}", f"topic:{m['topic']}"],
            metadata={"topic": m["topic"], "memory_kind": m["memory_kind"], "fixture_idx": m["idx"]},
            timestamp=m["occurred_at"],
            # update_mode="replace" is required when document_id is None.
            # "append" (the default) requires an existing document_id to append to.
            update_mode="replace",
        )
        try:
            result = await retain_to_bank(provider, TEST_BANK_ID, payload)
            retained += 1
            print(f"  [{m['idx']:02d}] OK  {m['memory_kind']:<10} {m['topic']:<12} {m['occurred_at']}  -> {result}")
        except Exception as exc:
            errors += 1
            print(f"  [{m['idx']:02d}] ERR {m['memory_kind']:<10} {m['topic']:<12} {m['occurred_at']}  -> {exc}")

    print()
    print(f"Done. Retained: {retained}/{len(memories)}  Errors: {errors}")
    print(f"Bank: {TEST_BANK_ID}")


if __name__ == "__main__":
    asyncio.run(main())
