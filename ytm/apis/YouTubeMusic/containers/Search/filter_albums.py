from ..... import utils as ytm_utils
from ... import containers

__all__ = __name__.split('.')[-1:]

def filter_albums(self, update=True):
    filter = 'albums'
    params = ytm_utils.get_nested(self, 'results', filter, 'params')
    items = ytm_utils.get_nested(self, 'results', filter, 'items', default=[])
    query = ytm_utils.get_nested(self, 'query')

    if not params or not query: return # raise

    data = self.api.base.search \
    (
        query = query,
        params = params,
    )

    # Compat, so parser knows what each item represents
    shelves = ytm_utils.get_nested(data, 'contents', 'sectionListRenderer', 'contents', default=())

    for shelf in shelves:
        shelf['musicShelfRenderer']['title'] = \
        {
            'runs': \
            [
                {
                    'text': filter.title(),
                },
            ],
        }

    parsed_data = self._parse(data)

    filtered_data = ytm_utils.get_nested(parsed_data, 'results', filter)
    filtered_items = ytm_utils.get_nested(filtered_data, 'items')

    # parsed_data['query'] = query
    # filtered_data['params'] = params

    parsed_items = ytm_utils.get_nested(parsed_data, 'results', filter, 'items', default=[])

    if update and items:
        items.extend(parsed_items[len(items):])

    container = containers.SearchAlbums(self.api, filtered_items)

    container._continuation = ytm_utils.get_nested(filtered_data, 'continuation')

    # container._continuation = parsed_data['']

    return container
