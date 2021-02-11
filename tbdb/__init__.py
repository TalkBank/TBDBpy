""" TBDBpy: Python API to TalkBankDB.

TBDBpy allows access to data from TalkBankDB through several functions:
    * getTranscripts()
    * getParticipants()
    * getTokens()
    * getTokenTypes()
    * getUtterances()
    * getNgrams()
    * getCQL()

Each of these functions take a dictionary parameter defining a corpusName and 
a set of optional fields to define a TalkBankDB request.  Each returns a dictionary with 
two members: {'colHeadings': [], 'data': [[]]}
    - colHeadings: List of strings describing columns in data.
    - data: List of lists, where each list represents a table row.

Additional functions return metadata about TalkBankDB: 
    * getPathTrees()
    * validPath()
"""

import requests
import json
import getpass


########################################
# Private methods.
########################################
def _makeReq(queryParams, route, DB_query):
    """Processes request/response from each API function to TalkBankDB."""

    URL = 'https://sla2.talkbank.org:1515/' + route

    # Set default values in query if not set in queryParams.
    if DB_query:
        query = {
            'corpusName': queryParams['corpusName'],
            'corpora':  queryParams['corpora'] if 'corpora' in queryParams else {},
            'lang': queryParams['lang'] if 'lang' in queryParams else {},
            'media': queryParams['media'] if 'media' in queryParams else {},
            'age': queryParams['age'] if 'age' in queryParams else {},
            'gender': queryParams['gender'] if 'gender' in queryParams else {},
            'designType': queryParams['designType'] if 'designType' in queryParams else {},
            'activityType': queryParams['activityType'] if 'activityType' in queryParams else {},
            'groupType': queryParams['groupType'] if 'groupType' in queryParams else {},
            'cqlArr': queryParams['cqlArr'] if 'cqlArr' in queryParams else {},
            'nGram': queryParams['nGram'] if 'nGram' in queryParams else {},
            'respType': 'JSON'
        }

        if 'nsAuth' in queryParams:
            query['nsAuth'] = queryParams['nsAuth']

    if DB_query:
        resp = requests.post(URL, json={'queryVals': query})
    else:
        resp = requests.post(URL, json={})

    return json.loads(resp.text)


def _authenticate():
    """Collects input to define paths and userIDs/passwords to authenticate."""
    authReqs = []

    another = 'y'
    while another == 'y':
        path = input('Path to authenticate: ')
        user_id = input('User ID: ')
        password = getpass.getpass('Password: ')

        authReqs.append({'path': path, 'userID': user_id, 'pswd': password})

        another = input('Authenticate another? (Y/N): ')

        if another.lower() != 'y':
            return authReqs


#######################################
# Public API methods.
########################################
def getTranscripts(queryParams, auth=False):
    """
    Get transcript metadata where each row represents a transcript.

    Parameters
    ----------
    corpusName: str
        Name of corpus to query.  For example, to search within the childes corpus, corpus='childes'.
    corpora: list of list, optional
        Paths of corpus/corporas to query under corpusName.
        This is a path starting with the corpus name followed by subfolder names leading to a folder for which all transcripts beneath it will be queried.
        For example, to query all transcripts in the MacWhinney childes corpus: [['childes', 'Eng-NA', 'MacWhinney']].
    lang: list of str, optional
        Query by language.
        For example, to get transcripts that contain both English and Spanish: ['eng', 'spa']. 
        Legal values: 3-letter language codes based on the ISO 639-3 standard.
    media: list of str, optional
        Query by media type.  For example, to get transcripts with an associated video recording: ['video'].  
        Legal values: 'audio' or 'video'.
    age: list of dict, optional
        Query by participant month age range.  
        For example, to get transcripts with target participants who are 14-18 months old: [{'from': 14, 'to': 18}].
    gender: list of str, optional
        Query by participant gender. 
        For example, to get transcripts with female target participants: ['female'].  Legal values: 'female' or 'male'.
    designType: list of str, optional
        Query by design type.  
        For example, to get transcripts from a longitudinal study: ['long'] Legal values are 'long' for longitudinal studies, 'cross' for cross-sectional studies.
    activityType: list of str, optional
        Query by activity type.  
        For example, to get transcripts where the target participant is engaged in toy play: ['toyplay'].  See the CHAT manual for legal values.
    groupType: list of str, optional
        Query by group type.  
        For example, to get transcripts where the target participant is hearing limited: ['HL'].  See the CHAT manual for legal values.
    auth: list of str, default False
        Determine if user should be prompted to authenticate in order to access protected collections. Defaults to False.

    Returns
    -------
        dict
            Dictionary with two members:
                - colHeadings: List of strings describing columns in data.
                - data: List of lists, where each list represents a table row.

    Each list (row) in 'data' has:
    * Link to view transcript and play any associated media.
    * Corpus path to transcript.
    * Media types (audio/video) linked to transcript.
    * Unique ID for transcript (PID).
    * Languages spoken. Date recorded.
    * Design Type.
    * Activity Type.
    * Group Type.

    Examples
    --------
    Get metadata for one transcript:

    tbdb.getTranscripts({'corpusName': 'childes', 'corpora': [['childes','Eng-NA','MacWhinney', '010411a']]})
    """

    if auth:
        queryParams['nsAuth'] = _authenticate()

    return _makeReq(queryParams, 'getTranscriptSummary', True)


def getParticipants(queryParams, auth=False):
    """
    Get participant info of transcripts where each row represents a transcript.

    Parameters
    ----------
    corpusName: str
        Name of corpus to query.  For example, to search within the childes corpus, corpus='childes'.
    corpora: list of list, optional
        Paths of corpus/corporas to query under corpusName.
        This is a path starting with the corpus name followed by subfolder names leading to a folder for which all transcripts beneath it will be queried.
        For example, to query all transcripts in the MacWhinney childes corpus: [['childes', 'Eng-NA', 'MacWhinney']].
    lang: list of str, optional
        Query by language.
        For example, to get transcripts that contain both English and Spanish: ['eng', 'spa']. 
        Legal values: 3-letter language codes based on the ISO 639-3 standard.
    media: list of str, optional
        Query by media type.  For example, to get transcripts with an associated video recording: ['video'].  
        Legal values: 'audio' or 'video'.
    age: list of dict, optional
        Query by participant month age range.  
        For example, to get transcripts with target participants who are 14-18 months old: [{'from': 14, 'to': 18}].
    gender: list of str, optional
        Query by participant gender. 
        For example, to get transcripts with female target participants: ['female'].  Legal values: 'female' or 'male'.
    designType: list of str, optional
        Query by design type.  
        For example, to get transcripts from a longitudinal study: ['long'] Legal values are 'long' for longitudinal studies, 'cross' for cross-sectional studies.
    activityType: list of str, optional
        Query by activity type.  
        For example, to get transcripts where the target participant is engaged in toy play: ['toyplay'].  See the CHAT manual for legal values.
    groupType: list of str, optional
        Query by group type.  
        For example, to get transcripts where the target participant is hearing limited: ['HL'].  See the CHAT manual for legal values.
    auth: list of str, default False
        Determine if user should be prompted to authenticate in order to access protected collections. Defaults to False.

    Returns
    -------
        dict
            Dictionary with two members:
                - colHeadings: List of strings describing columns in data.
                - data: List of lists, where each list represents a table row.

    Each list (row) in 'data' has:
    * Link to view transcript and play any associated media.
    * Corpus path to transcript.
    * Speaker’s ID.
    * Speaker’s name.
    * Speaker’s role.
    * Speaker’s language.
    * Speaker’s age in months.
    * Speaker’s age in Years/Months/Days.
    * Speaker’s gender.
    * Number of words spoken by speaker.
    * Number of utterances spoken by speaker.
    * Average number of words per speaker’s utterance.
    * Median number of words per speaker’s utterance.

    Examples
    --------
    Get participant info for one transcript:

    tbdb.getParticipants({'corpusName': 'childes', 'corpora': [['childes','Eng-NA','MacWhinney', '010411a']]})
    """
    
    if auth:
        queryParams['nsAuth'] = _authenticate()

    return _makeReq(queryParams, 'getParticipantSummary', True)


def getUtterances(queryParams, auth=False):
    """
    Get utterance text and metadata info of transcripts where each row represents an utterance.

    Parameters
    ----------
    corpusName: str
        Name of corpus to query.  For example, to search within the childes corpus, corpus='childes'.
    corpora: list of list, optional
        Paths of corpus/corporas to query under corpusName.
        This is a path starting with the corpus name followed by subfolder names leading to a folder for which all transcripts beneath it will be queried.
        For example, to query all transcripts in the MacWhinney childes corpus: [['childes', 'Eng-NA', 'MacWhinney']].
    lang: list of str, optional
        Query by language.
        For example, to get transcripts that contain both English and Spanish: ['eng', 'spa']. 
        Legal values: 3-letter language codes based on the ISO 639-3 standard.
    media: list of str, optional
        Query by media type.  For example, to get transcripts with an associated video recording: ['video'].  
        Legal values: 'audio' or 'video'.
    age: list of dict, optional
        Query by participant month age range.  
        For example, to get transcripts with target participants who are 14-18 months old: [{'from': 14, 'to': 18}].
    gender: list of str, optional
        Query by participant gender. 
        For example, to get transcripts with female target participants: ['female'].  Legal values: 'female' or 'male'.
    designType: list of str, optional
        Query by design type.  
        For example, to get transcripts from a longitudinal study: ['long'] Legal values are 'long' for longitudinal studies, 'cross' for cross-sectional studies.
    activityType: list of str, optional
        Query by activity type.  
        For example, to get transcripts where the target participant is engaged in toy play: ['toyplay'].  See the CHAT manual for legal values.
    groupType: list of str, optional
        Query by group type.  
        For example, to get transcripts where the target participant is hearing limited: ['HL'].  See the CHAT manual for legal values.
    auth: list of str, default False
        Determine if user should be prompted to authenticate in order to access protected collections. Defaults to False.

    Returns
    -------
        dict
            Dictionary with two members:
                - colHeadings: List of strings describing columns in data.
                - data: List of lists, where each list represents a table row.

    Each list (row) in 'data' has:
    * Link to view transcript and play any associated media.
    * Corpus path to transcript.
    * Utterance sequence number (starts at 0).
    * Word sequence number within utterance (starts at 0).
    * Speaker’s ID.
    * Speaker’s role.
    * Utterance postcodes.
    * Utterance GEMS.
    * Utterance.
    * Start time of utterance in associated media.
    * End time of utterance in associated media.

    Examples
    --------
    Get utterance info for one transcript:

    tbdb.getUtterances({'corpusName': 'childes', 'corpora': [['childes','Eng-NA','MacWhinney', '010411a']]})
    """

    if auth:
        queryParams['nsAuth'] = _authenticate()

    return _makeReq(queryParams, 'getUtteranceSummary', True)


def getTokens(queryParams, auth=False):
    """
    Get tokens (words) and metadata info of transcripts where each row represents a token.

    Parameters
    ----------
    corpusName: str
        Name of corpus to query.  For example, to search within the childes corpus, corpus='childes'.
    corpora: list of list, optional
        Paths of corpus/corporas to query under corpusName.
        This is a path starting with the corpus name followed by subfolder names leading to a folder for which all transcripts beneath it will be queried.
        For example, to query all transcripts in the MacWhinney childes corpus: [['childes', 'Eng-NA', 'MacWhinney']].
    lang: list of str, optional
        Query by language.
        For example, to get transcripts that contain both English and Spanish: ['eng', 'spa']. 
        Legal values: 3-letter language codes based on the ISO 639-3 standard.
    media: list of str, optional
        Query by media type.  For example, to get transcripts with an associated video recording: ['video'].  
        Legal values: 'audio' or 'video'.
    age: list of dict, optional
        Query by participant month age range.  
        For example, to get transcripts with target participants who are 14-18 months old: [{'from': 14, 'to': 18}].
    gender: list of str, optional
        Query by participant gender. 
        For example, to get transcripts with female target participants: ['female'].  Legal values: 'female' or 'male'.
    designType: list of str, optional
        Query by design type.  
        For example, to get transcripts from a longitudinal study: ['long'] Legal values are 'long' for longitudinal studies, 'cross' for cross-sectional studies.
    activityType: list of str, optional
        Query by activity type.  
        For example, to get transcripts where the target participant is engaged in toy play: ['toyplay'].  See the CHAT manual for legal values.
    groupType: list of str, optional
        Query by group type.  
        For example, to get transcripts where the target participant is hearing limited: ['HL'].  See the CHAT manual for legal values.
    auth: list of str, default False
        Determine if user should be prompted to authenticate in order to access protected collections. Defaults to False.

    Returns
    -------
        dict
            Dictionary with two members:
                - colHeadings: List of strings describing columns in data.
                - data: List of lists, where each list represents a table row.

    Each list (row) in 'data' has:
    * Link to view transcript and play any associated media.
    * Corpus path to transcript.
    * Utterance sequence number (starts at 0).
    * Word sequence number within utterance (starts at 0).
    * Speaker’s role.
    * Speaker’s ID.
    * The word (token).
    * The word’s stem.
    * Part of speech code. (See CHAT manual for descriptions of codes).

    Examples
    --------
    Get token info for one transcript:

    tbdb.getTokens({'corpusName': 'childes', 'corpora': [['childes','Eng-NA','MacWhinney', '010411a']]})
    """

    if auth:
        queryParams['nsAuth'] = _authenticate()

    return _makeReq(queryParams, 'getTokenSummary', True)


def getTokenTypes(queryParams, auth=False):
    """
    Get tokens (word) types and metadata info of transcripts where each row represents a token type.

    Parameters
    ----------
    corpusName: str
        Name of corpus to query.  For example, to search within the childes corpus, corpus='childes'.
    corpora: list of list, optional
        Paths of corpus/corporas to query under corpusName.
        This is a path starting with the corpus name followed by subfolder names leading to a folder for which all transcripts beneath it will be queried.
        For example, to query all transcripts in the MacWhinney childes corpus: [['childes', 'Eng-NA', 'MacWhinney']].
    lang: list of str, optional
        Query by language.
        For example, to get transcripts that contain both English and Spanish: ['eng', 'spa']. 
        Legal values: 3-letter language codes based on the ISO 639-3 standard.
    media: list of str, optional
        Query by media type.  For example, to get transcripts with an associated video recording: ['video'].  
        Legal values: 'audio' or 'video'.
    age: list of dict, optional
        Query by participant month age range.  
        For example, to get transcripts with target participants who are 14-18 months old: [{'from': 14, 'to': 18}].
    gender: list of str, optional
        Query by participant gender. 
        For example, to get transcripts with female target participants: ['female'].  Legal values: 'female' or 'male'.
    designType: list of str, optional
        Query by design type.  
        For example, to get transcripts from a longitudinal study: ['long'] Legal values are 'long' for longitudinal studies, 'cross' for cross-sectional studies.
    activityType: list of str, optional
        Query by activity type.  
        For example, to get transcripts where the target participant is engaged in toy play: ['toyplay'].  See the CHAT manual for legal values.
    groupType: list of str, optional
        Query by group type.  
        For example, to get transcripts where the target participant is hearing limited: ['HL'].  See the CHAT manual for legal values.
    auth: list of str, default False
        Determine if user should be prompted to authenticate in order to access protected collections. Defaults to False.

    Returns
    -------
        dict
            Dictionary with two members:
                - colHeadings: List of strings describing columns in data.
                - data: List of lists, where each list represents a table row.

    Each list (row) in 'data' has:
    * Speaker’s role.
    * The word. Number of occurances of word in selected transcripts.
    * Part of speech (See CHAT manual for descriptions of codes).
    * The word’s stem.

    Examples
    --------
    Get token type info for one transcript:

    tbdb.getTokenTypes({'corpusName': 'childes', 'corpora': [['childes','Eng-NA','MacWhinney', '010411a']]})
    """
    if auth:
        queryParams['nsAuth'] = _authenticate()

    return _makeReq(queryParams, 'getTokenTypes', True)


def getCQL(queryParams, auth=False):
    """
    Queryting by 'CQL' (Corpus Query Language) lets us search for patterns in the selected transcripts. 
    We construct a CQL query by specifying a search pattern of words, lemmas, and parts of speech.

    The 'cqlArr' parameter specifies a pattern to search for in text.  The pattern is built up by appending components that are one of three types:
        - Exact word match ('type': 'word').
        - Match any form of a word ('type': 'lemma').
        - Or part of speech ('type': 'pos').

    Along with type, components have another value, 'freq', specifying how many times an item should appear at that location.
        - Appear once at that location ('freq': 'once').
        - Appear zero or more times at location ('freq': 'zeroPlus').
        - Appear one or more times at location ('freq': 'onePlus').

    We append these two-part (type/freq) components together to search for patterns across corpora.

    Some examples:
        - To find all instances of exactly 'go home':
        'cqlArr': [
            {'type': 'word', 'item': 'go', 'freq': 'once'},
            {'type': 'word', 'item': 'home', 'freq': 'once'}]

        This matches all utterances containing:
        'go home'

    - To find all instances of any form of 'go' followed by 'home', we use 'type': 'lemma' for 'go':
        'cqlArr': [
            {'type': 'lemma', 'item': 'go', 'freq': 'once'},
            {'type': 'word', 'item': 'home', 'freq': 'once'}]

    This matches all utterances containing:
        'go home'
        'goes home'
        'went home'
        'going home'

    - To find all instances of a subject pronoun, followd by any form of 'go', followed by one or more adverbs, followed by 'home':
    'cqlArr': [
        {'type': 'pos', 'item': 'pro:sub', 'freq': 'once'},
        {'type': 'lemma', 'item': 'go', 'freq': 'once'},
        {'type': 'pos', 'item': 'adv', 'freq': 'onePlus'},
        {'type': 'word', 'item': 'home', 'freq': 'once'}]

    This matches all utterances containing:
    'they went back home'
    'they go back home'
    'he went back home'
    'we went back home'
    others...

    There are many 'item' values for part of speech ('type': 'pos').  See the CHAT manual or the CQL tab on TalkBankDB (https://talkbank.org/DB) for legal part-of-speech codes.


    Parameters
    ----------
    cqlArr: list of dict
        Specifies a pattern to search for in text.  See this function description for details.
    corpusName: str
        Name of corpus to query.  For example, to search within the childes corpus, corpus='childes'.
    corpora: list of list, optional
        Paths of corpus/corporas to query under corpusName.
        This is a path starting with the corpus name followed by subfolder names leading to a folder for which all transcripts beneath it will be queried.
        For example, to query all transcripts in the MacWhinney childes corpus: [['childes', 'Eng-NA', 'MacWhinney']].
    lang: list of str, optional
        Query by language.
        For example, to get transcripts that contain both English and Spanish: ['eng', 'spa']. 
        Legal values: 3-letter language codes based on the ISO 639-3 standard.
    media: list of str, optional
        Query by media type.  For example, to get transcripts with an associated video recording: ['video'].  
        Legal values: 'audio' or 'video'.
    age: list of dict, optional
        Query by participant month age range.  
        For example, to get transcripts with target participants who are 14-18 months old: [{'from': 14, 'to': 18}].
    gender: list of str, optional
        Query by participant gender. 
        For example, to get transcripts with female target participants: ['female'].  Legal values: 'female' or 'male'.
    designType: list of str, optional
        Query by design type.  
        For example, to get transcripts from a longitudinal study: ['long'] Legal values are 'long' for longitudinal studies, 'cross' for cross-sectional studies.
    activityType: list of str, optional
        Query by activity type.  
        For example, to get transcripts where the target participant is engaged in toy play: ['toyplay'].  See the CHAT manual for legal values.
    groupType: list of str, optional
        Query by group type.  
        For example, to get transcripts where the target participant is hearing limited: ['HL'].  See the CHAT manual for legal values.
    auth: list of str, default False
        Determine if user should be prompted to authenticate in order to access protected collections. Defaults to False.

    Returns
    -------
        dict
            Dictionary with two members:
                - colHeadings: List of strings describing columns in data.
                - data: List of lists, where each list represents a table row.

    Each list (row) in 'data' has:
    * Speaker’s role.
    * The word. Number of occurances of word in selected transcripts.
    * Part of speech (See CHAT manual for descriptions of codes).
    * The word’s stem.

    Examples
    --------
    CQL query for any form of 'my' followed by any form of 'ball' (each occurring one time) in the 'MacWhinney' collection:

    tbdb.getCQL(
        {
        'corpusName': 'childes',
        'corpora': [['childes', 'Eng-NA', 'MacWhinney']],
        'cqlArr': [{'type': 'lemma', 'item': 'my', 'freq': 'once'}, {'type': 'lemma', 'item': 'ball', 'freq': 'once'}]
        })
    """

    if auth:
        queryParams['nsAuth'] = _authenticate()

    return _makeReq(queryParams, 'cql', True)


def getNgrams(queryParams, auth=False):
    """
    Get n-grams of specified size (n) and type.

    Parameters
    ----------
    nGram: dict
        To search for all n-grams of length 3 of word type: {'size':3, 'type':'word'}. 
        Legal values for 'size' is any positive integer equal to or greater than 1.  
        Legal values for 'type' are:
            - 'word' to return exact word n-grams.
            - 'stem' to return word stem n-grams.
            - 'pos' to return part of speech n-grams.
    corpusName: str
        Name of corpus to query.  For example, to search within the childes corpus, corpus='childes'.
    corpora: list of list, optional
        Paths of corpus/corporas to query under corpusName.
        This is a path starting with the corpus name followed by subfolder names leading to a folder for which all transcripts beneath it will be queried.
        For example, to query all transcripts in the MacWhinney childes corpus: [['childes', 'Eng-NA', 'MacWhinney']].
    lang: list of str, optional
        Query by language.
        For example, to get transcripts that contain both English and Spanish: ['eng', 'spa']. 
        Legal values: 3-letter language codes based on the ISO 639-3 standard.
    media: list of str, optional
        Query by media type.  For example, to get transcripts with an associated video recording: ['video'].  
        Legal values: 'audio' or 'video'.
    age: list of dict, optional
        Query by participant month age range.  
        For example, to get transcripts with target participants who are 14-18 months old: [{'from': 14, 'to': 18}].
    gender: list of str, optional
        Query by participant gender. 
        For example, to get transcripts with female target participants: ['female'].  Legal values: 'female' or 'male'.
    designType: list of str, optional
        Query by design type.  
        For example, to get transcripts from a longitudinal study: ['long'] Legal values are 'long' for longitudinal studies, 'cross' for cross-sectional studies.
    activityType: list of str, optional
        Query by activity type.  
        For example, to get transcripts where the target participant is engaged in toy play: ['toyplay'].  See the CHAT manual for legal values.
    groupType: list of str, optional
        Query by group type.  
        For example, to get transcripts where the target participant is hearing limited: ['HL'].  See the CHAT manual for legal values.
    auth: list of str, default False
        Determine if user should be prompted to authenticate in order to access protected collections. Defaults to False.

    Returns
    -------
        dict
            Dictionary with two members:
                - colHeadings: List of strings describing columns in data.
                - data: List of lists, where each list represents a table row.

    Each list (row) in 'data' has:
    * Speaker’s role.
    * The n-gram (word, stem, or part-of-speech). See CHAT manual for part-of-speech code values.
    * Frequency count of n-gram.

    Examples
    --------
    Get 3-grams for one transcript:

    tbdb.getNgrams(
        {
            'nGram': {'size': '3', 'type': 'word'},
            'corpusName': 'childes',
            'corpora': [['childes', 'Eng-NA', 'MacWhinney', '010411a']]
        })
    """
    if auth:
        queryParams['nsAuth'] = _authenticate()

    return _makeReq(queryParams, 'getNgrams', True)


def getPathTrees():
    """
    Get path tree to every doc in TalkBank.
    This can be useful for:
    - Verifying 'corpora' param passed to query functions by walking down and verifying path in object returned here.
    - GUIs to select paths. 
    - Auto-complete paths.
    """

    return _makeReq({}, 'getPathTrees', False)


def validPath(targetPath):
    """
    Check for valid path
    Can be used by other functions to validate the 'corpora' parameter lists passed to query functions.
    
    Parameters
    ----------
    targetPath: list of str
        List of strings representing path to validate in pathTree.

    Returns
    -------
        bool
            True if targetPath is a valid path.
            False otherwise.

    Examples
    --------
    Example of a valid path.
    
    validPath(['childes', 'childes', 'Clinical']);


    Example of non-existent path.

    validPath(['childes', 'childes', 'somethingThatDoesNotExist']);
    """

    def checkPath(targetPath, pathTree=getPathTrees()):
        # Successfully walked down targetPath in pathTree.
        if len(targetPath) == 0:
            return True

        # If targetPath so far is valid, continue down path.
        if targetPath[0] in pathTree:
            checkPath(targetPath[1:len(targetPath)], pathTree[targetPath[0]])
        else:
            print('Invalid path at: ' + targetPath[0])
            return False

    return checkPath(['respMsg'] + targetPath, getPathTrees())
