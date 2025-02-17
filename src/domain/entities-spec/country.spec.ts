import sql from '../../db';
import { addAllCountries } from '../entities/country';

describe('addAllCountries', () => {
  it('should update the codes of existing countries', async () => {
    await sql`INSERT INTO country (tag) VALUES ('en:france')`;
    await addAllCountries();
    const countries = await sql`SELECT * FROM country`;
    expect(countries.length).toBeGreaterThan(100);
    const fr = countries.find((c) => c.tag === 'en:france');
    expect(fr).toBeTruthy();
    expect(fr.code).toBe('fr');
  });
});
