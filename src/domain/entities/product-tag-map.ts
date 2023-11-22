export class ProductTagMap {
    static MAPPED_TAGS: { [tag: string] : any; } = {};
    static mapTag(name, entityClass) {
        this.MAPPED_TAGS[name] = entityClass;
    }
}

