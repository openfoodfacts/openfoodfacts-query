import { Injectable } from '@nestjs/common';
import sql from '../../db';

@Injectable()
export class SettingsService {
  async updateSetting(settings: any) {
    const result = await sql`UPDATE settings SET ${sql(settings)}`;
    if (!result.count) {
      await sql`INSERT INTO settings ${sql(settings)}`;
    }
  }

  async getLastModified() {
    return (await sql`SELECT last_modified FROM settings`)[0].last_modified;
  }

  async setLastModified(lastModified: Date) {
    await this.updateSetting({ last_modified: lastModified });
  }

  async getLastMessageId() {
    return (
      (await sql`SELECT last_message_id FROM settings`)[0].last_message_id ||
      '$'
    );
  }

  async setLastMessageId(messageId: string) {
    await this.updateSetting({ last_message_id: messageId });
  }

  getRedisUrl() {
    return process.env.REDIS_URL;
  }
}
