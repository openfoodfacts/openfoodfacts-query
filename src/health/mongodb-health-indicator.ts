import { Injectable } from '@nestjs/common';
import {
  HealthIndicator,
  HealthIndicatorResult,
  HealthCheckError,
} from '@nestjs/terminus';
import { MongoClient } from 'mongodb';

@Injectable()
export class MongodbHealthIndicator extends HealthIndicator {
  NAME = 'mongodb';
  async isHealthy(): Promise<HealthIndicatorResult> {
    try {
      const client = new MongoClient(process.env.MONGO_URI, {
        serverSelectionTimeoutMS: 1000,
        connectTimeoutMS: 1000,
        socketTimeoutMS: 1000,
      });
      await client.connect();
      const db = client.db('off');
      const products = db.collection('products');
      const cursor = products.find({}, { projection: { code: 1 } });
      await cursor.next();
      await cursor.close();
      await client.close();

      return this.getStatus(this.NAME, true);
    } catch (e) {
      throw new HealthCheckError(
        'MongoDB check failed',
        this.getStatus(this.NAME, false, e),
      );
    }
  }
}
