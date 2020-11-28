
        #### Parse session variables that we will need to return when we submit search form
        viewState = formDecoded.split("__VIEWSTATE",maxsplit=-1)[2]
        viewState = viewState.split('"',maxsplit=-1)[2]
        viewStateGenerator = formDecoded.split("__VIEWSTATEGENERATOR",maxsplit=-1)[2]
        viewStateGenerator = viewStateGenerator.split('"',maxsplit=-1)[2]
        eventValidation = formDecoded.split("__EVENTVALIDATION",maxsplit=-1)[2]
        eventValidation = eventValidation.split('"',maxsplit=-1)[2]

        #### Set the form parameters
        params = {
                '__EVENTTARGET':'',
                '__EVENTARGUMENT':'',
                '__VIEWSTATE':viewState,
                '__VIEWSTATEGENERATOR':viewStateGenerator,
                '__EVENTVALIDATION':eventValidation,
                'propertySearchOptions:ownerName':'frank',
                'propertySearchOptions:streetNumber':'',
                'propertySearchOptions:streetName':'',
                'propertySearchOptions:propertyid':'',
                'propertySearchOptions:geoid':'',
                'propertySearchOptions:dba':'',
                'propertySearchOptions:abstract':'',
                'propertySearchOptions:subdivision':'',
                'propertySearchOptions:mobileHome':'',
                'propertySearchOptions:condo':'',
                'propertySearchOptions:agentCode':'',
                'propertySearchOptions:taxyear':2019,
                'propertySearchOptions:propertyType':'All',
                'propertySearchOptions:orderResultsBy':'Owner Name',
                'propertySearchOptions:recordsPerPage':25,
                'propertySearchOptions:searchAdv':'Search'
                }

                # 'propertySearchOptions:searchText':'frank',
                # 'propertySearchOptions:search':'Search',

        #### Set the cookies
        # cookieDict = dict(aSession.cookies)
        # for i in cookieDict:
        #     cookieText = i + "=" + cookieDict[i]
        # cookieText = {'Cookie':cookieText}
        # print(aSession.cookies)
        #### POST request form submission
        time.sleep(3)
        #r = aSession.post(searchForm2,data=json.dumps(params))
        r = aSession.post(searchForm2,data=params)
        #print(r.request.cookies)
        #r = requests.post(searchForm2,headers=headers,data=blah)
        #print("\n**************************** Headers\n")
        # print("\n**************************** Body\n")
        # print(r.request.body)
        # print("\n**************************** Response content\n")
        # print(r.content.decode("utf-8"))
        #print(r.content)
        ##s = aSession.get("https://propaccess.trueautomation.com/clientdb/SearchResults.aspx?cid=20")
        # print(s.content.decode("utf-8"))
