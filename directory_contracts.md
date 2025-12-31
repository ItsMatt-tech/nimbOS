# NimbOS Directory Contracts (Authoritative)

This document defines the **access contracts** for all directories under `/opt/nimbos`.

These contracts are *design-level guarantees* that guide:

- filesystem permissions
- container volume mappings
- backup & snapshot scope
- security hardening

Violations of these contracts are considered **bugs**.

---

## Core Principles

- **User data lives only in **``
- **Configuration is input, never output**
- **Runtime state is disposable**
- **Caches are safe to delete**
- **AI is infrastructure, not content**
- **Services never write outside their scope**

---

## Contract Matrix

### `/opt/nimbos/config`

**Purpose:** Define system behavior

**Access**

- `arcowl`: RW (development phase)
- `nimbos`: R
- Containers: R (read-only bind mounts)

**Rules**

- Never written by containers
- Version controlled
- Changes require service restart

---

### `/opt/nimbos/runtime`

**Purpose:** Transient runtime state

**Access**

- `nimbos`: RW
- Containers: RW
- `arcowl`: R (debug)

**Rules**

- Cleared on reboot
- Never backed up
- No persistent meaning

---

### `/opt/nimbos/services`

**Purpose:** Service-owned persistent state (non-user)

**Access**

- Owning service: RW
- Other services: ❌
- `arcowl`: R (debug), RW via sudo

**Rules**

- One directory per service
- Rebuildable from config + data
- May later change ownership to per-service users

---

### `/opt/nimbos/ai`

**Purpose:** AI models and inference assets

**Access**

- AI services: RW
- Other services: R
- `arcowl`: R

**Rules**

- No user writes
- Version pinned
- Large but reproducible

---

### `/opt/nimbos/logs`

**Purpose:** Observability

**Access**

- Services: RW (append-only)
- `arcowl`: R
- API/UI: R

**Rules**

- Rotated
- Never snapshotted
- Never user-modified

---

### `/opt/nimbos/cache`

**Purpose:** Performance-only data

**Access**

- Services: RW
- `arcowl`: RW

**Rules**

- Always safe to delete
- Never backed up
- No guarantees

---

### `/opt/nimbos/storage`

**Purpose:** User-owned, irreplaceable data

Mounted from a separate data disk.

**Access**

- Services: RW (explicit, scoped)
- `arcowl`: RW (admin)
- API/UI: Scoped via services

**Rules**

- Only location for user data
- Snapshotted and backed up
- Services must not mount entire tree unless required

Subdirectories:

```
users/    # per-user data
shared/  # shared documents
media/   # photos, videos, backups
```

---

## Container Volume Mapping Rules

**Allowed**

- `config/` → read-only
- `services/<service>` → RW
- `ai/` → RW (AI only)
- `cache/<service>` → RW
- `storage/<scope>` → RW (explicit)

**Forbidden**

- Writing to `config/`
- Writing to `storage/` root
- Mounting `/opt/nimbos` wholesale
- Anonymous volumes

---

## Backup & Snapshot Scope

| Directory | Backup | Snapshot |
| --------- | ------ | -------- |
| config    | ✔      | ✔        |
| services  | ❌      | optional |
| ai        | ❌      | ❌        |
| logs      | ❌      | ❌        |
| cache     | ❌      | ❌        |
| storage   | ✔      | ✔        |

---

## Status

This document is **authoritative** for Step 1.2 (Directory Contracts). Enforcement is progressive and will be tightened during security hardening stages.

