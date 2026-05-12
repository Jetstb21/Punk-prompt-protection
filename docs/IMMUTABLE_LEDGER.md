# Tamper-Evident Ledger v0.1

AI prediction is a moving layer. A ledger is the fixed base layer.

Prediction tells what may be true. Ledger proves what happened.

This project starts with a local append-only, tamper-evident JSONL ledger. It does not claim that a local file is impossible to delete or rewrite. Instead, it makes mutation detectable: every event depends on the prior event hash.

## Event Fields

- event_index
- created_utc
- event_type
- input_sha256
- decision
- previous_hash
- metadata
- event_hash

## Rules

No event is edited. Corrections are new events. Each event points backward to the previous event. Replay must produce the same final head hash.

## Future Anchors

Stronger immutability can be layered later by anchoring ledger head hashes into Git commits, signed tags, release checksums, external timestamp services, and distributed copies.

## Private GRECO Extension

The public software ledger is the first layer only. The private GRECO architecture extends the ledger through an inner/outer sphere model with 50% overlap, Green Zone partitions, and local/global snap-reset checkpoints.

- I-sphere = inner protected ledger / brain
- O-sphere = outer operational shell
- 50% overlap = reconstructive zone
- first circumference = locked identity shell
- second circumference = restriction / defense / reconstruction boundary

Damage at the exposed shell can be reconstructed from overlap, valid snap reset, and replayed ledger state.
