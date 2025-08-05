import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont
import io

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لطفاً محصول را به صورت «نام | قیمت | توضیحات» ارسال کن.")

async def handle_product_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "|" in text:
        name, price, description = map(str.strip, text.split("|", 2))
        img = Image.new('RGB', (600, 400), color='white')
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text((30, 30), f"{name}\n\n{price} تومان\n\n{description}", fill="black", font=font)
        byte_io = io.BytesIO()
        img.save(byte_io, 'PNG')
        byte_io.seek(0)
        await update.message.reply_photo(photo=byte_io)
    else:
        await update.message.reply_text("❌ فرمت اشتباه است. لطفاً پیام را به صورت «نام | قیمت | توضیحات» ارسال کن.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_product_message))
    print("🤖 ربات در حال اجراست...")
    app.run_polling()
