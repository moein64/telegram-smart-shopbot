1  import os
2  from telegram import Update
3  from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
4  from PIL import Image, ImageDraw, ImageFont
5  import io
6  
7  TOKEN = os.getenv("BOT_TOKEN")
8  
9  async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
10     await update.message.reply_text("سلام! نام محصول | قیمت | توضیح را بفرست تا پوستر ساخته شود.")
11 
12 async def handle_product_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
13     text = update.message.text
14     if "|" in text:
15         name, price, description = map(str.strip, text.split("|", 2))
16         img = Image.new('RGB', (600, 400), color=(255, 255, 255))
17         draw = ImageDraw.Draw(img)
18         font = ImageFont.load_default()
19         draw.text((30, 30), f"{name}\nقیمت: {price} تومان\n{description}", font=font, fill=(0, 0, 0))
20         byte_io = io.BytesIO()
21         img.save(byte_io, 'PNG')
22         byte_io.seek(0)
23         await update.message.reply_photo(photo=byte_io, caption=f"{name}\nقیمت: {price} تومان\n{description}")
24     else:
25         await update.message.reply_text("لطفاً پیام را به صورت: نام محصول | قیمت | توضیح بفرستید.")
26 
27 if __name__ == "__main__":
28     app = ApplicationBuilder().token(TOKEN).build()
29     app.add_handler(CommandHandler("start", start))
30     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_product_message))
31     print("🤖 ربات در حال اجراست...")
32     app.run_polling()
