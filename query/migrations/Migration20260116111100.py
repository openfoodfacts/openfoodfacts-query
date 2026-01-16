from query.config import config_settings
from query.tables import product_update_event

async def up(transaction):
    # anonymize ip addresses in the db by computing a HMAC hexdigest
    # we use a good enough regexp to match ip but avoid re-encode already encoded values
    await transaction.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
    await transaction.execute(
        """UPDATE product_update_event
        SET message = jsonb_set(
            message, ARRAY['ip'],
            to_jsonb(encode(hmac(message->>'ip', $1, 'sha256'), 'hex')),
            FALSE)
        WHERE
            message->>'ip' IS NOT NULL AND
            message->>'ip' SIMILAR TO '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[0-9a-fA-F]+:[[0-9a-fA-F:]+)';
        """,
        config_settings.APP_SECRET_KEY,
    )
