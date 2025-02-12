import { Entity, PrimaryKey, Property } from '@mikro-orm/core';

@Entity()
export class Country {
  @PrimaryKey({ columnType: 'serial' })
  id: number;

  // The following fields map directly to Product fields
  @Property({ unique: true })
  code: string;
}
