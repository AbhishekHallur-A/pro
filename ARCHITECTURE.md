# High-Level Architecture (Instagram + Twitter Hybrid)

This document describes a production-ready, scalable architecture for a social media app that blends visual sharing with real-time conversation. It is designed to start as a modular monolith and evolve into microservices.

---

## 1) Client–Server Flow

1. **Client apps** (Web + Mobile) send requests to the API Gateway.
2. **API Gateway** authenticates, rate-limits, and routes requests.
3. **API layer** validates input, executes use cases, and writes to the database.
4. **Async events** are published for feeds, notifications, and media processing.
5. **Clients** receive real-time updates via WebSockets or push notifications.

---

## 2) API Layer

**Responsibilities**
- Authentication (JWT/OAuth2) and authorization.
- Request validation + DTO mapping.
- Business use cases (posts, comments, likes, follows).
- Orchestration of async tasks (feed updates, notifications, media processing).

**Entry points**
- REST/JSON for standard requests.
- WebSockets for real-time events.

**Structure (clean architecture)**
- **Domain**: entities + business rules.
- **Use cases**: application services.
- **Interfaces**: controllers + API handlers.
- **Adapters**: database, cache, external services.
- **Infrastructure**: framework + config.

---

## 3) Database Layer

**Primary DB: PostgreSQL**
- Users, posts, comments, likes, follows, notifications.
- Strong relational integrity and indexing.

**Search Index: OpenSearch**
- Search across users, hashtags, posts.

**Cache: Redis**
- Feed caching, rate limit counters, session storage.

---

## 4) Media Storage

- Object storage (S3/GCS) for images/video.
- CDN (CloudFront/Fastly) for global delivery.
- Media processing pipeline (resize, transcode, thumbnails) using async workers.

---

## 5) Notification System

- **Events** are published to a message bus (SQS/SNS/Kafka).
- **Notification service** consumes events and sends:
  - Push notifications (APNs/FCM)
  - Email notifications (SES/SendGrid)
  - In-app notifications (stored in DB, delivered via WebSockets)

---

## 6) Caching

- Redis for:
  - Home feed cache (hot users).
  - Post/like counters.
  - Rate limit tokens.
- CDN edge caching for media and static assets.

---

## 7) Rate Limiting

- API Gateway enforces per-IP and per-user throttles.
- Redis token bucket or leaky bucket for fine-grained limits.
- Enhanced protection for authentication and content creation endpoints.

---

## 8) Future Microservices Readiness

Start as a modular monolith, split into services as traffic grows:
- **Auth & Identity**
- **Profiles**
- **Content (posts/comments/likes)**
- **Social Graph**
- **Feed & Ranking**
- **Media Processing**
- **Notifications**
- **Messaging**

Use event-driven boundaries so services can be extracted with minimal refactoring.

---

## 9) Clean Architecture Diagram Description

```
Clients (Web/Mobile)
   ↓ HTTPS/WebSocket
API Gateway (Auth + Rate Limit + Routing)
   ↓
API Layer (Controllers → Use Cases → Domain)
   ↓                    ↘
Database Layer (Postgres)  Event Bus (Kafka/SQS)
   ↓                           ↓
Search (OpenSearch)        Async Workers
   ↓                           ↓
Cache (Redis)          Notifications + Media Processing
   ↓                           ↓
CDN + Object Storage (S3/GCS)   Push/Email/WebSocket
```

**Notes**
- The API layer uses clean architecture to keep domain logic isolated.
- Async workers scale independently for feed, notifications, and media tasks.
- Each box can later become a dedicated microservice.
