# -*- coding: utf-8 -*-
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# ============================================================
# 1) YOUR SETTINGS  (change these two lines)
# ============================================================
import os

TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

# ============================================================
# 2) ALL BOT TEXTS (edit the Amharic here, keep the quote marks)
# ============================================================

# --- Start menu ---
WELCOME = "እንኳን ወደ SmartStudy Tutors በደህና መጡ! እባክዎ ይምረጡ፦"
BTN_PARENT = "ወላጅ ነኝ"
BTN_TUTOR = "አስጠኚ ነኝ"

# --- Parent questions ---
P_Q_GRADE = "ልጅዎ የስንተኛ ክፍል ተማሪ ነው? (ምሳሌ፦ 8ኛ ክፍል)"
P_Q_SUBJECT = "የትኛውን ትምህርት ያስፈልገዋል? (ምሳሌ፦ ሂሳብ)"
P_Q_PLACE = "የሚኖሩት በየትኛው አካባቢ ነው?"
P_Q_TIME = "የትኞቹ ቀናት እና ሰዓታት ይመቹዎታል? (ምሳሌ፦ ሰኞ፣ ረቡዕ እና አርብ ከሰዓት በኋላ)"
P_Q_PHONE = "የመጨረሻ ጥያቄ፦ በየትኛው ስልክ ቁጥር ልንደውልልዎ እንችላለን?"
P_THANKS = "እናመሰግናለን! ጥያቄዎን ተቀብለናል፤ በቅርቡ እንደውልልዎታለን።"

# --- Tutor questions ---
T_Q_NAME = "በጣም ጥሩ! ሙሉ ስምዎን ይንገሩን።"
T_Q_SUBJECTS = "የትኞቹን ትምህርቶች ማስተማር ይችላሉ? (ምሳሌ፦ ሂሳብ፣ ፊዚክስ)"
T_Q_GRADES = "የትኞቹን ክፍሎች ማስተማር ይችላሉ? (ምሳሌ፦ ከ5ኛ እስከ 10ኛ ክፍል)"
T_Q_AREA = "የሚኖሩት በየትኛው አካባቢ ነው? በኦንላይን ማስተማርም ይችላሉ?"
T_Q_PHONE = "የመጨረሻ ጥያቄ፦ በየትኛው ስልክ ቁጥር ልንደውልልዎ እንችላለን?"
T_THANKS = "እናመሰግናለን! መረጃዎን ተቀብለናል፤ የሚመጥን ተማሪ ሲገኝ እናገናኝዎታለን።"

# --- Other ---
CANCELLED = "ተሰርዟል። እንደገና ለመጀመር /start ይላኩ።"
YOUR_ID = "የእርስዎ መለያ ቁጥር፦ "

# --- Messages that arrive to YOU (the admin) ---
A_PARENT_TITLE = "አዲስ የወላጅ ጥያቄ"
A_TUTOR_TITLE = "አዲስ የአስጠኚ ምዝገባ"
L_GRADE = "ክፍል"
L_SUBJECT = "ትምህርት"
L_PLACE = "አካባቢ"
L_TIME = "ሰዓት"
L_PHONE = "ስልክ"
L_NAME = "ስም"
L_SUBJECTS = "ትምህርቶች"
L_GRADES = "ክፍሎች"
L_TELEGRAM = "ቴሌግራም"

# ============================================================
# 3) THE BOT LOGIC (you normally don't need to change this)
# ============================================================

P_GRADE, P_SUBJECT, P_PLACE, P_TIME, P_PHONE = range(5)
T_NAME, T_SUBJECTS, T_GRADES, T_AREA, T_PHONE = range(5, 10)

TEXT = filters.TEXT & ~filters.COMMAND


def who(user):
    handle = f"@{user.username}" if user.username else "-"
    return f"{L_TELEGRAM}: {user.full_name} ({handle})"


# ---------- MENU ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(BTN_PARENT, callback_data="parent")],
        [InlineKeyboardButton(BTN_TUTOR, callback_data="tutor")],
    ]
    await update.message.reply_text(
        WELCOME, reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(YOUR_ID + str(update.effective_user.id))


# ---------- PARENT FORM ----------
async def parent_begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(P_Q_GRADE)
    return P_GRADE


async def p_grade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["grade"] = update.message.text
    await update.message.reply_text(P_Q_SUBJECT)
    return P_SUBJECT


async def p_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["subject"] = update.message.text
    await update.message.reply_text(P_Q_PLACE)
    return P_PLACE


async def p_place(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["place"] = update.message.text
    await update.message.reply_text(P_Q_TIME)
    return P_TIME


async def p_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["time"] = update.message.text
    await update.message.reply_text(P_Q_PHONE)
    return P_PHONE


async def p_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    d = context.user_data
    d["phone"] = update.message.text
    summary = (
        f"{A_PARENT_TITLE}\n\n"
        f"{L_GRADE}: {d['grade']}\n"
        f"{L_SUBJECT}: {d['subject']}\n"
        f"{L_PLACE}: {d['place']}\n"
        f"{L_TIME}: {d['time']}\n"
        f"{L_PHONE}: {d['phone']}\n"
        f"{who(update.effective_user)}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=summary)
    await update.message.reply_text(P_THANKS)
    return ConversationHandler.END


# ---------- TUTOR FORM ----------
async def tutor_begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(T_Q_NAME)
    return T_NAME


async def t_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(T_Q_SUBJECTS)
    return T_SUBJECTS


async def t_subjects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["subjects"] = update.message.text
    await update.message.reply_text(T_Q_GRADES)
    return T_GRADES


async def t_grades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["grades"] = update.message.text
    await update.message.reply_text(T_Q_AREA)
    return T_AREA


async def t_area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["area"] = update.message.text
    await update.message.reply_text(T_Q_PHONE)
    return T_PHONE


async def t_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    d = context.user_data
    d["phone"] = update.message.text
    summary = (
        f"{A_TUTOR_TITLE}\n\n"
        f"{L_NAME}: {d['name']}\n"
        f"{L_SUBJECTS}: {d['subjects']}\n"
        f"{L_GRADES}: {d['grades']}\n"
        f"{L_PLACE}: {d['area']}\n"
        f"{L_PHONE}: {d['phone']}\n"
        f"{who(update.effective_user)}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=summary)
    await update.message.reply_text(T_THANKS)
    return ConversationHandler.END


# ---------- CANCEL ----------
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(CANCELLED)
    return ConversationHandler.END


# ---------- CONNECT EVERYTHING ----------
app = ApplicationBuilder().token(TOKEN).build()

parent_form = ConversationHandler(
    entry_points=[CallbackQueryHandler(parent_begin, pattern="^parent$")],
    states={
        P_GRADE: [MessageHandler(TEXT, p_grade)],
        P_SUBJECT: [MessageHandler(TEXT, p_subject)],
        P_PLACE: [MessageHandler(TEXT, p_place)],
        P_TIME: [MessageHandler(TEXT, p_time)],
        P_PHONE: [MessageHandler(TEXT, p_phone)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

tutor_form = ConversationHandler(
    entry_points=[CallbackQueryHandler(tutor_begin, pattern="^tutor$")],
    states={
        T_NAME: [MessageHandler(TEXT, t_name)],
        T_SUBJECTS: [MessageHandler(TEXT, t_subjects)],
        T_GRADES: [MessageHandler(TEXT, t_grades)],
        T_AREA: [MessageHandler(TEXT, t_area)],
        T_PHONE: [MessageHandler(TEXT, t_phone)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("myid", myid))
app.add_handler(parent_form)
app.add_handler(tutor_form)

print("Bot is running... press Ctrl+C to stop")
app.run_polling()