import { Entity, PrimaryKey, Property } from '@mikro-orm/core';

@Entity()
export class Settings {
  @PrimaryKey()
  id = 1;

  @Property({ columnType: 'timestamptz' })
  lastModified?: Date;

  @Property()
  lastMessageId?: string;
}
