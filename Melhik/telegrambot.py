# from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
# from Melhikapp.models import *

# FREELANCER, EMPLOYER = range(2) 

# USERNAME, FIRST_NAME, LAST_NAME, EMAIL, PASSWORD = range(5)

# def start(update, context):
#     context.user_data['context'] = context
#     reply_keyboard = [
#         ['Freelancer', 'Employer']
#     ]

#     update.message.reply_text(
#         'Please select whether you are a Freelancer or Employer:',
#         reply_markup=ReplyKeyboardMarkup(
#             reply_keyboard, one_time_keyboard=True))

#     return FREELANCER

# def freelancer_employer(update, context):
#     context = update.effective_user.user_data['context'] = context
#     user = update.message.text
#     if user == 'Freelancer':
#         update.message.reply_text(
#             'Please enter your credentials:', 
#             reply_markup=ReplyKeyboardRemove())
#         return USERNAME
#     else:
#         update.message.reply_text(
#             'Please enter your credentials:',
#             reply_markup=ReplyKeyboardRemove())
#         return USERNAME


# def username(update, context):
#   username = update.message.text
#   if not username:
#     update.message.reply_text("Please enter a username")
#     return USERNAME
#   context.user_data['username'] = username
#   return FIRST_NAME


# def first_name(update, context):
#   first_name = update.message.text
#   if not first_name:
#     update.message.reply_text("Please enter your first name")
#     return FIRST_NAME
#   context.user_data['first_name'] = first_name
#   return LAST_NAME


# def last_name(update, context):
#    lastname = update.message.text
#    if not lastname:
#      update.message.reply_text('Please enter your surname')
#      return LAST_NAME
#    context.user_data['lastname'] = lastname
#    return EMAIL


# # Email handler  
# def email(update, context):
#   email = update.message.text
#   if not email:
#     update.message.reply_text("Please enter your email")
#     return EMAIL
#   context.user_data['email'] = email
#   return PASSWORD


# def password(update, context):
#   password = update.message.text
#   if not password:
#     update.message.reply_text("Please enter a password")
#     return PASSWORD
#   if len(password) < 8:
#     update.message.reply_text("Password must be at least 8 characters")
#     return PASSWORD
#   if not any(char.isalpha() for char in password) or not any(char.isdigit() for char in password):  
#     update.message.reply_text("Password must contain letters and numbers")
#     return PASSWORD
#   context.user_data['password'] = password
#   return "done"

# def done(update, context):
#   update.message.reply_text("Thank you for choosing KofeJob") 
#   return ConversationHandler.END

# def fallback(update, context):
#   update.message.reply_text("Invalid input") 
#   return ConversationHandler.END



# def main():
#     updater = Updater("6575514030:AAFO2CwLOdy7dkZKyMosGNmZuVMPXHL0ZlQ", use_context=True)

#     dp = updater.dispatcher

#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('start', start)],

#         states={
#             FREELANCER: [MessageHandler(Filters.text, freelancer_employer)],

#             USERNAME: [MessageHandler(Filters.text, username)], 

#             FIRST_NAME: [MessageHandler(Filters.text, first_name)],

#             LAST_NAME:[MessageHandler(Filters.text,last_name)],

#             EMAIL:[MessageHandler(Filters.text,email)],

#             PASSWORD: [
#                         MessageHandler(Filters.text, password), 
#                       ]},
                       
#         fallbacks=[MessageHandler(Filters.regex("^Done$"), done)]
#     )

#     dp.add_handler(conv_handler)

#     updater.start_polling()
#     updater.idle()

# if __name__ == '__main__':
#     main()