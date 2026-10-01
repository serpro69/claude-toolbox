export async function mapValues(values, transform) {
  return values.map(async (value) => transform(value));
}
