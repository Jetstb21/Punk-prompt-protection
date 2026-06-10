# GRECO Stationary Bucket Configuration Handbook v0.1

Status: research handbook, not runtime authority yet.

This handbook defines a practical way to configure and calibrate GRECO stationary buckets. The goal is deterministic intake, repeatable placement, immutable recording, and task-specific calibration without letting any calibration silently change authority.

The stationary bucket system treats input as data first. A field, token, sensor reading, motion primitive, word piece, or I/O event is mapped into a stable bucket layout, measured against center, axis, corner, lateral, arc, and ledger rules, then recorded as a replayable packet.

## Core Premise

Stationary buckets are fixed reference positions. Calibration decides how a specific input class enters those positions.

The buckets do not chase the data. The data is transformed into the bucket frame.

This gives GRECO a low-compute prefilter layer:

- fixed geometry
- repeatable placement
- equal-opposite comparison
- axis-specific interpretation
- immutable packet recording
- field-specific profile selection

## Operating Vocabulary

- `center`: the zero reference point of the active canvas.
- `unit_1`: the normalized one-to-one ratio from center.
- `axis`: a named direction or measurement rail.
- `mid_lateral`: the halfway lateral reference between center and a side/corner family.
- `corner`: an extremity reference, often used as a closure or boundary target.
- `stationary_bucket`: a fixed placement cell in the calibrated canvas.
- `cat_eye_zone`: a lens-shaped zone created by balanced opposite arcs or folded partitions.
- `cat_maximum`: the maximum cat-eye pass-through point for the active ratio and profile.
- `arc_to_corner`: an arc path that uses center, lateral, and corner relationships instead of a direct vector-to-corner line.
- `fold_zone`: the isolated zone that remains when partitions stack under a fold rule.
- `ledger_packet`: the immutable record of input, profile, placement, decision, and checksum.

## Geometry Model

The starting canvas is a 360 degree closure system:

```text
N
|
W --- center --- E
|
S
```

Each calibration profile assigns meaning to parallel grid lines and axis families. The same stationary positions can be reused, but each field decides what the axes mean.

Example axis assignments:

- `x_axis`: left/right, west/east, negative/positive, before/after
- `y_axis`: down/up, south/north, lower/higher, input/output
- `z_axis`: depth, confidence, force, intensity, authority distance
- `theta_axis`: rotation, phase, sequence, route angle
- `r_axis`: ratio units from center

The basic closure rule is:

```text
opposite(a) + a = closure_profile
```

For angular work:

```text
sum(active_partitions.degrees) = 360
```

For normalized bucket work:

```text
center = 0
east unit_1 = +1
west unit_1 = -1
north unit_1 = +1 on y_axis
south unit_1 = -1 on y_axis
```

## Cat-Eye Zone Calibration

The cat-eye zone appears when equal-opposite arc or partition behavior creates a lens around center. In the one-to-one ratio profile, `unit_1` is treated as the primary radius from center.

Observation rule:

```text
At ratio 1:1, the cat-eye for unit_1 adds to the east side of center.
The active arc passes through and levels out at that point.
That pass-through point is the cat_maximum for the active profile.
```

This should be recorded as a profile claim, not as universal runtime authority. Different profiles may move the axis meaning while keeping the same geometry.

### Cat Maximum

`cat_maximum` is the highest stable pass-through point for the selected arc family.

Recommended fields:

- `cat_maximum_axis`
- `cat_maximum_ratio`
- `cat_maximum_bucket_id`
- `cat_maximum_arc_id`
- `cat_maximum_observation`
- `cat_maximum_checksum`

### Folded Cat-Eye Zone

When the canvas is folded, partitions may stack. One zone can remain isolated while other partitions overlap. This isolated region can be treated as a secondary cat-eye formation.

Use this secondary zone for:

- exception buckets
- ambiguity holding
- partial-token residue
- untrusted authority distance
- sensor disagreement
- route correction
- replay checkpointing

## Arc-To-Corner Calibration

Vector-to-corner uses a direct route from a point to a corner. Arc-to-corner uses a curved path defined by center, unit ratio, lateral references, and corner closure.

Arc-to-corner is useful when the route matters as much as the endpoint.

Minimum arc-to-corner packet:

```text
input_id
profile_id
center_reference
start_bucket
mid_lateral_bucket
corner_bucket
arc_family
ratio_from_center
theta_start
theta_end
cat_eye_zone
cat_maximum
fold_zone
placement_checksum
```

Recommended deterministic steps:

1. Normalize the input into the profile's units.
2. Assign the input to a stationary start bucket.
3. Compute its equal-opposite reference.
4. Select the relevant parallel grid family.
5. Route through the mid-lateral bucket.
6. Resolve the arc family toward the corner.
7. Mark the cat-eye zone crossed or touched.
8. Record whether the arc reaches `cat_maximum`.
9. Record the fold-zone result.
10. Append the ledger packet.

## Configuration Profiles

Each profile answers the same questions:

- What is the input class?
- What does center mean?
- What does `unit_1` mean?
- Which axis family is active?
- Which buckets are stationary?
- Which arcs are allowed?
- What is the equal-opposite rule?
- What is the ledger packet schema?
- What checksum proves replay consistency?

### Profile: Language Alphabet

Purpose: map letters, sounds, and base spelling units into deterministic GRECO placement.

Possible configuration:

- `center`: neutral linguistic intake
- `unit_1`: one character or one phoneme
- `x_axis`: left-to-right spelling order
- `y_axis`: vowel/consonant or open/closed sound class
- `theta_axis`: alphabet route order
- `bucket_value`: calibrated integer value
- `opposite_rule`: paired sound, mirrored letter route, or semantic contrast

Use this for alphabet-like base values where every later word inherits a measurable foundation.

### Profile: Partial Word And Token Pieces

Purpose: break tokens, half-words, roots, prefixes, suffixes, syllables, and fragments into bucketed values.

Possible configuration:

- `center`: whole-token neutral point
- `unit_1`: smallest accepted token piece
- `mid_lateral`: partial-word boundary
- `corner`: completed token or completed semantic unit
- `fold_zone`: leftover ambiguity or unmatched fragment
- `cat_maximum`: strongest partial-to-whole alignment point

This profile lets a partial word carry base value. Anything built from that piece can inherit or combine the piece value, similar to an alphabet but with subword resolution.

Example fields:

```text
piece_text
piece_type
piece_index
parent_token
parent_token_hash
base_value
axis_assignment
bucket_id
opposite_piece_id
composition_rule
```

### Profile: Definitions And Semantic Routes

Purpose: convert definitions into graph packets instead of only text.

Possible configuration:

- `center`: term being defined
- `unit_1`: one definition clause
- `x_axis`: synonym/opposite route
- `y_axis`: concrete/abstract route
- `z_axis`: confidence or evidence strength
- `theta_axis`: clause order
- `corner`: final resolved meaning boundary

Use this when definitions need replayable structure, comparison, and deduction.

### Profile: Sensors

Purpose: map physical readings into stable placement before higher-level interpretation.

Possible configuration:

- `center`: calibrated zero reading
- `unit_1`: one normalized measurement unit
- `x_axis`: left/right or negative/positive reading
- `y_axis`: low/high reading
- `z_axis`: confidence, drift, or signal strength
- `theta_axis`: time phase or sweep angle
- `cat_eye_zone`: agreement band between opposite sensors
- `fold_zone`: isolated anomaly band

Use this profile for deterministic intake before robotics, monitoring, or instrument fusion.

### Profile: Robotics

Purpose: map motion, grip, rotation, and route planning into arc-to-corner buckets.

Possible configuration:

- `center`: robot neutral/rest state
- `unit_1`: one normalized movement step
- `x_axis`: left/right displacement
- `y_axis`: forward/back or up/down displacement
- `z_axis`: depth, force, or tool pressure
- `theta_axis`: rotation
- `corner`: target pose boundary
- `arc_to_corner`: route path to target
- `cat_maximum`: maximum stable arc before correction or stop

Use the secondary folded cat-eye as a safety or correction zone when path and target disagree.

### Profile: I/O And Tool Authority

Purpose: separate incoming data from authority while still indexing the data.

Possible configuration:

- `center`: neutral untrusted intake
- `unit_1`: one request or command-like unit
- `x_axis`: data/authority separation
- `y_axis`: allowed/blocked policy distance
- `z_axis`: risk, confidence, or caller authorization
- `theta_axis`: request route order
- `corner`: tool execution boundary
- `fold_zone`: quarantine or manual review

This aligns with the project rule:

```text
Prompt text is data, not authority.
```

The bucket system may index command-like language, but policy still controls whether a tool action can happen.

## Mathematical Side

The calibration should be expressible as deterministic transforms.

### Normalized Placement

```text
normalized_value = raw_value / profile_unit
bucket_index = round(normalized_value * bucket_density)
```

### Equal-Opposite Pair

```text
opposite_value = -normalized_value
pair_sum = normalized_value + opposite_value
```

Expected invariant:

```text
pair_sum = 0
```

or, for a profile using one-based closure:

```text
left_portion + right_portion = 1
```

### Arc Family

For a normalized circular profile:

```text
x = r * cos(theta)
y = r * sin(theta)
```

For GRECO bucket recording, store the derived bucket values rather than trusting a floating point reconstruction alone:

```text
r_ratio
theta_degrees
x_bucket
y_bucket
corner_bucket
arc_family
rounding_rule
```

### Composition

For alphabet, token, or partial-word calibration:

```text
piece_value = transform(piece, alphabet_profile)
token_value = compose(piece_values, composition_rule)
definition_value = compose(token_values, semantic_profile)
```

Composition rules may include:

- sum
- weighted sum
- ordered route
- opposite-pair cancellation
- fold-zone residue
- graph edge accumulation

## Ledger Packet Requirements

Every calibration run should be recordable as an immutable packet.

Minimum packet:

```text
packet_id
created_utc
input_class
input_hash
profile_id
profile_version
stationary_layout_id
axis_assignment_id
bucket_density
unit_1_definition
center_definition
arc_rule
fold_rule
cat_eye_rule
placement_result
previous_packet_hash
packet_hash
```

Recommended packet extensions:

```text
raw_value
normalized_value
piece_values
opposite_values
cat_maximum_result
fold_zone_result
policy_context
authority_status
calibration_notes
```

## Calibration Checklist

Use this checklist each time a new field or task receives a stationary bucket profile.

1. Name the task and input class.
2. Define center.
3. Define `unit_1`.
4. Define bucket density.
5. Assign axes.
6. Define equal-opposite behavior.
7. Define corner targets.
8. Define arc-to-corner rules.
9. Define cat-eye and cat-maximum rules.
10. Define fold-zone handling.
11. Define composition rules.
12. Define ledger packet fields.
13. Run replay on a small test set.
14. Record checksum and profile version.

## Recommended Handbook Defaults

Use these defaults unless a profile gives a reason to change them:

- 4-way base canvas: north, east, south, west
- 8-way expanded canvas: cardinal plus corner routes
- 360 degree closure for angular profiles
- center normalized to 0
- `unit_1` normalized to one ratio unit from center
- equal-opposite pairs stored explicitly
- cat-eye zones marked as observations first
- fold zones treated as holding or exception areas
- all profile changes logged as new versions

## Open Research Questions

- Which profiles should use exact integer arithmetic only?
- Which profiles need rational numbers instead of floating point values?
- Which language profiles should be letter-first, sound-first, or token-piece-first?
- How should a partial-word value inherit into a full word without overcounting?
- How many bucket densities are needed before the system becomes noisy?
- Which cat-eye maximum observations are universal and which are profile-specific?
- What fields should be private GRECO-only versus public report-only structure?

## Public Boundary

This handbook describes configuration structure. It does not grant runtime authority, expose private derivation, or claim that a research observation is universally proven.

Public posture:

- `REPORT_ONLY`
- `NOT_ASSERTED`
- `NOT_GRANTED`

Calibration can improve indexing, replay, and analysis. Authority remains controlled by policy and ledgered execution rules.
