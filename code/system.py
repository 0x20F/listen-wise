from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager


async def get_media_info():
    sessions = await MediaManager.request_async()

    current_session = sessions.get_current_session()
    if current_session:
        info = await current_session.try_get_media_properties_async()

        info_dict = {song_attr: info.__getattribute__(
            song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        info_dict['genres'] = list(info_dict['genres'])

        return info_dict

    return None