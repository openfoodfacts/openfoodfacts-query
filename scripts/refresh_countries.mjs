import { writeFileSync } from 'fs';
import stringify from 'json-stable-stringify';

writeFileSync(
  'query/assets/countries.json',
  stringify(
    await (
      await fetch(
        'https://static.openfoodfacts.org/data/taxonomies/countries.json',
      )
    ).json(),
    { space: 2 },
  ),
);
