import { Entity, PrimaryKey } from '@mikro-orm/core';

@Entity()
export class LoadedTag {
  @PrimaryKey()
  id: string;
}
