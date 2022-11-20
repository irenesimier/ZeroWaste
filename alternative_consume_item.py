import csv

def consume_item_multiple():
    more_items = True
    header = ["Ingredients", "Quantity bought", "Best by date"]
    
    fobj = open("ingredient_stock.csv", "r")
    file_contents = fobj.read()
    fobj.close()
        
    row_list = file_contents.split("\n")[1:]
    row_list.remove("")
        
    list_row_elmts = []
    for string in row_list:
        list_row_elmts.append(string.split(","))
            
    dict_row = {}
    for i in range(len(list_row_elmts)):
        dict_row[i] = [list_row_elmts[i][0], int(list_row_elmts[i][1]), list_row_elmts[i][2]]    
            # {0: [item, qty, expiry], 1: [blabla]}
    
    while more_items:
        ingredient = input("What ingredient did you use? Please write \'n/a\' if there is no more item to remove: ")
        if ingredient == "n/a":
            more_items = False
            break
        list_of_ingr = []
        for key in dict_row:
            list_of_ingr.append(dict_row[key][0])
        
        while ingredient not in list_of_ingr:
            ingredient = input("The ingredient you inputted is not in the records. Please re-input the item: ")
            
        qty_used = int(input("How much of it did you use? (no units) "))
        qty_rem_for_ingred = 0
        for key in dict_row:
            if dict_row[key][0] == ingredient:
                qty_rem_for_ingred += int(dict_row[key][1])
                
        while qty_used > qty_rem_for_ingred:
            print("The quantity you inputted is greater than the total quantity of this ingredient in the records, which is recorded to be", str(qty_rem_for_ingred) + ".")
            qty_used = int(input("Please re-input the quantity: "))
        
        list_keys_to_del = []
        
        while qty_used > 0:
            for key in dict_row:
                should_break = False
                if dict_row[key][0] == ingredient:
                    if dict_row[key][1] <= qty_used:
                        list_keys_to_del.append(key)
                        qty_used -= dict_row[key][1]
                    else:
                        dict_row[key][1] -= qty_used
                        should_break = True
                        qty_used = 0
                        break
                if should_break:
                    break
        
    for key in list_keys_to_del:
        del dict_row[key]
    
    all_data = []
    for key in dict_row:
        all_data.append(dict_row[key])
    
    f = open("ingredient_stock.csv", "w", newline='') 
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(all_data)
    f.close()