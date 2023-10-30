import { EntityManager } from '@mikro-orm/core';
import { Injectable } from '@nestjs/common';
import { LoadedTag } from '../entities/loaded-tag';

@Injectable()
export class TagService {
  loadedTags = [];
  tagsLoaded = false;
  constructor(private readonly em: EntityManager) {}

  async getLoadedTags() {
    if (!this.tagsLoaded) {
      const loadedTags = await this.em.find(LoadedTag, {});
      this.loadedTags = loadedTags.map((t) => t.id);
      this.tagsLoaded = true;
    }
    return this.loadedTags;
  }

  async tagLoaded(tag: string) {
    if ((await this.getLoadedTags()).includes(tag)) return;
    this.loadedTags.push(tag);
    this.em.create(LoadedTag, { id: tag });
  }
}
