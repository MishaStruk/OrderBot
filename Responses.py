import DatabaseMoudle

def help_text(firstname):
    text = f"""Hello {firstname},\nThis is the help section
Registration:
In order to register use /start command.
When you use it, you will have to write your password twice.
You cannot use the commands as your password.
Ordering:
After you registered you could place an order. In order to place an order use /order command.
You can only order pizza,toast or falafel.
Example: /order. Then write pizza.
And you will order a pizza
Notice: You can only place one order each day.
Order list:
You can view all of your orders by typing /myorders
Password:
If you forgot your password use /password command. It will show you your password based on your ID.
"""
    return text
