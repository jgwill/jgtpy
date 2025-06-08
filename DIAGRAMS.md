# Class Relationships

This document provides high level diagrams for the main services and command line interfaces.

```mermaid
classDiagram
    class JGTCDSRequest
    class JGTCDSSvc {
        +new_rq_default()
        +create()
        +zone_update_from_cdf()
    }
    class JGTCDS
    JGTCDSSvc --> JGTCDSRequest
    JGTCDSSvc --> JGTCDS

    class JGTIDSRequest
    class JGTIDS
    JGTCDS ..> JGTIDS
    JGTCDSSvc ..> JGTIDSRequest

    class JGTADSRequest
    class JGTADS
    JGTADS --> JGTADSRequest
```

These diagrams show how service classes depend on their request objects and core data modules.
