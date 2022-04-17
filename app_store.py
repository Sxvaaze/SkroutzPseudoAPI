import main as skroutzapi
"""
          _____                    _____                    _____                   _______                           _____                _____                   _______                   _____                    _____                    _____          
         /\    \                  /\    \                  /\    \                 /::\    \                         /\    \              /\    \                 /::\    \                 /\    \                  /\    \                  /\    \         
        /::\    \                /::\    \                /::\____\               /::::\    \                       /::\    \            /::\    \               /::::\    \               /::\    \                /::\    \                /::\    \        
       /::::\    \              /::::\    \              /::::|   |              /::::::\    \                     /::::\    \           \:::\    \             /::::::\    \             /::::\    \              /::::\    \              /::::\    \       
      /::::::\    \            /::::::\    \            /:::::|   |             /::::::::\    \                   /::::::\    \           \:::\    \           /::::::::\    \           /::::::\    \            /::::::\    \            /::::::\    \      
     /:::/\:::\    \          /:::/\:::\    \          /::::::|   |            /:::/~~\:::\    \                 /:::/\:::\    \           \:::\    \         /:::/~~\:::\    \         /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \     
    /:::/  \:::\    \        /:::/__\:::\    \        /:::/|::|   |           /:::/    \:::\    \               /:::/__\:::\    \           \:::\    \       /:::/    \:::\    \       /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \    
   /:::/    \:::\    \      /::::\   \:::\    \      /:::/ |::|   |          /:::/    / \:::\    \              \:::\   \:::\    \          /::::\    \     /:::/    / \:::\    \     /::::\   \:::\    \      /::::\   \:::\    \       \:::\   \:::\    \   
  /:::/    / \:::\    \    /::::::\   \:::\    \    /:::/  |::|___|______   /:::/____/   \:::\____\           ___\:::\   \:::\    \        /::::::\    \   /:::/____/   \:::\____\   /::::::\   \:::\    \    /::::::\   \:::\    \    ___\:::\   \:::\    \  
 /:::/    /   \:::\ ___\  /:::/\:::\   \:::\    \  /:::/   |::::::::\    \ |:::|    |     |:::|    |         /\   \:::\   \:::\    \      /:::/\:::\    \ |:::|    |     |:::|    | /:::/\:::\   \:::\____\  /:::/\:::\   \:::\    \  /\   \:::\   \:::\    \ 
/:::/____/     \:::|    |/:::/__\:::\   \:::\____\/:::/    |:::::::::\____\|:::|____|     |:::|    |        /::\   \:::\   \:::\____\    /:::/  \:::\____\|:::|____|     |:::|    |/:::/  \:::\   \:::|    |/:::/__\:::\   \:::\____\/::\   \:::\   \:::\____\
\:::\    \     /:::|____|\:::\   \:::\   \::/    /\::/    / ~~~~~/:::/    / \:::\    \   /:::/    /         \:::\   \:::\   \::/    /   /:::/    \::/    / \:::\    \   /:::/    / \::/   |::::\  /:::|____|\:::\   \:::\   \::/    /\:::\   \:::\   \::/    /
 \:::\    \   /:::/    /  \:::\   \:::\   \/____/  \/____/      /:::/    /   \:::\    \ /:::/    /           \:::\   \:::\   \/____/   /:::/    / \/____/   \:::\    \ /:::/    /   \/____|:::::\/:::/    /  \:::\   \:::\   \/____/  \:::\   \:::\   \/____/ 
  \:::\    \ /:::/    /    \:::\   \:::\    \                  /:::/    /     \:::\    /:::/    /             \:::\   \:::\    \      /:::/    /             \:::\    /:::/    /          |:::::::::/    /    \:::\   \:::\    \       \:::\   \:::\    \     
   \:::\    /:::/    /      \:::\   \:::\____\                /:::/    /       \:::\__/:::/    /               \:::\   \:::\____\    /:::/    /               \:::\__/:::/    /           |::|\::::/    /      \:::\   \:::\____\       \:::\   \:::\____\    
    \:::\  /:::/    /        \:::\   \::/    /               /:::/    /         \::::::::/    /                 \:::\  /:::/    /    \::/    /                 \::::::::/    /            |::| \::/____/        \:::\   \::/    /        \:::\  /:::/    /    
     \:::\/:::/    /          \:::\   \/____/               /:::/    /           \::::::/    /                   \:::\/:::/    /      \/____/                   \::::::/    /             |::|  ~|               \:::\   \/____/          \:::\/:::/    /     
      \::::::/    /            \:::\    \                  /:::/    /             \::::/    /                     \::::::/    /                                  \::::/    /              |::|   |                \:::\    \               \::::::/    /      
       \::::/    /              \:::\____\                /:::/    /               \::/____/                       \::::/    /                                    \::/____/               \::|   |                 \:::\____\               \::::/    /       
        \::/____/                \::/    /                \::/    /                 ~~                              \::/    /                                      ~~                      \:|   |                  \::/    /                \::/    /        
         ~~                       \/____/                  \/____/                                                   \/____/                                                                \|___|                   \/____/                  \/____/         

                                                                                                SkroutzPseudo API V1.2.0 Beta by github.com/Sxvaaze                                                                                                                                                                                                                                                              
"""

# If link is empty or not a valid skroutz product url (does not contain "skroutz.gr/shop/") then all api calls will return an error defined by function filter_input in main.py
link = input("Give url: ")

# Store Demo #1
res1 = skroutzapi.call(link)

# Store Demo #2
res2 = skroutzapi.call(link, store_data = ['name', 'tags', 'rating_score', 'rating_count', 'payment_methods', 'address', 'gemh_num'])
# The store_data = [] <List> flag will filter out the dict results to only scrape for the data given as arguments. This will heavily increase 
# performance in the scenario where you want to scrape only certain data, so please consider using it.

# WARNING: if store_data is given as an empty list, then the api will return None NOT A DICTIONARY (e.g: data=[])

# store_data options: 'all' returns all data
# 'name' returns store name
# 'tags' returns store tags
# 'identifiers' returns the identifiers dict
# 'shop_links' enables the check for store info (telephone, has_website, website_url, has_skroutz_products, skroutz_products_page)
# 'rating_score' returns the score (out of 5 / stars)
# 'rating_count' returns the rating count (positive, negative, total)
# 'payment_methods' returns the payment methods the store supports
# 'address' returns the store's address
# 'gemh_num' returns the store's num in the Γ.Ε.ΜΗ (Γενικό Εμπορικό Μητρώο)

print(res1)
print('-' * 100)
print(res2)