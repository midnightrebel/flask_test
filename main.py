import asyncio

from flask import render_template

from consts import app
from coroutines import create_tables, get_last_update, update_currency_rates


@app.route("/update", methods=["GET"])
async def update():
    await update_currency_rates()
    return "Currency rates have been updated."


@app.route("/last_update", methods=["GET"])
async def last_update():
    last_update = await get_last_update()
    if last_update:
        return str(last_update)
    else:
        return "Currency rates have not been updated yet."


@app.route("/currency_interface", methods=["GET"])
def currency_interface():
    return render_template("index.html")


if __name__ == "__main__":
    asyncio.run(create_tables())
    app.run(debug=True)
