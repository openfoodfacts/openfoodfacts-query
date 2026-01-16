from query.config import config_settings

async def up(transaction):
    # anonymize ip addresses in the db by computing a HMAC hexdigest
    # we use a good enough regexp to match ip but avoid re-encode already encoded values
    await transaction.execute(
        """UPDATE product_update_event
        SET message = message - 'ip'
        WHERE
            message->>'ip' IS NOT NULL
        """
    )