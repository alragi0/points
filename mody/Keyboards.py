from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton

start_key = ReplyKeyboardMarkup(
    [
        ["⌯ حذف حساب","⌯ اضافة حساب"],
        ["⌯ تحديث"],
        ["⌯ حساباتي","⌯ تعيين النقاط"],
    ],
    resize_keyboard=True
)

login_key = ReplyKeyboardMarkup(
    [
        ["⌯ تسجيل الدخول"],
    ],
    resize_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    [
        ["⌯ الغاء"],
    ],
    resize_keyboard=True,
)

send_you_contact = ReplyKeyboardMarkup(
    [
        [KeyboardButton('⌯ مشاركة جهة اتصالك', request_contact=True)],
    ],
    resize_keyboard=True,
)
