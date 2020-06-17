import scrape as s

i = 1
while i <= 1000:
    print('Iteration: '+str(i))
    output = s.scrape_site()

    if output == -1:
        break
    i += 1