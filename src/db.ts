import postgres from 'postgres';

const sql = postgres({
  host: process.env.POSTGRES_HOST.split(':')[0],
  database: process.env.POSTGRES_DB,
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  port: parseInt(process.env.POSTGRES_HOST.split(':')?.[1] ?? '5432'),
});

export default sql;
