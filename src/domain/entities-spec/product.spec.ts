import { normalizeCode } from '../entities/product';

describe('normalizeCode', () => {
  it('should normalize codes', () => {
    expect(normalizeCode('0000a')).toBe('0000a');
    expect(normalizeCode('000000000000001')).toBe('00000001');
    expect(normalizeCode('1234567890')).toBe('0001234567890');
    expect(normalizeCode('12345678901234')).toBe('12345678901234');
  });
});
