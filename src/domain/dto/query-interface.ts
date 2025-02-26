type NullExpression = [null, []];
type Value = NonNullable<string | number>;
interface Expression {
  $in?: Array<Value> | NullExpression;
  $nin?: Array<Value> | NullExpression;
  $exists?: true;
  $ne?: Value | [];
  $all?: Array<Value>;
}
type ValueOrExpression = Value | Expression;
interface BaseFilter {
  [tag: string]: ValueOrExpression;
}

export interface Filter {
  $and?: Array<BaseFilter>;
  // Note we don't support Array<BaseFilter> for anything other than $and
  [tag: string]: Array<BaseFilter> | ValueOrExpression;
}

type Sort = Array<[string, 1 | -1]>;

export interface FindQuery {
  filter: Filter;
  projection: { [key: string]: 1 | 0 };
  sort: Sort;
  limit: number;
  skip: number;
}

type AggregateMatch = { $match: Filter };

type AggregateGroup = { $group: { _id: string } };

type AggregateGroupQuery = Array<
  | AggregateMatch
  | AggregateGroup
  | { $sort: Sort }
  | { $limit: number }
  | { $skip: number }
>;

type AggregateCountQuery = Array<
  AggregateMatch | AggregateGroup | { $count: 1 }
>;

export type AggregateQuery = AggregateGroupQuery | AggregateCountQuery;
