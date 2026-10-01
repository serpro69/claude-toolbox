export async function mapValues(values, transform) {
  return Promise.all(values.map((value) => transform(value)));
}
