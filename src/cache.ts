import NodeCache from "node-cache";

// TTL in seconds; HEALTH_CHECK_INTERVAL env var controls health cache refresh
const TTL = parseInt(process.env.HEALTH_CHECK_INTERVAL || "60", 10);

const cache = new NodeCache({ stdTTL: TTL });

export function get<T>(key: string): T | undefined {
  return cache.get<T>(key);
}

export function set<T>(key: string, value: T): void {
  cache.set(key, value);
}

export function del(key: string): void {
  cache.del(key);
}
