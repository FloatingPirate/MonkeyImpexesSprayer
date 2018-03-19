##You know, that kind of thing, that makes Your life easier

#############################################RELEASE VERSION DICTIONARIES#############################################
stores_r1 = {'eur':'lynxeubasestore', 'sv': 'lynxswestore', 'fi':'lynxfinstore', 'no': 'lynxnorstore', 'da': 'lynxdnkstore'}
stores_r2 = {'eur':'lynxeubasestore', 'sv': 'lynxswestore', 'fi':'lynxfinstore', 'no': 'lynxnorstore', 'da': 'lynxdnkstore', 
'pt':'lynxprtstore', 'be': 'lynxbelstore', 'nl': 'lynxnldstore', 'es': 'lynxespstore'}

#############################################MONKEY IMPEX BODY#############################################
PROCESSOR_LINE = """UPDATE GenericItem[processor = de.hybris.platform.commerceservices.impex.impl.ConfigPropertyImportProcessor]; pk[unique = true]\n"""
CONTENT_CATALOG_CONFIG_LINE = """$contentCatalog = $config-lx.{0}.content.catalog\n"""
CONTENT_CATALOG_VERSION_LINE = """$contentCatalogVersion = Staged\n"""
CONTENT_CATALOG_VERSION = """$catalogVersion = catalogVersion(catalog(id[default = '$contentCatalog']), version[default = '$contentCatalogVersion'])[unique = true, default = '$contentCatalog:$contentCatalogVersion']\n"""
THEME_ID = """$defaultThemeId = blue"""
NEW_LINE_X = "\n"
IMPEX_HEADER = """INSERT_UPDATE LynxTranslationItem; code[unique = true]; $catalogVersion; englishMasterCopy; value[lang = en]; themeId[default = '$defaultThemeId']\n"""
IMPEX_VALUE_LINE = "; {0} ; ; {1} ; {2} ;"

#############################################MONKEY IMPEX LOCATION PATTERN#############################################
IMPEX_LOCATION_LINE = "bin/custom/{0}/resources/{0}/dataload/090_scandi_release/{1}\n"

#############################################COLLECTION OF ALL NECESSARY IMPEX PARAMETERS#############################################
def collectUserInput():
    eurFileName = raw_input('Eur file name: ')
    localFileName = raw_input('Local file name: ')
    monkeyCode = raw_input('Property code: ')
    emcpValue = raw_input('EMCP: ')
    englishValue = raw_input('English value: ')
    
    return [eurFileName, localFileName, monkeyCode, emcpValue, englishValue]

#############################################CREATION OF MONKEY IMPEXES BASED ON RELEASE VERSION#############################################
def createImpexesOutOfInput(inputData_list, monkey_version):
    
    if monkey_version == '1':
        for locale in stores_r1.keys(): 
            printImpexToFile(locale, inputData_list)
    elif monkey_version == '2': 
        for locale in stores_r2.keys(): 
            printImpexToFile(locale, inputData_list)
    else:
        print("\n\nUnsupported monkey impex version was selected. This script will do nothing.")

#############################################ACTUAL CREATION OF MONKEY IMPEX. ONE PER STORE#############################################        
def printImpexToFile(locale, inputData_list):
    
    location = getImpexLocation(locale, inputData_list)

    try: 
        with open(location, 'w+') as monkey_impex:
            monkey_impex.write(PROCESSOR_LINE)
            monkey_impex.write(CONTENT_CATALOG_CONFIG_LINE.format(locale))
            monkey_impex.write(CONTENT_CATALOG_VERSION_LINE)
            monkey_impex.write(CONTENT_CATALOG_VERSION)
            monkey_impex.write(NEW_LINE_X)
            monkey_impex.write(THEME_ID)
            monkey_impex.write(NEW_LINE_X*2)
            monkey_impex.write(IMPEX_HEADER)
            monkey_impex.write(IMPEX_VALUE_LINE.format(inputData_list[2], inputData_list[3], inputData_list[4]))
    except IOError: 
        print("\n\nProbably, the version of release(monkey version), that You are using, is not the one, that you've typed. Unsupported files will not be written")
    
#############################################DETERMENING OF IMPEX LOCATION BASED ON A STORE#############################################        
def getImpexLocation(locale, inputData_list):
    #EUR store impexes, as a rule, have a different name than all of the local store impexes
    eurFileName = inputData_list[0]
    localFileName = inputData_list[1]
    
    if locale == 'eur':
        location = IMPEX_LOCATION_LINE.format(stores_r2.get(locale), eurFileName)
    else: 
        location = IMPEX_LOCATION_LINE.format(stores_r2.get(locale), localFileName)

    return location
    
#############################################MAIN FUNCTION#############################################    
if __name__ == "__main__":
    
    try: 
        print("Type '1' for creation of impexes for countries existing before R2 only, and '2' otherwise\n")

        monkey_version = raw_input("Monkey version: ")

        monkey_values = collectUserInput()

        createImpexesOutOfInput(monkey_values, monkey_version)

    except KeyboardInterrupt:
        print("\n\nScript execution was interrupted by You, user. Live with it :(")