# Graph Report - .  (2026-06-07)

## Corpus Check
- Corpus is ~924 words - fits in a single context window. You may not need a graph.

## Summary
- 35 nodes · 45 edges · 9 communities (8 shown, 1 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_API Router & Response Models|API Router & Response Models]]
- [[_COMMUNITY_Flight Data & Service|Flight Data & Service]]
- [[_COMMUNITY_Geographic Bounding Box|Geographic Bounding Box]]
- [[_COMMUNITY_Custom Error Handling|Custom Error Handling]]
- [[_COMMUNITY_App Entry & Health|App Entry & Health]]

## God Nodes (most connected - your core abstractions)
1. `BoundingBox` - 7 edges
2. `Flight` - 7 edges
3. `OpenSkyError` - 7 edges
4. `fetch_flights()` - 7 edges
5. `_parse_state_vector()` - 5 edges
6. `FlightResponse` - 4 edges
7. `get_flights()` - 4 edges
8. `Flight` - 4 edges
9. `ErrorResponse` - 3 edges
10. `Any` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Any` --uses--> `BoundingBox`  [INFERRED]
  backend/services/opensky.py → backend/models/bbox.py
- `BoundingBox` --uses--> `BoundingBox`  [INFERRED]
  backend/services/opensky.py → backend/models/bbox.py
- `Flight` --uses--> `BoundingBox`  [INFERRED]
  backend/services/opensky.py → backend/models/bbox.py
- `OpenSkyError` --uses--> `BoundingBox`  [INFERRED]
  backend/services/opensky.py → backend/models/bbox.py
- `OpenSkyError` --uses--> `Flight`  [INFERRED]
  backend/services/opensky.py → backend/models/flight.py

## Import Cycles
- None detected.

## Communities (9 total, 1 thin omitted)

### Community 0 - "API Router & Response Models"
Cohesion: 0.27
Nodes (7): BaseModel, ErrorResponse, FlightResponse, Wrapper returned by GET /flights., Returned when something goes wrong (e.g. OpenSky is unreachable)., get_flights(), Fetch current state vectors for all aircraft visible over India.      Returns li

### Community 1 - "Flight Data & Service"
Cohesion: 0.31
Nodes (9): Any, BoundingBox, Flight, Flight, Represents a single aircraft's current state vector from OpenSky., fetch_flights(), _parse_state_vector(), Convert a raw OpenSky state vector into a Flight model.     Returns None if the (+1 more)

### Community 2 - "Geographic Bounding Box"
Cohesion: 0.40
Nodes (3): BoundingBox, Returns query parameters the OpenSky API expects., Geographic rectangle used to filter aircraft by region.     frozen=True makes in

### Community 3 - "Custom Error Handling"
Cohesion: 0.50
Nodes (3): Exception, OpenSkyError, Raised when the OpenSky API is unreachable or returns an error.     Carries an H

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `OpenSkyError` connect `Custom Error Handling` to `API Router & Response Models`, `Flight Data & Service`, `Geographic Bounding Box`?**
  _High betweenness centrality (0.175) - this node is a cross-community bridge._
- **Why does `Flight` connect `Flight Data & Service` to `API Router & Response Models`, `Custom Error Handling`?**
  _High betweenness centrality (0.157) - this node is a cross-community bridge._
- **Why does `BoundingBox` connect `Geographic Bounding Box` to `Flight Data & Service`, `Custom Error Handling`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `BoundingBox` (e.g. with `Any` and `BoundingBox`) actually correct?**
  _`BoundingBox` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `Flight` (e.g. with `Any` and `BoundingBox`) actually correct?**
  _`Flight` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `OpenSkyError` (e.g. with `BoundingBox` and `Flight`) actually correct?**
  _`OpenSkyError` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Returns 200 OK when the API is running.`, `Geographic rectangle used to filter aircraft by region.     frozen=True makes in`, `Returns query parameters the OpenSky API expects.` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._