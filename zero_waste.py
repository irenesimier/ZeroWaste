import datetime
import csv
import os.path

def zero_waste():

    def convert_date(date):
        incorrect = True
        while (incorrect):
            try:
                time = date.split("/")
                while len(time[0]) != 4 or len(time[1]) != 2 or len(time[2]) != 2:
                    date = input("Incorrect date format. Please re-input the date: ")
                    time = date.split("/")    
                if int(time[1]) == 0:
                    time[1].remove("0")
                if int(time[2]) == 0:
                    time[2].remove("0")
                date = datetime.datetime(int(time[0]), int(time[1]), int(time[2]))
                incorrect = False
                return date
            except ValueError:
                date = input("Incorrect date format. Please re-input the date: ")
        



    def buy_item():
        more_items = True
        header = ["Ingredients", "Quantity", "Best by date"]
        all_data = []
        while more_items:
            row_data = []
            ingredient = input("What ingredient did you buy? ")
            if ingredient == "STOP":
                more_items = False
                break
            qty_bought = input("How much of it did you buy? (no units) ")
            best_by = convert_date(input("Please input the best-by date (YYYY/MM/DD): "))
            row_data.append(ingredient)
            row_data.append(qty_bought)
            row_data.append(best_by)
            all_data.append(row_data)
        file_exists = os.path.isfile("ingredient_stock.csv")
        f = open("ingredient_stock.csv", "a", encoding= 'UTF8', newline='') 
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerows(all_data)
     
     
     
    def consume_item():
        more_items = True
        while more_items:
            lines = list()
            consumed_ingredient = input("Please enter consumed item: ")
            if consumed_ingredient == "STOP":
                more_items = False
                break
            consumed_quantity = input("Please enter how many item of this type you consumed: ")
            with open('ingredient_stock.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                not_in_stock = True
                for row in reader:
                    if row[0] == consumed_ingredient:
                        not_in_stock = False
                        row[1] = str(int(row[1]) - int(consumed_quantity))
                        if int(row[1]) < 0:
                            print('WARNING! Empty Stock... You only consumed: ')
                            available_items = int(row[1]) + int(consumed_quantity)
                            print (available_items)
                        elif int(row[1]) > 0:
                            lines.append(row)
                    else:
                        lines.append(row)
                if (not_in_stock):
                    print('Item not in stock')            
            with open('ingredient_stock.csv', 'w') as writeFile:
                write = csv.writer(writeFile)
                write.writerows(lines)
            
            
            
    def donate():
        today = datetime.datetime.today()
        stock_lines = list()
        donation_lines = list()
        with open('ingredient_stock.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            firstline = True
            for row in reader:
                if firstline:
                    stock_lines.append(row)
                    donation_lines.append(row)
                    firstline = False
                else:
                    best_by = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
                    if best_by > today:
                        stock_lines.append(row)
                    else:
                        donation_lines.append(row)
        with open('ingredient_stock.csv', 'w') as writeFile:
            write = csv.writer(writeFile)
            write.writerows(stock_lines)
        with open('donation.csv', 'w') as writeFile:
            write = csv.writer(writeFile)
            write.writerows(donation_lines)
    
    
    
    def display_menu(): 
        make_changes=True
        while make_changes:
            print ("""
            What would you like to do? 
            1. Buy item (Type STOP to stop buying)
            2. Consume item (Type STOP to stop consuming)
            3. Prepare today's donation list
            4. Exit
            """)
            ans=input("Select an option above: ") 
            if ans=="1":
                buy_item()
                print("\n Items added to Stock.") 
            elif ans=="2":
                consume_item()
                print("\n Items removed from Stock.") 
            elif ans=="3":
                donate()  
                print("\n Donation list is updated.")
            elif ans=="4":
                make_changes=False
                print("\n Exit")  
            else:
                print("\n Invalid choice, please re-input an option: ")
    
    
    
    def main():
        display_menu()
        
    if __name__ == "__main__":
        main()