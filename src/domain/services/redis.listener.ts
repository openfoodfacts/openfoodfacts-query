import { Injectable, Logger } from '@nestjs/common';
import { createClient, commandOptions } from 'redis';
import { MessagesService } from './messages.service';
import { SettingsService } from './settings.service';

@Injectable()
export class RedisListener {
  private logger = new Logger(RedisListener.name);
  private client: any; // Don't strongly type here is it is really verbose

  constructor(
    private readonly settings: SettingsService,
    private readonly messages: MessagesService,
  ) {}

  async startRedisConsumer() {
    const redisUrl = this.settings.getRedisUrl();
    if (!redisUrl) return;
    this.client = createClient({ url: redisUrl });
    this.client.on('error', (err: any) => this.logger.error(err));
    await this.client.connect();
    this.receiveMessages();
  }

  async stopRedisConsumer() {
    if (this.client && this.client.isOpen) await this.client.quit();
  }

  async receiveMessages() {
    const lastMessageId = await this.settings.getLastMessageId();
    if (!this.client.isOpen) return;
    try {
      const keys = await this.client.xRead(
        commandOptions({
          isolated: true,
        }),
        [
          // XREAD can read from multiple streams, starting at a
          // different ID for each...
          {
            key: 'product_updates_off',
            id: lastMessageId,
          },
        ],
        {
          // Read 1000 entry at a time, block for 5 seconds if there are none.
          COUNT: 1000,
          BLOCK: 5000,
        },
      );
      if (keys?.length) {
        const messages = keys[0].messages;
        if (messages?.length) {
          /** Message looks like this:
                {
                  code: "0850026029062",
                  flavor: "off",
                  user_id: "stephane",
                  action: "updated",
                  comment: "Modification : Remove changes",
                  diffs: "{\"fields\":{\"change\":[\"categories\"],\"delete\":[\"product_name\",\"product_name_es\"]}}",
                }
               */
          await this.processMessages(messages);
          await this.settings.setLastMessageId(
            messages[messages.length - 1].id,
          );
        }
      }
      setTimeout(() => {
        this.receiveMessages();
      }, 0);
    } catch (e) {
      this.logger.error(e);
      // Try again in 10 seconds
      setTimeout(() => {
        this.receiveMessages();
      }, 10000);
    }
  }

  async processMessages(messages: any[]) {
    // Fix JSON properties on each message to be objects rather than strings
    for (const event of messages) {
      if (event.message.diffs)
        event.message.diffs = JSON.parse(event.message.diffs);
    }
    await this.messages.create(messages);
  }

  async pauseAndRun(action: () => Promise<void>) {
    // Pause redis while doing a scheduled import
    await this.stopRedisConsumer();

    try {
      await action();
    } finally {
      // Resume redis after import
      await this.startRedisConsumer();
    }
  }
}
