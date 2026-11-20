
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { getCookie, formatActivityTime } from '../../utils.js';

describe('getCookie', () => {
  beforeEach(() => {
    document.cookie = 'csrftoken=';
  });

  it('returns the value of an existing cookie', () => {
    document.cookie = 'username=testuser';

    expect(getCookie('username')).toBe('testuser');
  });

  it('returns null when the cookie does not exist', () => {
    expect(getCookie('missing')).toBeNull();
  });

  it('preserves equals signs in cookie values', () => {
    document.cookie = 'token=abc=123==';

    expect(getCookie('token')).toBe('abc=123==');
  });

  it('decodes URL-encoded cookie values', () => {
    document.cookie = 'name=John%20Smith';

    expect(getCookie('name')).toBe('John Smith');
  });
});

describe('formatActivityTime', () => {
  it('returns 00:00 when given an empty value', () => {
    expect(formatActivityTime('')).toBe('00:00');
  });

  it('returns 00:00 when given null', () => {
    expect(formatActivityTime(null)).toBe('00:00');
  });

  it('extracts the time from an ISO datetime string', () => {
    expect(formatActivityTime('2026-11-19T14:30:00Z')).toBe('14:30');
  });

  it('returns an existing time in HH:MM format', () => {
    expect(formatActivityTime('09:45:00')).toBe('09:45');
  });

  it('returns 00:00 when an ISO datetime has no time after T', () => {
    expect(formatActivityTime('2026-11-19T')).toBe('00:00');
  });
});
