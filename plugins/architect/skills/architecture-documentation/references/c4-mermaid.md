# C4 diagrams in Mermaid

Use `flowchart`, which renders everywhere and gives full control over layout. Mermaid's native `C4Context` syntax is marked experimental and its layout is hard to control, so prefer it only if the repo already uses it. The `classDef` lines double as the legend's styling.

## System context

```mermaid
---
title: "System context: Clinic Booking"
---
flowchart TB
    patient["<b>Patient</b><br/>[Person]<br/>Books and cancels appointments"]
    booking["<b>Clinic Booking</b><br/>[Software system]<br/>Manages agendas and reservations"]
    whatsapp["<b>WhatsApp Business</b><br/>[External system]<br/>Delivers reminders"]

    patient -->|"Books appointments in"| booking
    booking -->|"Sends reminders through"| whatsapp
    whatsapp -->|"Delivers reminders to"| patient

    classDef person fill:#08427b,stroke:#052e56,color:#fff
    classDef system fill:#1168bd,stroke:#0b4884,color:#fff
    classDef external fill:#666,stroke:#444,color:#fff
    class patient person
    class booking system
    class whatsapp external
```

## Container

```mermaid
---
title: "Container diagram: Clinic Booking"
---
flowchart TB
    patient["<b>Patient</b><br/>[Person]"]

    subgraph boundary["Clinic Booking [Software system]"]
        web["<b>Web App</b><br/>[Container: Next.js]<br/>Booking UI"]
        api["<b>API</b><br/>[Container: NestJS]<br/>Booking rules and agendas"]
        worker["<b>Reminder Worker</b><br/>[Container: Node.js]<br/>Sends scheduled reminders"]
        db[("<b>Database</b><br/>[Container: PostgreSQL]<br/>Appointments, agendas")]
        queue[["<b>Job Queue</b><br/>[Container: Redis]<br/>Pending reminders"]]
    end

    whatsapp["<b>WhatsApp Business</b><br/>[External system]"]

    patient -->|"Books appointments using<br/>HTTPS"| web
    web -->|"Calls<br/>JSON/HTTPS"| api
    api -->|"Reads and writes<br/>SQL/TCP"| db
    api -->|"Enqueues reminders in<br/>Redis protocol"| queue
    worker -->|"Consumes reminders from<br/>Redis protocol"| queue
    worker -->|"Sends messages through<br/>HTTPS"| whatsapp

    classDef person fill:#08427b,stroke:#052e56,color:#fff
    classDef container fill:#438dd5,stroke:#2e6295,color:#fff
    classDef external fill:#666,stroke:#444,color:#fff
    class patient person
    class web,api,worker,db,queue container
    class whatsapp external
```

## Component

Same shape as the container diagram, with the `subgraph` standing for one container and the nodes marked `[Component: technology]`. Show the neighbouring containers outside the subgraph.

## Dynamic

Use a `sequenceDiagram`, one flow per diagram, with numbered steps (`autonumber`) and participants named after the containers.

## Deployment

Use nested `subgraph`s for deployment nodes (region, cluster, VPC), with container instances inside them and the replica count in the label, e.g. `API x3`.

## Legend

Add a small legend in the text next to the diagram, or as a separate `subgraph Key` when colors carry meaning: dark blue is a person, blue is this system or its containers, and grey is external.
