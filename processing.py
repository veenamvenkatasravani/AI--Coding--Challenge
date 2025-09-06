import re
import heapq
from dataclasses import dataclass, field
from typing import List, Dict, Any

URGENT_TERMS = {
    "immediately": 3, "urgent": 3, "asap": 3, "critical": 3,
    "cannot access": 2, "down": 2, "failed": 2, "not working": 2,
    "error": 1, "issue": 1, "problem": 1
}

POS_WORDS = {"thank", "great", "appreciate", "awesome", "love", "fixed"}
NEG_WORDS = {"frustrated", "angry", "bad", "terrible", "cannot", "can't", "won't",
             "refund", "issue", "error", "not working", "broken"}

EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+", re.I)
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}")

@dataclass(order=True)
class PrioritizedEmail:
    priority: int
    idx: int = field(compare=False)
    record: Dict[str, Any] = field(compare=False)

def extract_info(text: str) -> Dict[str, Any]:
    emails = EMAIL_RE.findall(text or "")
    phones = PHONE_RE.findall(text or "")
    return {"phones": list(set(phones)), "emails": list(set(emails))}

def sentiment(text: str) -> str:
    t = (text or "").lower()
    pos = sum(w in t for w in POS_WORDS)
    neg = sum(w in t for w in NEG_WORDS)
    if neg > pos:
        return "Negative"
    if pos > neg:
        return "Positive"
    return "Neutral"

def priority(subject: str, body: str):
    text = f"{subject} {body}".lower()
    hits = []
    score = 0
    for k, w in URGENT_TERMS.items():
        if k in text:
            hits.append(k)
            score += w
    label = "Urgent" if score >= 3 else "Not urgent"
    return label, score, hits

def build_priority_queue(df):
    pq = []
    for i, row in df.iterrows():
        pr_label, pr_score, hits = priority(row.get('subject',''), row.get('body',''))
        sent = sentiment(row.get('body',''))
        info = extract_info(row.get('body',''))
        rec = {
            **row.to_dict(),
            "sentiment": sent,
            "priority_label": pr_label,
            "priority_score": pr_score,
            "priority_hits": hits,
            "extracted": info,
        }
        heapq.heappush(pq, PrioritizedEmail(priority=-pr_score, idx=i, record=rec))
    return pq

def dequeue_all(pq) -> List[Dict[str, Any]]:
    out = []
    while pq:
        out.append(heapq.heappop(pq).record)
    return out
