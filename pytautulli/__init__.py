"""
A python module to get information from Tautulli.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import asyncio
import logging
import socket

import aiohttp
import async_timeout


_LOGGER = logging.getLogger(__name__)
_BASE_URL = '{schema}://{host}:{port}/api/v2?apikey={api_key}&cmd='


class Tautulli(object):
    """A class for handling connections with a Tautulli instance."""

    def __init__(self, host, port, api_key, loop, session, ssl=False):
        """Initialize the connection to a Tautulli instance."""
        self._loop = loop
        self._session = session
        self.api_key = api_key
        self.schema = 'https' if ssl else 'http'
        self.host = host
        self.port = port
        self.connection = None
        self.tautulli_session_data = {}
        self.tautulli_home_data = {}
        self.base_url = _BASE_URL.format(schema=self.schema,
                                         host=self.host,
                                         port=self.port,
                                         api_key=self.api_key)

    async def test_connection(self):
        """Test the connection to Tautulli."""
        cmd = 'get_server_friendly_name'
        url = self.base_url + cmd
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(url)
                self.connection = await response.json()
            logger("Status from Tautulli: " + str(response.status))

        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
            msg = "Can not load data from Tautulli: {}".format(url)
            logger(msg, 40)

    async def get_data(self):
        """Get Tautulli data."""
        try:
            await self.get_session_data()
            await self.get_home_data()
        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
            msg = "Can not load data from Tautulli."
            logger(msg, 40)

    async def get_session_data(self):
        """Get Tautulli sessions."""
        cmd = 'get_activity'
        url = self.base_url + cmd
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(url)

            logger("Status from Tautulli: " + str(response.status))
            self.tautulli_session_data = await response.json()
            logger(self.tautulli_session_data)

        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
            msg = "Can not load data from Tautulli: {}".format(url)
            logger(msg, 40)

    async def get_home_data(self):
        """Get Tautulli home stats."""
        cmd = 'get_home_stats'
        url = self.base_url + cmd
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(url)

            logger("Status from Tautulli: " + str(response.status))
            self.tautulli_home_data = await response.json()
            logger(self.tautulli_home_data)

        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
            msg = "Can not load data from Tautulli: {}".format(url)
            logger(msg, 40)

    @property
    def connection_status(self):
        """Return the server stats from Tautulli."""
        if self.connection['response']['message']:
            return_value = False
        else:
            return_value = True
        return return_value

    @property
    def session_data(self):
        """Return data from Tautulli."""
        return self.tautulli_session_data['response']['data']

    @property
    def home_data(self):
        """Return data from Tautulli."""
        return self.tautulli_home_data['response']['data']


def custom_activity(alist):
    """Create additional activitie keys."""
    if alist['media_type'] == 'episode':
        senum = ('S{0}'.format(alist['parent_media_index'].zfill(2)) +
                 'E{0}'.format(alist['media_index'].zfill(2)))
        alist['senum'] = senum
        alist['show_senum'] = alist['grandparent_title'] + ' ' + senum
        alist['s_senum_e'] = (alist['grandparent_title'] +
                              ' ' + senum + ' ' + alist['title'])
        alist['magic_title'] = alist['s_senum_e']
    elif alist['media_type'] == 'movie':
        alist['magic_title'] = alist['full_title']
    return alist


def default_activity_attributes():
    """Return default values for the activity_list."""
    output = {}
    alist = ['_cache_time', 'actors', 'added_at', 'allow_guest', 'art',
             'aspect_ratio', 'audience_rating', 'audio_bitrate',
             'audio_bitrate_mode', 'audio_channel_layout', 'audio_channels',
             'audio_codec', 'audio_decision', 'audio_language',
             'audio_language_code', 'audio_profile', 'audio_sample_rate',
             'bandwidth', 'banner', 'bif_thumb', 'bitrate', 'channel_stream',
             'children_count', 'collections', 'container', 'content_rating',
             'deleted_user', 'device', 'directors', 'do_notify', 'duration',
             'email', 'file', 'file_size', 'full_title', 'genres',
             'grandparent_rating_key', 'grandparent_thumb',
             'grandparent_title', 'guid', 'height', 'id', 'indexes',
             'ip_address', 'ip_address_public', 'is_admin', 'is_allow_sync',
             'is_home_user', 'is_restricted', 'keep_history', 'labels',
             'last_viewed_at', 'library_name', 'live', 'live_uuid', 'local',
             'location', 'machine_id', 'media_index', 'media_type',
             'optimized_version', 'optimized_version_profile',
             'optimized_version_title', 'original_title',
             'originally_available_at', 'parent_media_index',
             'parent_rating_key', 'parent_thumb', 'parent_title', 'platform',
             'platform_name', 'platform_version', 'player', 'product',
             'product_version', 'profile', 'progress_percent',
             'quality_profile', 'rating', 'rating_key', 'relay', 's_senum_e',
             'section_id', 'senum', 'session_id', 'session_key',
             'shared_libraries', 'show_senum', 'sort_title', 'state',
             'stream_aspect_ratio', 'stream_audio_bitrate',
             'stream_audio_bitrate_mode', 'stream_audio_channel_layout',
             'stream_audio_channel_layout_', 'stream_audio_channels',
             'stream_audio_codec', 'stream_audio_decision',
             'stream_audio_language', 'stream_audio_language_code',
             'stream_audio_sample_rate', 'stream_bitrate', 'stream_container',
             'stream_container_decision', 'stream_duration',
             'stream_subtitle_codec', 'stream_subtitle_container',
             'stream_subtitle_decision', 'stream_subtitle_forced',
             'stream_subtitle_format', 'stream_subtitle_language',
             'stream_subtitle_language_code', 'stream_subtitle_location',
             'stream_video_bit_depth', 'stream_video_bitrate',
             'stream_video_codec', 'stream_video_codec_level',
             'stream_video_decision', 'stream_video_framerate',
             'stream_video_height', 'stream_video_language',
             'stream_video_language_code', 'stream_video_ref_frames',
             'stream_video_resolution', 'stream_video_width', 'studio',
             'subtitle_codec', 'subtitle_container', 'subtitle_decision',
             'subtitle_forced', 'subtitle_format', 'subtitle_language',
             'subtitle_language_code', 'subtitle_location', 'subtitles',
             'summary', 'synced_version', 'synced_version_profile', 'tagline',
             'throttled', 'thumb', 'title', 'transcode_audio_channels',
             'transcode_audio_codec', 'transcode_container',
             'transcode_decision', 'transcode_height', 'transcode_hw_decode',
             'transcode_hw_decode_title', 'transcode_hw_decoding',
             'transcode_hw_encode', 'transcode_hw_encode_title',
             'transcode_hw_encoding', 'transcode_hw_full_pipeline',
             'transcode_hw_requested', 'transcode_key', 'transcode_progress',
             'transcode_protocol', 'transcode_speed', 'transcode_throttled',
             'transcode_video_codec', 'transcode_width', 'type', 'updated_at',
             'user', 'user_id', 'user_rating', 'user_thumb', 'username',
             'video_bit_depth', 'video_bitrate', 'video_codec',
             'video_codec_level', 'video_decision', 'video_frame_rate',
             'video_framerate', 'video_height', 'video_language',
             'video_language_code', 'video_profile', 'video_ref_frames',
             'video_resolution', 'video_width', 'view_offset', 'width',
             'writers', 'year']
    for key in alist:
        output[key] = ""
    return output


def logger(message, level=10):
    """Handle logging."""
    logging.getLogger(__name__).log(level, str(message))

    # Enable this for local debug:
    # print('Log level: "' + str(level) + '", message: "' + str(message) + '"')
