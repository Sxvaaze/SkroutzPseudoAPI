import main as skroutzapi
"""
          _____                    _____                    _____                   _______         
         /\    \                  /\    \                  /\    \                 /::\    \        
        /::\    \                /::\    \                /::\____\               /::::\    \       
       /::::\    \              /::::\    \              /::::|   |              /::::::\    \      
      /::::::\    \            /::::::\    \            /:::::|   |             /::::::::\    \     
     /:::/\:::\    \          /:::/\:::\    \          /::::::|   |            /:::/~~\:::\    \    
    /:::/  \:::\    \        /:::/__\:::\    \        /:::/|::|   |           /:::/    \:::\    \   
   /:::/    \:::\    \      /::::\   \:::\    \      /:::/ |::|   |          /:::/    / \:::\    \  
  /:::/    / \:::\    \    /::::::\   \:::\    \    /:::/  |::|___|______   /:::/____/   \:::\____\ 
 /:::/    /   \:::\ ___\  /:::/\:::\   \:::\    \  /:::/   |::::::::\    \ |:::|    |     |:::|    |
/:::/____/     \:::|    |/:::/__\:::\   \:::\____\/:::/    |:::::::::\____\|:::|____|     |:::|    |
\:::\    \     /:::|____|\:::\   \:::\   \::/    /\::/    / ~~~~~/:::/    / \:::\    \   /:::/    / 
 \:::\    \   /:::/    /  \:::\   \:::\   \/____/  \/____/      /:::/    /   \:::\    \ /:::/    /  
  \:::\    \ /:::/    /    \:::\   \:::\    \                  /:::/    /     \:::\    /:::/    /   
   \:::\    /:::/    /      \:::\   \:::\____\                /:::/    /       \:::\__/:::/    /    
    \:::\  /:::/    /        \:::\   \::/    /               /:::/    /         \::::::::/    /     
     \:::\/:::/    /          \:::\   \/____/               /:::/    /           \::::::/    /      
      \::::::/    /            \:::\    \                  /:::/    /             \::::/    /       
       \::::/    /              \:::\____\                /:::/    /               \::/____/        
        \::/____/                \::/    /                \::/    /                 ~~              
         ~~                       \/____/                  \/____/            

                            SkroutzPseudo API V1.1.0 Beta by github.com/Sxvaaze
"""

# If link is empty or not a valid skroutz product url (does not contain "skroutz.gr/s/") then all api calls will return an error defined by function filter_input in main.py
link = input("Give url: ")

#Demo 1 (API request for an item's data with no show_all & no limit)
#Returns base data and info of first store
res1 = skroutzapi.call(link)

# Demo 2 (API request for an item with show_all & no limit (Returns data from ALL STORES))
# Returns base data and info for all stores 
res2 = skroutzapi.call(link, show_all=True)

# Demo 3 (API request for an item with show_all & a limit (Returns ALL STORES if store_count <= limit, else returns data from up to << LIMIT >> stores))
# Returns base data and info for up to << limit >> stores
res3 = skroutzapi.call(link, show_all=True, limit=6)

# Demo 4 (Similar to demo3, but data flag is used)
# The data flag limits the api to scrape only for the dictionary keys given. This increases performance. All data not included in list will be returned as None
res4 = skroutzapi.call(link, show_all=True, limit=6, data=['base_price', 'store_count', 'rating_count', 'rating_score'])

# WARNING: if data is given as an empty list, then the api will return None NOT A DICTIONARY (e.g: data=[])

# data options: 'all' returns all available data
# 'product_name'
# 'base_price'
# 'store_names'
# 'store_count'
# 'rating_count'
# 'rating_score'
# 'discussion_count'
# 'lowest_price'
# 'max_price'
# 'is_on_sale'

print(res1)
print('-' * 100)
print(res2)
print('-' * 100)
print(res3)
print('-' * 100)
print(res4)
