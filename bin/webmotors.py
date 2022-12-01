from asyncio import threads
import requests
import json
import os
from threading import Thread

def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + "_" + str(counter) + extension
        counter += 1

    return path

def getImages(marca, modelo, versao, paginas):
    count = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'AMCV_3ADD33055666F1A47F000101%40AdobeOrg=1176715910%7CMCIDTS%7C19250%7CMCMID%7C57678114885588894255475597516422916789%7CMCOPTOUT-1663239309s%7CNONE%7CvVersion%7C5.4.0; _gcl_aw=GCL.1663024195.CjwKCAjwsfuYBhAZEiwA5a6CDPdowuX-ptYm4Mld18WBqh5fPTKCRoIsatdsHxxDSyrPFuSUEkX8XhoCaPwQAvD_BwE; _gcl_dc=GCL.1663024195.CjwKCAjwsfuYBhAZEiwA5a6CDPdowuX-ptYm4Mld18WBqh5fPTKCRoIsatdsHxxDSyrPFuSUEkX8XhoCaPwQAvD_BwE; _gcl_au=1.1.272342158.1663024194; blueID=70cb01e8-f26e-4eea-adad-6b4168a93002; _pxvid=03867298-32f0-11ed-8a2a-495042796a71; AWSALB=MW8hndKLWQzEs9JzAhmYZ6HNeswRmcLdoJhqC8yBYH7nO+eVE052W8uUiSxsk1vZPxnuyQ02u+renGFs2rVibYZFjc5G787+F4IkkKBO/BIJy17CBkt6EFO26GZ8; AWSALBCORS=MW8hndKLWQzEs9JzAhmYZ6HNeswRmcLdoJhqC8yBYH7nO+eVE052W8uUiSxsk1vZPxnuyQ02u+renGFs2rVibYZFjc5G787+F4IkkKBO/BIJy17CBkt6EFO26GZ8; at_check=true; AMCVS_3ADD33055666F1A47F000101%40AdobeOrg=1; pxcts=fa33c564-3473-11ed-ac92-77474d75556f; s_cc=true; s_sq=webmglobaldev%3D%2526c.%2526a.%2526activitymap.%2526page%253D%25252Fwebmotors%25252Fcomprar%25252Fhomepage%2526link%253DVer%252520Ofertas%252520%252528399.959%252529%2526region%253DabId0.27896525129245975%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253D%25252Fwebmotors%25252Fcomprar%25252Fhomepage%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.webmotors.com.br%25252Fcarros%25252Festoque%25253Fidcmpint%25253Dt1%25253Ac17%25253Am07%25253Awebmotors%25253Abusca%25253A%25253Averofertas%2526ot%253DA; WMLastFilterSearch=%7B%22car%22%3A%22carros%2Festoque%22%2C%22bike%22%3A%22motos%2Festoque%22%2C%22estadocidade%22%3A%22estoque%22%2C%22lastType%22%3A%22car%22%2C%22cookie%22%3A%22v3%22%2C%22ano%22%3A%7B%7D%2C%22preco%22%3A%7B%7D%2C%22marca%22%3A%22HONDA%22%2C%22modelo%22%3A%22%22%7D; WebMotorsDataFormLeads=%7B%22dataForm%22%3A%7B%22uniqueId%22%3A43331344%2C%22listingType%22%3A%22U%22%2C%22vehicleType%22%3A%22car%22%2C%22idGuid%22%3A%22534ba688-ec2f-4d1d-b0d2-2afede900d93%22%2C%22make%22%3A%22HONDA%22%2C%22makeId%22%3A16%2C%22model%22%3A%22FIT%22%2C%22modelId%22%3A1194%2C%22version%22%3A%221.5%20EX%2016V%20FLEX%204P%20AUTOM%C3%81TICO%22%2C%22versionId%22%3A342096%2C%22yearModel%22%3A2013%2C%22yearFabrication%22%3A2012%2C%22price%22%3A64900%2C%22storeName%22%3A%22Nacional%20Veiculos%22%2C%22storeDocument%22%3A%2230062953000145%22%2C%22sellerId%22%3A3878286%2C%22sellerType%22%3A%22PJ%22%2C%22city%22%3A%22Santo%20Andr%C3%A9%22%2C%22hyundaiGroup%22%3Afalse%7D%7D; _px3=29c945fbc2c4bfe5081b3a28cf267a580cc3835b599f0c5593a80116f7c70069:81Vf2sl2aaB6nNNJ/QYnkOs7ykb5JEtA02oabNbQKQOSIY7q5rDIBUxLTp92tvU7qJH+Nl2stAG3Z6h2y5aoEg==:1000:EDy/9DBZpBYiRIuyYRystfOumT3t8DPi+avc+OaWcWhxv4LeD0OO7D+jjKVKo6aSZWolIeCh/PfXP07N1/MHEm364YZ3HGuU6TEUgjBGFOkGkLEjDDqfYCI3QOWbyEo8y+7Edj/sXvSlah7+AObbRpPfuPT1y537avHyswuNPcOJT1zY3JWXCV0Gb1vWRzVU2fe2iKAjWg104nYtIEeRXg==; mbox=session#3160c622c505499b8cf973f87d94b4fd#1663233960; WebMotorsVisitor=1; WebMotorsLastSearches=%5B%7B%22route%22%3A%22carros%2Festoque%2Fhonda%2Ffit%22%2C%22query%22%3A%22%22%7D%2C%7B%22route%22%3A%22carros-usados%2Festoque%2Fhonda%2Fcity%22%2C%22query%22%3A%22%3Ftipoveiculo%3Dcarros-usados%26marca1%3DHONDA%26modelo1%3DCITY%22%7D%2C%7B%22route%22%3A%22carros%2Festoque%2Fchevrolet%2Fastra%2F18-mpfi-comfort-sedan-8v-alcool-4p-manual%22%2C%22query%22%3A%22%3Ftipoveiculo%3Dcarros%26marca1%3DCHEVROLET%26modelo1%3DASTRA%26versao1%3D1.8%2520MPFI%2520COMFORT%2520SEDAN%25208V%2520%25C3%2581LCOOL%25204P%2520MANUAL%22%7D%2C%7B%22route%22%3A%22carros%2Festoque%2Fchevrolet%2Fastra%22%2C%22query%22%3A%22%3Ftipoveiculo%3Dcarros%26marca1%3DCHEVROLET%26modelo1%3DASTRA%22%7D%5D; gpv_v39=%2Fwebmotors%2Fcomprar%2Fhomepage; WebMotorsSearchDataLayer=%7B%22search%22%3A%7B%22location%22%3A%7B%7D%2C%22ordination%22%3A%7B%22name%22%3A%22Mais%20relevantes%22%2C%22id%22%3A1%7D%2C%22pageNumber%22%3A1%2C%22totalResults%22%3A21843%2C%22vehicle%22%3A%7B%22type%22%3A%7B%22id%22%3A1%2C%22name%22%3A%22carro%22%7D%7D%2C%22cardExhibition%22%3A%7B%22id%22%3A%221%22%2C%22name%22%3A%22Cards%20Grid%22%7D%2C%22eventType%22%3A%22buscaRealizada%22%7D%7D; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; WebMotorsTrackingFrom=buscaRealizada',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    URLAPI = 'https://www.webmotors.com.br/api/search/car?url='
    for pagina in range(paginas):
        URL = URLAPI+'https://www.webmotors.com.br/carros/estoque/'+marca+'/?&actualPage='+str(pagina)
        if modelo:
            URL = URLAPI+'https://www.webmotors.com.br/carros/estoque/'+marca+'/'+modelo+'/?&actualPage='+str(pagina)
            if versao:
                URL = URLAPI+'https://www.webmotors.com.br/carros/estoque/'+marca+'/'+modelo+'/'+versao.replace(' ', '-')+'?&actualPage='+str(pagina)
        resp = requests.get(URL, headers=headers)
        dic_resp = json.loads(resp.text)

        for n in range(24):
            count += 1
            try:
                curr = dic_resp['SearchResults'][n]['Specification']['Title']
                curryear = str(int(dic_resp['SearchResults'][n]['Specification']['YearModel']))
                currname = curr.split(' ')[0].lower()+"_"+curr.split(' ')[1].lower()
            except:
                print('END. No more results available.')
                return
            try:
                for m in range(50):
                    try:
                        img_path = dic_resp['SearchResults'][n]['Media']['Photos'][m]['PhotoPath']
                        img_path = img_path.replace('\\','/')

                        URLIMAGE = 'https://image.webmotors.com.br/_fotos/AnuncioUsados/gigante/'+img_path
                        
                        # dir = "images/"+curr.split(' ')[0].upper()+"/"+curr.split(' ')[1].upper()+'/'+curr+'/';
                        dir = "data/"+currname+'/'+currname+"_"+curryear+'/';
                        # dir = "images/"
                        if not os.path.exists(dir):
                            os.makedirs(dir)
                        # local_file = open(uniquify(dir+curr.replace(' ', '_')+".jpg"), "wb")
                        local_file = open(uniquify(dir+currname+".jpg"), "wb")
                        local_file.write(requests.get(URLIMAGE).content)
                        local_file.close()
                    except:
                        break
                # print(pagina+1, count, curr)
                print(curr)
            except:
                # print('ERROR', pagina+1, count, curr)
                print('ERROR', curr)
                pass
    return

threads_list = []
# carros  = [('honda','civic'), ('toyota','corolla'), ('honda','fit'), ('ford','fiesta'), ('ford','focus'), ('renault','duster'), ('chevrolet','cruze'), ('chevrolet','onix')]
carros  = [('honda','civic', ''), ('toyota','corolla', ''), ('fiat','uno', ''), ('chevrolet','celta', ''), ('volkswagen','nivus', ''), ('renault','duster', ''), ('ford','focus', ''), ('ford','fiesta', ''), ('ford','fusion', '')]

for carro in carros:
    marca, modelo, versao = carro
    new_thread = Thread(target=getImages,args=(marca, modelo, versao, 20))
    threads_list.append(new_thread)
    # getImages(marca, modelo, '', 5)
for thread in threads_list:
    thread.start()
for thread in threads_list:
    thread.join()
print(f'Finished.')
# marca  = 'subaru'
# modelo = 'impreza'
# versao = ''
# getImages(marca, modelo, versao, 5)
# versao = '2.0 WRX SEDAN 4X4 16V TURBO INTERCOOLER GASOLINA 4P AUTOMATICO'
# marcas = ['honda', 'toyota', 'ford', 'peugeot', 'chevrolet', 'volkswagen']
# for marca in marcas:
#     getImages(marca, modelo, versao, anode, anoate, 1)

