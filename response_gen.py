def draft_reply(email_row: dict, kb_snippets: list) -> str:
    name = email_row.get('sender', 'there')
    product_hint = ""
    subj = (email_row.get('subject') or '').lower()
    body = (email_row.get('body') or '').lower()
    for token in ["premium", "basic", "pro", "enterprise"]:
        if token in subj or token in body:
            product_hint = token.capitalize()
            break

    tone = email_row.get('sentiment', 'Neutral')
    empathy = {
        'Negative': "I’m sorry for the trouble you’ve experienced. Thanks for your patience while we get this fixed.",
        'Neutral': "Thanks for reaching out — happy to help.",
        'Positive': "We’re glad to hear from you and appreciate the kind words!"
    }[tone]

    kb_txt = "\n\n".join([f"Reference: {s['content']}" for s in kb_snippets if s.get('score',0) > 0])

    lines = [
        f"Hi {name},",
        empathy,
        f"Regarding your {('question about ' + product_hint) if product_hint else 'request'}, here’s what you can try:",
        kb_txt or "Our team will review your case and get back with detailed steps.",
        "\nIf the issue persists, please reply with any screenshots, your account email, and the last time it worked.",
        "\nBest regards,\nSupport Team",
    ]
    return "\n\n".join([l for l in lines if l.strip()])
