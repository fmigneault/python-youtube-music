'''
Module containing the method: browse
'''

import copy
from .. import constants
from .. import decorators

@decorators.catch
def browse \
        (
            self:         object,
            browse_id:    str = None,
            page_type:    str = None,
            continuation: str = None,
            params:       str = None,
        ) -> dict:
    '''
    Return browse data.

    Args:
        self: Class instance
        browse_id: Browse id
            Example: 'MPREb_GFKho1A5P3G'
        page_type: Page type
            Example: 'MUSIC_PAGE_TYPE_ALBUM'
        continuation: Continuation
            Example: '4qmFsgKMARIMRkVtdXNpY19ob2...'
        params: Params
            Example: 'wAEB'

    Returns:
        Browse data

    Example:
        >>> api = ytm.BaseYouTubeMusic()
        >>>
        >>> data = api.browse \
        (
        	browse_id = 'VLPL4fGSI1pDJn5kI81J1fYWK5eZRl1zJ5kM',
        	page_type = 'MUSIC_PAGE_TYPE_PLAYLIST',
        )

        >>>
        >>> data['header']['musicDetailHeaderRenderer']['title']
        {'runs': [{'text': 'Top 100 Music Videos Global'}]}
        >>>
    '''

    url = self._url_api(constants.ENDPOINT_YTM_API_BROWSE)

    request_params = copy.deepcopy(constants.URL_PARAMS)

    if continuation:
        request_params['continuation'] = continuation
        request_params['ctoken']       = continuation

    payload = copy.deepcopy(constants.PAYLOAD)

    if browse_id:
        payload['browseId'] = browse_id

    if params:
        payload['params'] = params

    if page_type:
        payload['browseEndpointContextSupportedConfigs'] = \
        {
            'browseEndpointContextMusicConfig': \
            {
                'pageType': page_type,
            }
        }

    resp = self.session.post \
    (
        url    = url,
        params = request_params,
        json   = payload,
    )

    data = resp.json()

    return data
