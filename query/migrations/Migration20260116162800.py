async def up(transaction):
    # remove ip addresses from message as they will be exposed
    await transaction.execute(
        """UPDATE product_update_event
        SET message = message - 'ip'
        WHERE
            message->>'ip' IS NOT NULL
        """
    )
