import { Entity, PrimaryKey, Property } from '@mikro-orm/core';
import sql from '../../db';
import { readdirSync, readFileSync } from 'fs';

@Entity()
export class Country {
  @PrimaryKey({ columnType: 'serial' })
  id: number;

  @Property({ unique: true })
  code?: string;

  @Property({ unique: true })
  tag: string;
}

export async function addAllCountries() {
  const countries: [key: string, country: any] = JSON.parse(
    readFileSync(`${__dirname}/../../assets/countries.json`, {
      encoding: 'utf-8',
    }),
  );

  const countryCodes = [];

  for (const [countryId, country] of Object.entries(countries)) {
    countryCodes.push([
      countryId,
      country.country_code_2?.en.toLowerCase() ?? null,
    ]);
  }

  await sql`INSERT INTO country (tag, code) SELECT tag, code 
      FROM (values ${sql(countryCodes)}) as source (tag, code)
      WHERE NOT EXISTS (SELECT * FROM country WHERE tag = source.tag AND code = source.code)
      ON CONFLICT (tag) 
      DO UPDATE SET code = EXCLUDED.code`;
}
