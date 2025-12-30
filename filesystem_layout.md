# NimbOS Filesystem Layout (Authoritative)

## Design Principles

- **OS is reproducible and disposable**: configs + code define behavior
- **Data is durable and isolated**: user content survives reinstalls
- **Performance-aware**: SSD for runtime, HDD/RAID for bulk data
- **Clear boundaries**: each directory has a single responsibility

All NimbOS runtime lives under:

```
/opt/nimbos
```

Only **storage/** is mounted from a separate data disk.

---

## Top-Level Layout

```
/opt/nimbos
├── config/
├── runtime/
├── services/
├── ai/
├── logs/
├── cache/
└── storage/
```

---

## `/opt/nimbos/config` — Configuration (Persistent)

**Purpose**\
Defines *how the system behaves*.

**Contents**

- Service configuration files (YAML/TOML/JSON)
- `docker-compose.yml`
- API configuration
- WAN / network policies
- References to secrets (not raw secrets)

**Properties**

- Small, human-readable
- Version controlled (Git)
- Survives service restarts
- Survives OS reinstall (via restore)

**Why this exists**

- Enables full system rebuild from config
- Makes change history explicit
- Separates behavior from data

---

## `/opt/nimbos/runtime` — Runtime State (Ephemeral)

**Purpose**\
Holds short-lived system state created at runtime.

**Contents**

- PID files
- Unix sockets
- Lock files
- Temporary runtime metadata

**Properties**

- Recreated at boot
- Never backed up
- Safe to delete

**Why this exists**

- Prevents stale state issues
- Keeps backups clean
- Simplifies crash recovery

---

## `/opt/nimbos/services` — Service State (Fast SSD)

**Purpose**\
Persistent service-owned data that is *not* user content.

**Contents**

- Docker volumes
- Databases (indexes, metadata)
- Immich metadata / ML assets
- Syncthing indexes
- RAG indexes

**Properties**

- Performance-sensitive
- Rebuildable from config + data
- Service-specific formats

**Why this exists**

- Keeps heavy IO off HDD
- Allows service reset without data loss
- Clean container volume mapping

---

## `/opt/nimbos/ai` — AI Assets & Models (Fast SSD)

**Purpose**\
All local AI resources required for inference.

**Contents**

- Ollama models
- Embedding models
- Whisper models
- Tokenizer caches

**Properties**

- Large but reproducible
- Version-pinned
- Never user-modified

**Why this exists**

- Clear isolation of AI stack
- Predictable performance
- Easy model upgrades / swaps

---

## `/opt/nimbos/logs` — Logs

**Purpose**\
Centralized logging location.

**Contents**

- API logs
- Service logs
- AI inference logs
- WAN / audit logs

**Properties**

- Append-only
- Rotated
- Not snapshotted

**Why this exists**

- Prevents log sprawl
- Easy log rotation
- Simple container bind-mounts

---

## `/opt/nimbos/cache` — Rebuildable Cache

**Purpose**\
Performance-only data that can be regenerated.

**Contents**

- Thumbnails
- Transcodes
- Previews
- Temporary embeddings

**Properties**

- Safe to wipe
- Never backed up

**Why this exists**

- Explicit "safe to delete" boundary
- Prevents cache pollution

---

## `/opt/nimbos/storage` — User & Content Data (HDD / RAID)

**Purpose**\
The only location for *irreplaceable user data*.

Mounted from a **separate disk**.

```
storage/
├── users/     # home directories
├── shared/    # shared documents
└── media/     # photos, videos, backups
```

**Properties**

- Large
- Snapshotted
- Backed up
- Survives OS reinstall

**Why this exists**

- Enables safe OS replacement
- Clear snapshot & rollback scope
- Simple installer logic

---

## Architectural Benefits (Summary)

- Physical OS/data separation
- Clean backup boundaries
- Safe experimentation
- Deterministic rebuilds
- Clear permissions model
- AI treated as infrastructure

This layout is intentionally boring, explicit, and resilient — exactly what a base OS layer should be.

