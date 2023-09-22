def create_spend_chart(categories):
    spent_amounts = []
    # Get total spent in each category
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    # Calculate percentage rounded down to the nearest 10
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    # Create the bar chart substrings
    header = "Percentage spent by category\n"

    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    names = list(map(lambda category: category.name, categories))
    max_length = max(map(lambda name: len(name), names))
    names = list(map(lambda name: name.ljust(max_length), names))
    for x in zip(*names):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + chart + footer).rstrip("\n")
        
      
class Category:
  
  def __init__(self,name):
    self.name = name
    self.ledger = list()
    
  #Constructor for the class, it needs to have a name and also in this problem an instance variable that is a list

  def __str__(self):
    category_title = f"{self.name:*^30}\n"
    #* is a fill character, ^ is an alignment specifier, It means that the content (in this case, self.name) should be centered within the available space. 30 is there to specify the width.
    items = ""
    total = 0
    for item in self.ledger:
      items += f"{item['description'][0:23]:23}" + f"{item['amount']:>7.2f}" + '\n'
      #the f-string, it is the first 23 character of description, and forced to fill spaces till 23 characters if it isnt log enough. in this case, the dictionary key named description is with single quotes cause if not it gives an error because of the f-string quotations
      total += item["amount"]
    output = category_title + items + "Total: " + str(total)
    return output
  #Built-in string method, whatever we return here will be printed when calling print function. f"{}" is an f-string, which is a way to format strings in Python. Inside the curly braces {...}, you can include expressions or variables, and Python will replace them with their values when the string is created. 
  
  def deposit(self, amount, description=""):
    """A deposit method that accepts an amount and description. If no description is given, it should default to an empty string. The method should append an object to the ledger list in the form of {"amount": amount, "description": description}."""
    self.ledger.append({"amount": amount, "description": description})
    #We only have to append the parameters of the function to the category list
  
  def withdraw(self, amount, description=""):
    """A withdraw method that is similar to the deposit method, but the amount passed in should be stored in the ledger as a negative number. If there are not enough funds, nothing should be added to the ledger. This method should return True if the withdrawal took place, and False otherwise."""
    if (self.check_funds(amount)):
      self.ledger.append({"amount": -abs(amount), "description": description})
      return True
    return False
  #Here first we have to check if we have funds then if true we withdraw and return a True if not just return False. -abs(amount) makes any number negative, it is not needed but it is more robust compared to -amount.
  
  def get_balance(self):
    """A get_balance method that returns the current balance of the budget category based on the deposits and withdrawals that have occurred."""
    balance=0
    for item in self.ledger:
      balance += item["amount"]
    return balance
    #We make the balance 0 (so we dont have some false data or we add past calls of the function together), then we add all the amounts in the list at the moment and that is the current balance. item["amount"] is a nice way of parsing through the list that in this case is a list of tuplets
  
  def transfer(self, amount, category):
    """A transfer method that accepts an amount and another budget category as arguments. The method should add a withdrawal with the amount and the description "Transfer to [Destination Budget Category]". The method should then add a deposit to the other budget category with the amount and the description "Transfer from [Source Budget Category]". If there are not enough funds, nothing should be added to either ledgers. This method should return True if the transfer took place, and False otherwise."""
    if (self.check_funds(amount)):
      self.withdraw(amount, "Transfer to " + category.name)
      category.deposit(amount, "Transfer from " + self.name)
      return True
    return False
    #To make a transfer we need to check if we have funds in the category that we'll take money from, if so transfer it to the other one
  
  def check_funds(self, amount):
    """A check_funds method that accepts an amount as an argument. It returns False if the amount is greater than the balance of the budget category and returns True otherwise. This method should be used by both the withdraw method and transfer method."""
    if (self.get_balance() < amount):
      return False
    return True
  #Uses the balance function, if balance is lower than amount we return Flase as if not enough funds
