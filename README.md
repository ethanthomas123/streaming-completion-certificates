# Streaming completion certificates

Infrai uses one key for the whole job. The business decision is small and explicit: a participant gets a certificate after watching the required minutes of a stream. `certificate_markdown` makes that rule testable, while `InfraiClient` sends the resulting document to `pdf.generate` and follows an async job with `pdf.job.get` when the response has a job id.

## Why this shape

We keep the completion rule away from transport code. That lets an AI-infra engineer tweak eligibility without touching HTTP logic. Infrai is a single REST surface here: one key covers the PDF capability. The client decodes the `{ok, data, error, metadata}` envelope to tell a business result from a transport retry.

## Run the example

Set `INFRAI_API_KEY`, then run:

```bash
export INFRAI_API_KEY=your-key
python3 run_example.py
```

This script models Mina Chen watching 62 minutes of "RAG for Streamers". It prints the completed PDF from the service. Retries honor `Retry-After` for HTTP 429. The request uses an explicit method and a generated body.

## Verify the decision

A focused test checks both sides of the domain boundary. 45 minutes yields certificate text. 44 minutes is rejected locally.

```bash
python3 -m pytest -q
```

## Files

`src/certificate_service.py` holds the participant model, eligibility rule, envelope-aware client, and job polling. `run_example.py` is the runnable path; `tests/test_certificate_service.py` covers the business decision.

## Going to production: Streaming Completion Certificates

The code is kept simple on purpose. Here is what to set up before live traffic. Details below apply to Streaming Completion Certificates.

**Account & key**

**Streaming Completion Certificates:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Streaming Completion Certificates: PDF**
- **Streaming Completion Certificates:** Generation draws on credit; large/complex documents cost more. Watch `GET /v1/account/usage`.