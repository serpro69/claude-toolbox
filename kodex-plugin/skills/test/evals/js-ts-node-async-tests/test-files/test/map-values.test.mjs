import assert from 'node:assert/strict';
import test from 'node:test';
import {mapValues} from '../src/map-values.mjs';

test('maps values', () => {
  mapValues([1, 2], async (value) => value * 2).then((result) => {
    assert.deepEqual(result, [2, 4]);
  });
});
