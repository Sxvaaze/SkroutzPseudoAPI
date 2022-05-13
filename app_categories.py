import main as skroutzapi

link = input("Give url: ")

res = skroutzapi.call(link, category=True)
print(res)