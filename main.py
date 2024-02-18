import asyncio

from consts import app
from coroutines import update_currency_rates, get_last_update, create_tables


@app.route('/update')
async def update():
    await update_currency_rates()
    return "Currency rates have been updated."


@app.route('/last_update')
async def last_update():
    last_update = await get_last_update()
    if last_update:
        return str(last_update)
    else:
        return "Currency rates have not been updated yet."


if __name__ == '__main__':
    asyncio.run(create_tables())
    app.run(debug=True)
