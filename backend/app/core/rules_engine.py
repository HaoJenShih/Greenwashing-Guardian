# app/core/rules_engine.py
# -*- coding: utf-8 -*-
"""
Lightweight rules engine (annotation only, no scoring).
- Normalizes text
- Splits into sentences
- Applies simple patterns per ESG risk dimension
- Returns structured evidence (hits)
You can later replace/extend the RULES with your rules.json loader.

This file has ZERO external tool dependency.
"""

from __future__ import annotations
from typing import Dict, Any, List, TypedDict
import re

# ----------------------------
# Data types
# ----------------------------

class RuleHit(TypedDict):
    cat: str          # one of: "vague", "lack_metrics", "misleading", "cherry", "no_3rd"
    rule_id: int      # synthetic id (stable per rule)
    text: str         # matched sentence snippet
    sent_idx: int     # sentence index if available

class RuleScanResult(TypedDict):
    hits: List[RuleHit]
    notes: str


# ----------------------------
# Minimal rule set (can be replaced by rules.json loader)
# Notes:
# - Keep it small, robust, and language-agnostic
# - Add synonyms if needed
# ----------------------------

# Hedging / vague verbs (English + typical variants)
VAGUE_VERBS = r"(aim|seek|strive|endeavor|commit|pledge|work towards|aspire|intend|plan to)"

# Lack of metrics/targets: mentions targets without year/baseline
TARGET_WORDS = r"(target|goal|objective|commitment)"
YEAR_OR_BASELINE = r"(20\d{2}|baseline|base\s*year|reference\s*year|from\s*20\d{2})"

# Misleading terminology: scope-2 methods / certificates / avoided-emissions disclosure
SCOPE2_AMBIG = r"(renewable electricity|green electricity)"
SCOPE2_QUAL = r"(market[- ]based|location[- ]based|dual reporting|residual mix|REC|GO|guarantee of origin|retire|cancel)"
AVOIDED_EMISSIONS = r"(avoided emissions|enabled emissions)"

# Cherry-picked data: only scope 1/2; missing scope 3
SCOPE_MENTION = r"(scope\s*1|scope\s*2|scope\s*3)"

# Absence of third-party verification: offsets with no credible standard
NEUTRAL_OFFSET = r"(carbon neutral|climate neutral).*?(via|through|using).*?(offset|credit)s?"
THIRD_PARTY_STD = r"(PAS\s*2060|Verra|Gold\s*Standard|ICROA|ISAE\s*3000|AA1000)"


# Synthetic rules: (category, compiled regex, id)
_RULES: List[tuple[str, re.Pattern, int]] = [
    # Vague/unsubstantiated
    ("vague", re.compile(VAGUE_VERBS, re.IGNORECASE), 901),

    # Lack of metrics/targets
    ("lack_metrics", re.compile(fr"{TARGET_WORDS}(?!.*{YEAR_OR_BASELINE})", re.IGNORECASE), 102),

    # Misleading terminology
    ("misleading", re.compile(fr"{SCOPE2_AMBIG}(?!.*{SCOPE2_QUAL})", re.IGNORECASE), 402),
    ("misleading", re.compile(fr"{AVOIDED_EMISSIONS}(?!.*(separate|disclose|outside\s+inventory))", re.IGNORECASE), 303),

    # Cherry-picked
    ("cherry", re.compile(r"(only\s+scope\s*1\s*/\s*2|scope\s*3\s*(excluded|later|deferred))", re.IGNORECASE), 202),

    # Absence of third-party verification
    ("no_3rd", re.compile(fr"{NEUTRAL_OFFSET}(?!.*{THIRD_PARTY_STD})", re.IGNORECASE), 302),
]


# ----------------------------
# Helpers
# ----------------------------

_SENT_SPLIT = re.compile(r"(?<=[\.\?\!])\s+|\n+")

def _normalize(text: str) -> str:
    """Basic OCR / punctuation normalization."""
    if not text:
        return ""
    t = text.replace("\u00a0", " ")  # non-breaking space
    t = re.sub(r"[ \t]+", " ", t)   # collapse spaces
    return t.strip()

def _split_sentences(text: str) -> List[str]:
    """Naive sentence splitter; good enough for rules."""
    text = _normalize(text)
    if not text:
        return []
    parts = _SENT_SPLIT.split(text)
    # keep short sentences but drop pure empty
    return [p.strip() for p in parts if p and p.strip()]


# ----------------------------
# Public API
# ----------------------------

def scan(text: str, company: str | None = None) -> RuleScanResult:
    """
    Annotate evidence only (no scoring).
    Returns: {"hits": [...], "notes": "..."}
    """
    sents = _split_sentences(text)
    hits: List[RuleHit] = []

    for i, sent in enumerate(sents):
        # Whitelist heuristic: if a sentence mentions credible third-party standards,
        # we skip "no_3rd" flags for that same sentence.
        has_third_party = bool(re.search(THIRD_PARTY_STD, sent, re.IGNORECASE))

        for cat, rx, rule_id in _RULES:
            if cat == "no_3rd" and has_third_party:
                continue
            if rx.search(sent):
                hits.append(RuleHit(cat=cat, rule_id=rule_id, text=sent[:400], sent_idx=i))

    notes = f"sentences={len(sents)}; hits={len(hits)}; whitelist_in_sent=third_party"
    return RuleScanResult(hits=hits, notes=notes)
def score(text: str) -> dict:
    """
    Legacy stub to satisfy old callers (ESGMetricsCalculatorTool).
    Always returns zeros with legacy-compatible fields so nothing crashes.
    """
    breakdown = [
        {"type": "Vague or unsubstantiated claims", "value": 0.0},
        {"type": "Lack of specific metrics or targets", "value": 0.0},
        {"type": "Misleading terminology", "value": 0.0},
        {"type": "Cherry-picked data", "value": 0.0},
        {"type": "Absence of third-party verification", "value": 0.0},
    ]
    return {
        "radar": {"vague":0,"lack_metrics":0,"misleading":0,"cherry":0,"no_3rd":0},
        "overall": 0.0,
        "overall_greenwashing_score": {"score": 0.0},
        "breakdown": breakdown,
        "engine": "legacy-stub",
    }
