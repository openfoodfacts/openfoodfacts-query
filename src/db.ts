import postgres from 'postgres';
import { SCHEMA } from './constants';

const sql = postgres({
  host: process.env.POSTGRES_HOST,
  database: process.env.POSTGRES_DB,
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  port: parseInt(process.env.POSTGRES_PORT.split(':').pop()),
});

export default sql;
