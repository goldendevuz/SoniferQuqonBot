import logging
import sys
import traceback
from pathlib import Path
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BufferedInputFile
from redis.asyncio import Redis
import config
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from fastapi import FastAPI, Request, status, HTTPException
from db import create_db_and_tables
import uvicorn
from fastapi.responses import JSONResponse
from enums.cryptocurrency import Cryptocurrency
from processing.processing import processing_router
from repositories.button_media import ButtonMediaRepository
from services.notification import NotificationService
from services.wallet import WalletService

from sqladmin import Admin, ModelView
from db import engine
from models import Buy, BuyItem, Cart, CartItem, Category, Coupon, Deposit, Item, Payment, Subcategory, User

redis = Redis(host=config.REDIS_HOST, password=config.REDIS_PASSWORD)
bot = Bot(config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=RedisStorage(redis))
app = FastAPI()
app.include_router(processing_router)


@app.post(config.WEBHOOK_PATH)
async def webhook(request: Request):
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret_token != config.WEBHOOK_SECRET_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    try:
        update_data = await request.json()
        await dp.feed_webhook_update(bot, update_data)
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return {"status": "error"}, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    await bot.set_webhook(
        url=config.WEBHOOK_URL,
        secret_token=config.WEBHOOK_SECRET_TOKEN
    )
    static = Path("static")
    if static.exists() is False:
        static.mkdir()
    me = await bot.get_me()
    photos = await bot.get_user_profile_photos(me.id)
    bot_photo_id = photos.photos[0][-1].file_id
    with open("static/no_image.jpeg", "w") as f:
        f.write(bot_photo_id)
    await ButtonMediaRepository.init_buttons_media()
    if config.CRYPTO_FORWARDING_MODE:
        for cryptocurrency in Cryptocurrency:
            is_addr_valid = WalletService.validate_withdrawal_address(
                cryptocurrency.get_forwarding_address(),
                cryptocurrency
            )
            if is_addr_valid is False:
                logging.debug(
                    f"Your withdrawal address for {cryptocurrency.name} cryptocurrency is not valid!"
                )
                sys.exit()
    for admin in config.ADMIN_ID_LIST:
        try:
            await bot.send_message(admin, 'Bot is working')
        except Exception as e:
            logging.warning(e)


@app.on_event("shutdown")
async def on_shutdown():
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    logging.warning('Bye!')


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    traceback_str = traceback.format_exc()
    admin_notification = (
        f"Critical error caused by {exc}\n\n"
        f"Stack trace:\n{traceback_str}"
    )
    if len(admin_notification) > 4096:
        byte_array = bytearray(admin_notification, 'utf-8')
        admin_notification = BufferedInputFile(byte_array, "exception.txt")
    await NotificationService.send_to_admins(admin_notification, None)
    return JSONResponse(
        status_code=500,
        content={"message": f"An error occurred: {str(exc)}"},
    )


def main() -> None:
    uvicorn.run(app, host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)

admin = Admin(app, engine)

# Har bir model uchun alohida ModelView yaratish
class BuyAdmin(ModelView, model=Buy):
    column_list = [c.name for c in Buy.__table__.columns]

class BuyItemAdmin(ModelView, model=BuyItem):
    column_list = [c.name for c in BuyItem.__table__.columns]

class CartAdmin(ModelView, model=Cart):
    column_list = [c.name for c in Cart.__table__.columns]

class CartItemAdmin(ModelView, model=CartItem):
    column_list = [c.name for c in CartItem.__table__.columns]

class CategoryAdmin(ModelView, model=Category):
    column_list = [c.name for c in Category.__table__.columns]

class CouponAdmin(ModelView, model=Coupon):
    column_list = [c.name for c in Coupon.__table__.columns]

class DepositAdmin(ModelView, model=Deposit):
    column_list = [c.name for c in Deposit.__table__.columns]

class ItemAdmin(ModelView, model=Item):
    column_list = [c.name for c in Item.__table__.columns]

class PaymentAdmin(ModelView, model=Payment):
    column_list = [c.name for c in Payment.__table__.columns]

class SubcategoryAdmin(ModelView, model=Subcategory):
    column_list = [c.name for c in Subcategory.__table__.columns]

class UserAdmin(ModelView, model=User):
    column_list = [c.name for c in User.__table__.columns]

# Admin panelga qo‘shish
admin.add_view(BuyAdmin)
admin.add_view(BuyItemAdmin)
admin.add_view(CartAdmin)
admin.add_view(CartItemAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(CouponAdmin)
admin.add_view(DepositAdmin)
admin.add_view(ItemAdmin)
admin.add_view(PaymentAdmin)
admin.add_view(SubcategoryAdmin)
admin.add_view(UserAdmin)
