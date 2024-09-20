from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler
import os

canquest = '' # Telegram Bot Token
logdosya = '' # Log file with accounts
kullanilanlar = '' # File name for used accounts (It's not important, you can write random.)


if not os.path.exists(kullanilanlar):
    os.makedirs(kullanilanlar)

async def start(update: Update, context):
    await update.message.reply_text('Bot çalışıyor!')

async def log(update: Update, context):
    if len(context.args) < 2:
        await update.message.reply_text('Lütfen site ismi ve adet sayısını girin. Örnek: /log site.com 2')
        return

    site = context.args[0]
    try:
        logsayi = int(context.args[1])
    except ValueError:
        await update.message.reply_text('Adet sayısı geçersiz, lütfen bir sayı girin.')
        return

    if not os.path.isfile(logdosya):
        await update.message.reply_text('TXT dosyası bulunamadı.')
        return

    sonuclar = []
    kalan_satirlar = []

    # TXT dosyasını oku
    with open(logdosya, 'r', encoding='utf-8') as file:
        satirlar = file.readlines()
        for satir in satirlar:
            if site in satir and len(sonuclar) < logsayi:
                sonuclar.append(satir.strip())
            else:
                kalan_satirlar.append(satir)


    if len(sonuclar) < logsayi:
        await update.message.reply_text(f'Yeterli hesap yok. Toplamda {len(sonuclar)} hesap bulundu.')
        return

    sonuc_dosya = f'{kullanilanlar}/{site}.txt'
    with open(sonuc_dosya, 'w', encoding='utf-8') as file:
        for sonuc in sonuclar:
            file.write(sonuc + '\n')


    with open(logdosya, 'w', encoding='utf-8') as file:
        for satir in kalan_satirlar:
            file.write(satir)


    with open(sonuc_dosya, 'rb') as file:
        await update.message.reply_document(document=InputFile(file), filename=f'{site}.txt')

async def test(update: Update, context):
    await update.message.reply_text('Komutlar çalışıyor!')

if __name__ == '__main__':
    app = ApplicationBuilder().token(canquest).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('log', log))
    app.add_handler(CommandHandler('test', test))

    print('Bot çalışmaya başladı.')
    app.run_polling()

    # Made by Canquest. If you want to share you need to give credit. Ex: "Credit: https://github.com/Yan-Jobs"
