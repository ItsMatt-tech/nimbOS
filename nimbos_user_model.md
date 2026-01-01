# NimbOS User Model (Headless Identity Layer)

This document describes the **NimbOS user model**, as defined in **Checklist Section 3 (User Identity Model – HEADLESS)**.

It is **authoritative** for all future design, implementation, and documentation decisions related to users, storage, services, and access control.

---

## Design Philosophy

> A NimbOS user is a **logical identity**, not an operating system account.

The user model is intentionally **headless**:
- no UI assumptions
- no API assumptions
- no dependency on Linux UIDs/GIDs

This allows:
- clean OS reinstalls
- container isolation
- future API/UI evolution
- multi-user expansion without data migration

---

## What a NimbOS User Is

A NimbOS user consists of:

- **Stable user ID** (string)
- **Display name** (human-facing)
- **Bound storage root**
- **Declared service access**
- *(Future)* authentication metadata

A user **does not**:
- imply OS login access
- own system state
- infer permissions implicitly

---

## Canonical User Schema (v0)

```yaml
id: arcowl
display_name: Arc Owl
storage_root: /opt/nimbos/storage/users/arcowl
services:
  syncthing: enabled
  immich: enabled
```

### Schema Rules

- `id` is immutable once created
- `id` maps 1:1 to a directory under `storage/users/`
- storage paths never change
- services must explicitly opt in

---

## Relationship to Linux Users

| Concept | Linux User | NimbOS User |
|------|-----------|------------|
| Identity | UID/GID | String ID |
| Purpose | OS access | Data & services |
| Scope | System | Platform |
| Persistence | Lost on reinstall | Survives reinstall |

During early development, the same name may exist in both systems (e.g. `arcowl`), but this coupling is **temporary and non-authoritative**.

---

## User → Storage Mapping

### Canonical Rule

```text
<user_id> → /opt/nimbos/storage/users/<user_id>
```

Example:

```text
arcowl → /opt/nimbos/storage/users/arcowl
```

### Properties

- 1:1 mapping
- Stable and immutable
- Independent of UID/GID
- Never inferred dynamically

---

## Storage Semantics

### User Storage (`users/`)

- Human-facing data
- Owned logically by users
- Backed up and snapshotted
- Services mount **only their assigned users**

### Shared Storage (`shared/`)

- Explicitly collaborative
- Not owned by any single user
- Access must be declared
- Never assumed

### Media Storage (`media/`)

> Media is **service-owned**, not user-owned.

- Opaque blobs managed by services (e.g. Immich)
- No per-user directories at platform level
- User ↔ media association handled internally by services
- Backed up and snapshotted as a whole

This avoids tight coupling between user identity and service internals.

---

## Service Access Rules

Services:
- must declare which users they serve
- receive only explicit mounts
- must not scan or infer users

Forbidden behaviors:
- scanning `users/`
- assuming a default user
- writing outside declared scope

---

## Cross-User Constraints (Locked)

Even on single-user systems:

- no user-to-user writes
- no shared metadata inside user directories
- no admin bypass of user isolation
- no platform-level “super user” concept

These constraints are enforced conceptually now and technically later.

---

## Multi-User Design Assumptions

The following are **locked design assumptions**:

- User IDs never change
- Linux users are implementation details
- Services never infer access
- Media remains service-owned
- Shared data is always opt-in

---

## Known Limitations (Explicit Non-Goals)

The following are intentionally **out of scope** for early NimbOS versions:

- per-file ACLs
- per-user quotas
- per-user encryption at rest
- concurrent multi-user UI

These are future features, not architectural requirements.

---

## Summary

The NimbOS user model provides:

- clean separation of identity and OS
- deterministic storage mapping
- service-safe access boundaries
- future-proof multi-user expansion

All future components (API, UI, services, installer) must conform to this document.

