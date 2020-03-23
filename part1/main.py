from fileFunction import menuProgam, chargerData, convertCsvJson
quitter = 'non'
# End of convert Json 
urlToCsv = 'netflix_shows.json'

while quitter != 'oui':
    # Appel le menu
    menuProgam()
    response = input('Faites un choix : ')
    choix = int(response)
    if choix == 1:
        chargerData(urlToCsv)
    elif choix == 2:
        convertCsvJson(chargerData(urlToCsv))
    elif choix == 3:
        print('Indexer les données...')
        # Indexer le fichier 
    quitter = input("Vous voulez quittez (oui/non) : ")