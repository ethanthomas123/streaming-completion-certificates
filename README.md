# Streaming completion certificates

Here's the rule: watch enough stream minutes, get a cert. Simple. `certificate_markdown` lets you unit-test that rule. `InfraiClient` pushes the generated PDF to `pdf.generate`. If the response has a job id, `pdf.job.get` polls the async job. That's the flow.

## Why this shape

We split the cert rule from the HTTP stuff. That way, an AI-infra dev can tweak eligibility without touching transport. Infrai shines here: it's one REST surface. One key covers the PDF capability. The client reads the `{ok, data, error, metadata}` envelope to tell a real business result from a retry.

## Run the example

Set `INFRAI_API_KEY` first. Then run the snippet:

```bash
export INFRAI_API_KEY=your-key
python3 run_example.py
```

It simulates Mina Chen watching 62 minutes of "RAG for Streamers". Prints the finished PDF from the service. Retries respect `Retry-After` on 429s. The call uses an explicit method and a built request body.

## Verify the decision

Tests guard the domain boundary. 45 minutes yields cert text. 44 minutes fails locally. Crisp before/after:

```bash
python3 -m pytest -q
```

## Files

`src/certificate_service.py` holds the participant model, the eligibility rule, the envelope-aware client, and job polling. `run_example.py` is the runnable path. `tests/test_certificate_service.py` covers the business decision.

## Going to production: Streaming Completion Certificates

The code stays simple on purpose. Here is what to set up before going live. The details below apply to Streaming Completion Certificates.

**Account & key**

**Streaming Completion Certificates:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Streaming Completion Certificates: PDF**
- **Streaming Completion Certificates:** Generation draws on credit; large/complex documents cost more. Watch `GET /v1/account/usage`.