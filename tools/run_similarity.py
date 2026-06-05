from src.embeddings import _mock_embed
from src.chunking import compute_similarity

pairs = [
    ("The bus departs at 6:00 AM.", "Buses start service at six in the morning."),
    ("The metro is closed on Sunday.", "The train operates daily."),
    ("This document lists bus routes.", "The recipe requires eggs and flour."),
    ("Station A is near the museum.", "The museum is next to Station A."),
    ("Fare increases from next month.", "Tickets cost 2 USD per ride."),
]

print('embedder backend:', _mock_embed._backend_name)
for i, (a, b) in enumerate(pairs, 1):
    va = _mock_embed(a)
    vb = _mock_embed(b)
    score = compute_similarity(va, vb)
    print(f"Pair {i}: {score:.6f}")
