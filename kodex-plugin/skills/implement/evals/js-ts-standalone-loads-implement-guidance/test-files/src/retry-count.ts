export function readRetryCount(value: unknown): number {
  return (value as number) || 3;
}
