export function readRetryCount(value: number | undefined): number {
  return value ?? 3;
}
