import json
import requests
import aerisapisdk.aerisutils as aerisutils

afbase = 'https://api.aerframe.aeris.com'

def get_application_endpoint(accountId, appId = None):
    if appId == None:
        return afbase + '/registration/v2/' + accountId + '/applications'
    else:
        return afbase + '/registration/v2/' + accountId + '/applications/' + appId

def get_channel_endpoint(accountId, channelId = None):
    if channelId == None:
        return afbase + '/notificationchannel/v2/' + accountId + '/channels'
    else:
        return afbase + '/notificationchannel/v2/' + accountId + '/channels/' + channelId



    

def get_applications(verbose, accountId, apiKey, searchAppShortName):
    """
    Calls AerFrame API to get a list of all registered applications for the account.

    Parameters
    ----------
    accountId : str
        String version of the numerical account ID 
    apiKey : str
        String version of the GUID API Key. Can be found in AerPort / Quicklinks / API Keys

    Returns
    -------
    str
        String version of the GUID app ID for the app short name passed in or '' if no match found

    """
    endpoint = get_application_endpoint(accountId) # Get app endpoint based on account ID
    myparams = {'apiKey': apiKey}
    r = requests.get(endpoint, params = myparams)
    aerisutils.vprint(verbose, "Response code: " + str(r.status_code))
    if (r.status_code == 200):
        apps = json.loads(r.text)
        aerisutils.vprint(verbose, json.dumps(apps['application'], indent=4)) # Print formatted json
        sdkappexists = False
        sdkappid = ''
        for app in apps['application']: # Iterate applications to try and find application we are looking for
            if (app['applicationShortName'] == searchAppShortName):
                sdkappexists = True
                sdkappid = app['resourceURL'].split('/applications/',1)[1]
        if sdkappexists:
            print(searchAppShortName + ' application exists. App ID: ' + sdkappid)
            return sdkappid
        else:
            print(searchAppShortName + ' application does not exist')
            return sdkappid
    else: # Response code was not 200
        aerisutils.print_http_error(r)
        return ''


            
def get_application(verbose, accountId, apiKey, appId):
    """
    Calls AerFrame API to get a specific registered application

    Parameters
    ----------
    accountId : str
        String version of the numerical account ID 
    apiKey : str
        String version of the GUID API Key. Can be found in AerPort / Quicklinks / API Keys
    appId : str
        String version of the GUID app ID returned by the create_application call

    Returns
    -------
    Dictionary
        Configuration information for this application

    """
    endpoint = get_application_endpoint(accountId, appId) # Get app endpoint based on account ID and appID
    myparams = {'apiKey': apiKey}
    r = requests.get(endpoint, params = myparams)
    aerisutils.vprint(verbose, "Response code: " + str(r.status_code))
    if (r.status_code == 200):
        appConfig = json.loads(r.text)
        aerisutils.vprint(verbose, json.dumps(appConfig))
        return appConfig
    else: 
        aerisutils.print_http_error(r)
        return ''


   
def create_application(verbose, accountId, apiKey, appShortName):
    """
    Calls AerFrame API to create a registered application

    Parameters
    ----------
    accountId : str
        String version of the numerical account ID 
    apiKey : str
        String version of the GUID API Key. Can be found in AerPort / Quicklinks / API Keys
    appShortName : str
        String to use for the short name of the application

    Returns
    -------
    Dictionary
        Configuration information for this application

    """
    endpoint = get_application_endpoint(accountId) # Get app endpoint based on account ID
    payload =  { 'applicationName': appShortName, \
                 'description': 'Application for aerframe sdk', \
                 'applicationShortName': appShortName, \
                 'applicationTag': appShortName }
    myparams = {"apiKey": apiKey}
    r = requests.post(endpoint, params = myparams, json = payload)
    aerisutils.vprint(verbose, "Response code: " + str(r.status_code))
    if (r.status_code == 201): #Check for 'created' http response
        appConfig = json.loads(r.text)
        print('Created application:\n' + json.dumps(appConfig, indent=4))
        return appConfig
    else: 
        aerisutils.print_http_error(r)
        return ''



def delete_application(verbose, accountId, apiKey, appId):
    """
    Calls AerFrame API to delete a registered application

    Parameters
    ----------
    accountId : str
        String version of the numerical account ID 
    apiKey : str
        String version of the GUID API Key. Can be found in AerPort / Quicklinks / API Keys
    appId : str
        String version of the GUID app ID returned by the create_application call

    Returns
    -------
    bool
        True if successfully deleted
        False if does not exist or problem deleting

    """
    endpoint = get_application_endpoint(accountId, appId) # Get app endpoint based on account ID and appID
    myparams = {"apiKey": apiKey}
    r = requests.delete(endpoint, params = myparams)
    if (r.status_code == 204): #Check for 'no content' http response
        print('Successfully deleted.')
        return True
    elif (r.status_code == 404): #Check if no matching app ID
        print('App ID does not match current application.')
        return False
    else:
        aerisutils.print_http_error(r)
        return False




# ========================================================================



def getchannels(verbose, accountId, apiKey, searchAppTag):
    endpoint = get_channel_endpoint(accountId)
    myparams = {'apiKey': apiKey}
    r = requests.get(endpoint, params = myparams)
    aerisutils.vprint(verbose, "Response code: " + str(r.status_code))
    if (r.status_code == 200):
        channels = json.loads(r.text)
        aerisutils.vprint(verbose, json.dumps(channels['notificationChannel'], indent=4)) # Print formatted json
        sdkchannelexists = False
        sdkchannelid = ''
        for channel in channels['notificationChannel']: # Iterate channels to try and find sdk application
            if (channel['applicationTag'] == searchAppTag):
                sdkchannelexists = True
                sdkchannel = channel
                sdkchannelid = channel['resourceURL'].split('/channels/',1)[1]
        if sdkchannelexists:
            print('SDK channel exists. Channel ID: ' + sdkchannelid)
            print('Channel config: ' + json.dumps(sdkchannel, indent=4))
            return sdkchannelid
        else:
            print('SDK channel does not exist')
            return sdkchannelid
    else: # Response code was not 200
        aerisutils.print_http_error(r)
        return ''



def getchannel(verbose, accountId, apiKey, channelId):
    endpoint = get_channel_endpoint(accountId, channelId)
    myparams = {'apiKey': apiKey}
    r = requests.get(endpoint, params = myparams)
    aerisutils.vprint(verbose, "Response code: " + str(r.status_code))
    if (r.status_code == 200):
        channelConfig = json.loads(r.text)
        aerisutils.vprint(verbose, json.dumps(channelConfig))
        return channelConfig
    else: 
        aerisutils.print_http_error(r)
        return ''




def createchannel(verbose, accountId, apiKey, applicationTag):
    endpoint = get_channel_endpoint(accountId)
    channelData = {'maxNotifications': '15',
                    'type': 'nc:LongPollingData'}
    payload =  { 'applicationTag': applicationTag, \
                 'channelData': channelData, \
                 'channelType': 'LongPolling' }
    myparams = {"apiKey": apiKey}
    r = requests.post(endpoint, params = myparams, json = payload)
    aerisutils.vprint(verbose, "Response code: " + str(r.status_code))
    if (r.status_code == 200): # In this case, we get a 200 for success rather than 201 like for application
        channelConfig = json.loads(r.text)
        print('Created notification channel:\n' + json.dumps(channelConfig, indent=4))
        return channelConfig
    else: 
        aerisutils.print_http_error(r)
        return ''


def deletechannel(verbose, accountId, apiKey, channelId):
    endpoint = get_channel_endpoint(accountId, channelId)
    myparams = {"apiKey": apiKey}
    r = requests.delete(endpoint, params = myparams)
    if (r.status_code == 204): #Check for 'no content' http response
        print('Successfully deleted.')
        return True
    elif (r.status_code == 404): #Check if no matching channel ID
        print('Channel ID does not match current application.')
        return False
    else:
        aerisutils.print_http_error(r)
        return False




# ========================================================================



def getsubscriptions(verbose, accountId, apiKey, appShortName):
    getinboundsubscriptions(verbose, accountId, apiKey, appShortName)
    getoutboundsubscriptions(verbose, accountId, apiKey, appShortName)
    

def getinboundsubscriptions(verbose, accountId, apiKey, appShortName):
    endpoint = 'https://api.aerframe.aeris.com/smsmessaging/v2/' + accountId + '/inbound/subscriptions'
    myparams = {'apiKey': apiKey}
    r = requests.get(endpoint, params = myparams)
    aerisutils.vprint(verbose, "Response code: " + str(r.status_code))
    if (r.status_code == 200):
        subscriptions = json.loads(r.text)
        aerisutils.vprint(verbose, json.dumps(subscriptions['subscription'], indent=4)) # Print formatted json
        print('Inbound subscriptions:\n')
        for subscription in subscriptions['subscription']: # Iterate subscriptions to try and find sdk application
            print(subscription['destinationAddress'])
    else: # Response code was not 200
        aerisutils.print_http_error(r)
        return ''

def getoutboundsubscriptions(verbose, accountId, apiKey, appShortName):
    endpoint = 'https://api.aerframe.aeris.com/smsmessaging/v2/' + accountId + '/outbound/' + appShortName + '/subscriptions'
    myparams = {'apiKey': apiKey}
    r = requests.get(endpoint, params = myparams)
    aerisutils.vprint(verbose, "Response code: " + str(r.status_code))
    if (r.status_code == 200):
        subscriptions = json.loads(r.text)
        if 'deliveryReceiptSubscription' in subscriptions.keys():
            print('There are outbound (MT-DR) subscriptions.' + json.dumps(subscriptions, indent=4))
            subscriptionId = subscriptions['deliveryReceiptSubscription'][0]['resourceURL'].split('/subscriptions/',1)[1]
            print('Subscription ID: ' + subscriptionId)
            return subscriptionId
        else:
            print('No outbound (MT-DR) subscriptions: ' + json.dumps(subscriptions, indent=4))
            return ''
    else: # Response code was not 200
        aerisutils.print_http_error(r)
        return ''

def getoutboundsubscription(verbose, accountId, apiKey, appShortName, subscriptionId):
    endpoint = 'https://api.aerframe.aeris.com/smsmessaging/v2/' + accountId + '/outbound/' + appShortName + '/subscriptions/' + subscriptionId
    myparams = {'apiKey': apiKey}
    r = requests.get(endpoint, params = myparams)
    aerisutils.vprint(verbose, "Response code: " + str(r.status_code))
    if (r.status_code == 200):
        subscription = json.loads(r.text)
        return subscription
    else: # Response code was not 200
        aerisutils.print_http_error(r)
        return ''

def createoutboundsubscription(verbose, accountId, apiKey, appShortName, appChannelId):
    endpoint = 'https://api.aerframe.aeris.com/smsmessaging/v2/' + accountId + '/outbound/' + appShortName + '/subscriptions'
    callbackReference = {'callbackData': appShortName + '-mt',
                        'notifyURL': 'https://api.aerframe.aeris.com/notificationchannel/v2/' \
                        + accountId + '/channels/' + appChannelId + '/callback'}
    payload =  { 'callbackReference': callbackReference, \
                 'filterCriteria': 'SP:*', \
                 #'filterCriteria': 'SP:Aeris', \
                 'destinationAddress': [appShortName] }
    myparams = {"apiKey": apiKey}
    print('Payload: \n' + json.dumps(payload, indent=4))
    r = requests.post(endpoint, params = myparams, json = payload)
    aerisutils.vprint(verbose, "Response code: " + str(r.status_code))
    if (r.status_code == 201): # In this case, we get a 201 'created' for success
        subscriptionConfig = json.loads(r.text)
        print('Created outbound (MT-DR) subscription:\n' + json.dumps(subscriptionConfig, indent=4))
        return subscriptionConfig
    else: 
        aerisutils.print_http_error(r)
        return ''

def deleteoutboundsubscription(verbose, accountId, apiKey, appShortName, subscriptionId):
    print('subID: ' + subscriptionId)
    print('appShortName: ' + appShortName)
    endpoint = 'https://api.aerframe.aeris.com/smsmessaging/v2/' + accountId + '/outbound/' \
                + appShortName + '/subscriptions/' + subscriptionId
    myparams = {"apiKey": apiKey}
    r = requests.delete(endpoint, params = myparams)
    if (r.status_code == 204): #Check for 'no content' http response
        print('Successfully deleted.')
        return True
    elif (r.status_code == 404): #Check if no matching subscription ID
        print('Subscription ID does not match current application.')
        return False
    else:
        aerisutils.print_http_error(r)
        return False




# ========================================================================


    
def sendmtsms(verbose, accountId, apiKey, appShortName, imsiDestination, smsText):
    endpoint = 'https://api.aerframe.aeris.com/smsmessaging/v2/' + accountId + '/outbound/' + appShortName + '/requests'
    #address = ["311882995001753"]
    #address = ["204043398999957"]
    address = [imsiDestination]
    outboundSMSTextMessage = {"message": smsText}
    payload =  { 'address': address, \
                 'senderAddress': appShortName, \
                 'outboundSMSTextMessage': outboundSMSTextMessage, \
                 'clientCorrelator': '123456', \
                 'senderName': appShortName }
    myparams = {"apiKey": apiKey}
    #print('Payload: \n' + json.dumps(payload, indent=4))
    r = requests.post(endpoint, params = myparams, json = payload)
    aerisutils.vprint(verbose, "Response code: " + str(r.status_code))
    if (r.status_code == 201): # In this case, we get a 201 'created' for success
        sendsmsresponse = json.loads(r.text)
        print('Sent SMS:\n' + json.dumps(sendsmsresponse, indent=4))
        return sendsmsresponse
    elif (r.status_code == 404): #Check if no matching device IMSI or IMSI not support SMS
        print('IMSI is not found or does not support SMS.')
        print(r.text)
        return False
    else: 
        aerisutils.print_http_error(r)
        return ''

def poll_notification_channel(verbose, accountId, apiKey, channelURL):
    myparams = {'apiKey': apiKey}
    print('Polling channelURL for polling interval: ' + channelURL)    
    r = requests.get(channelURL, params = myparams)
    aerisutils.vprint(verbose, "Response code: " + str(r.status_code))
    if (r.status_code == 200):
        getsms = json.loads(r.text)
        print('MO SMS and MT SMS DR:\n' + json.dumps(getsms, indent=4))
    else: # Response code was not 200
        aerisutils.print_http_error(r)
        return ''

def getlocation(verbose, accountId, apiKey, deviceIdType, deviceId):
    endpoint = 'https://api.aerframe.aeris.com/networkservices/v2/' + accountId + '/devices/' + deviceIdType + '/' + deviceId + '/networkLocation'
    myparams = {'apiKey': apiKey}
    r = requests.get(endpoint, params = myparams)
    aerisutils.vprint(verbose, "Response code: " + str(r.status_code))
    if (r.status_code == 200):
        locationInfo = json.loads(r.text)
        print('Location information:\n' + json.dumps(locationInfo, indent=4))
    else: # Response code was not 200
        aerisutils.print_http_error(r)
        return ''