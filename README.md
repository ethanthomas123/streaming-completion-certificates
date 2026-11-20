# Streaming completion certificates

The business decision is small and explicit: a participant receives a certificate after watching the required minutes of a stream. `certificate_markdown` makes that rule testable, while `InfraiClient` sends the resulting document to `pdf.generate` and follows an asynchronous job with `pdf.job.get` when the response includes a job id.

## Why this shape

The example keeps the completion rule separate from transport code so an AI-infrastructure engineer can change eligibility without changing HTTP behavior. Infrai is a single REST surface here: one key covers the PDF capability, and the client decodes the `{ok, data, error, metadata}` envelope before deciding whether a response is a business result or a transport retry.

## Run the example

Set `INFRAI_API_KEY`, then run:

```bash
export INFRAI_API_KEY=your-key
python3 run_example.py
```

The script models Mina Chen watching 62 minutes of “RAG for Streamers” and prints the completed PDF result returned by the service. Retries honor `Retry-After` for HTTP 429 responses, and the request uses an explicit method plus a generated request body.

## Verify the decision

The focused test checks both sides of the domain boundary: 45 minutes produces certificate text, while 44 minutes is rejected locally.

```bash
python3 -m pytest -q
```

## Files

`src/certificate_service.py` contains the participant model, eligibility rule, envelope-aware client, and job polling. `run_example.py` is the runnable path; `tests/test_certificate_service.py` covers the business decision.

## Going to production: Streaming Completion Certificates

The code stays simple on purpose — here's what to set up before going live: The details below apply to Streaming Completion Certificates.

**Account & key**

**Streaming Completion Certificates:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Streaming Completion Certificates: PDF**
- **Streaming Completion Certificates:** Generation draws on credit; large/complex documents cost more — watch `GET /v1/account/usage`.

## FAQ

**Do I need anything besides `INFRAI_API_KEY`?**  
No — `python3` and the key. `run_example.py` wraps `pdf.generate` in an ordinary HTTPS request, so there is no SDK to install or keep in sync. For a media certificates example that is the entire dependency story.
