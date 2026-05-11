import { test, expect } from 'vitest';
import { translations } from './i18n/translations';

test('contains 3 languages', () => {
  expect(Object.keys(translations)).toEqual(['hy','ru','en']);
});
