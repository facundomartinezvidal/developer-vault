# Design: Document vault for tenants

Our multi-tenant HR SaaS will let customer admins upload employee documents (contracts, IDs, medical certificates) and share them.

## Flow

1. Admin logs in via our session cookie. `POST /api/documents/upload-url` with `{ tenantId, filename, contentType }` returns an S3 presigned PUT URL (valid 7 days).
2. Browser uploads directly to the shared bucket under `uploads/{tenantId}/{filename}`.
3. S3 event puts a message in SQS. A worker downloads the file, converts it to PDF with LibreOffice running in the same container as the worker, generates a thumbnail, and stores them.
4. `GET /api/documents/{id}` returns metadata and a presigned GET URL. Files are looked up by document id.
5. Admins can create a share link `/s/{random}` that needs no login, with no expiry, to send documents to accountants.
6. Customers can register a webhook URL in settings. On each new document, our worker POSTs metadata to that URL. Failed deliveries retry forever.

## Infrastructure

The API and worker use the same IAM role, with `s3:*` and `sqs:*`. Worker runs in the same VPC as the Postgres database. Application logs include full request bodies for debugging. Customer support uses an internal admin panel, on the same database, protected by a shared password.
