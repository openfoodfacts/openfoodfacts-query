import { randomBytes } from 'crypto';

export function randomCode() {
  return 'TEST-' + randomBytes(20).toString('base64');
}
