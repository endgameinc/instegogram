#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Forked from https://github.com/LevPasha/Instagram-API-python (WTFPL License)

import requests
import random
import json
import hashlib
import hmac
import urllib
import time
from PIL import Image
from time import strftime


class InstagramAPI():

    API_URL = 'https://i.instagram.com/api/v1/'
    USER_AGENT = 'Instagram 8.4.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)'
    IG_SIG_KEY = '3d3d669cedc38f2ea7d198840e0648db3738224a0f661aa6a2c1e77dfa964a1e'
    EXPERIMENTS = 'ig_android_progressive_jpeg,ig_creation_growth_holdout,ig_android_report_and_hide,' + \
                  'ig_android_new_browser,ig_android_enable_share_to_whatsapp,' + \
                  'ig_android_direct_drawing_in_quick_cam_universe,ig_android_huawei_app_badging,' + \
                  'ig_android_universe_video_production,ig_android_asus_app_badging,ig_android_direct_plus_button,' + \
                  'ig_android_ads_heatmap_overlay_universe,ig_android_http_stack_experiment_2016,' + \
                  'ig_android_infinite_scrolling,ig_fbns_blocked,ig_android_white_out_universe,' + \
                  'ig_android_full_people_card_in_user_list,ig_android_post_auto_retry_v7_21,ig_fbns_push,' + \
                  'ig_android_feed_pill,ig_android_profile_link_iab,ig_explore_v3_us_holdout,' + \
                  'ig_android_histogram_reporter,ig_android_anrwatchdog,ig_android_search_client_matching,' + \
                  'ig_android_high_res_upload_2,ig_android_new_browser_pre_kitkat,ig_android_2fac,' + \
                  'ig_android_grid_video_icon,ig_android_white_camera_universe,ig_android_disable_chroma_subsampling,' + \
                  'ig_android_share_spinner,ig_android_explore_people_feed_icon,ig_explore_v3_android_universe,' + \
                  'ig_android_media_favorites,ig_android_nux_holdout,ig_android_search_null_state,' + \
                  'ig_android_react_native_notification_setting,ig_android_ads_indicator_change_universe,' + \
                  'ig_android_video_loading_behavior,ig_android_black_camera_tab,liger_instagram_android_univ,' + \
                  'ig_explore_v3_internal,ig_android_direct_emoji_picker,ig_android_prefetch_explore_delay_time,' + \
                  'ig_android_business_insights_qe,ig_android_direct_media_size,ig_android_enable_client_share,' + \
                  'ig_android_promoted_posts,ig_android_app_badging_holdout,ig_android_ads_cta_universe,' + \
                  'ig_android_mini_inbox_2,ig_android_feed_reshare_button_nux,ig_android_boomerang_feed_attribution,' + \
                  'ig_android_fbinvite_qe,ig_fbns_shared,ig_android_direct_full_width_media,' + \
                  'ig_android_hscroll_profile_chaining,ig_android_feed_unit_footer,ig_android_media_tighten_space,' + \
                  'ig_android_private_follow_request,ig_android_inline_gallery_backoff_hours_universe,' + \
                  'ig_android_direct_thread_ui_rewrite,ig_android_rendering_controls,' + \
                  'ig_android_ads_full_width_cta_universe,ig_video_max_duration_qe_preuniverse,' + \
                  'ig_android_prefetch_explore_expire_time,ig_timestamp_public_test,ig_android_profile,' + \
                  'ig_android_dv2_consistent_http_realtime_response,ig_android_enable_share_to_messenger,' + \
                  'ig_explore_v3,ig_ranking_following,ig_android_pending_request_search_bar,' + \
                  'ig_android_feed_ufi_redesign,ig_android_video_pause_logging_fix,ig_android_default_folder_to_camera,' + \
                  'ig_android_video_stitching_7_23,ig_android_profanity_filter,ig_android_business_profile_qe,' + \
                  'ig_android_search,ig_android_boomerang_entry,ig_android_inline_gallery_universe,' + \
                  'ig_android_ads_overlay_design_universe,ig_android_options_app_invite,' + \
                  'ig_android_view_count_decouple_likes_universe,ig_android_periodic_analytics_upload_v2,' + \
                  'ig_android_feed_unit_hscroll_auto_advance,ig_peek_profile_photo_universe,' + \
                  'ig_android_ads_holdout_universe,ig_android_prefetch_explore,ig_android_direct_bubble_icon,' + \
                  'ig_video_use_sve_universe,ig_android_inline_gallery_no_backoff_on_launch_universe,' + \
                  'ig_android_image_cache_multi_queue,ig_android_camera_nux,ig_android_immersive_viewer,' + \
                  'ig_android_dense_feed_unit_cards,ig_android_sqlite_dev,ig_android_exoplayer,ig_android_add_to_last_post,' + \
                  'ig_android_direct_public_threads,ig_android_prefetch_venue_in_composer,ig_android_bigger_share_button,' + \
                  'ig_android_dv2_realtime_private_share,ig_android_non_square_first,ig_android_video_interleaved_v2,' + \
                  'ig_android_follow_search_bar,ig_android_last_edits,ig_android_video_download_logging,' + \
                  'ig_android_ads_loop_count_universe,ig_android_swipeable_filters_blacklist,' + \
                  'ig_android_boomerang_layout_white_out_universe,ig_android_ads_carousel_multi_row_universe,' + \
                  'ig_android_mentions_invite_v2,ig_android_direct_mention_qe,' + \
                  'ig_android_following_follower_social_context'
    SIG_KEY_VERSION = '4'
    IGDataPath = 'data/'

    # username            # Instagram username
    # password            # Instagram password
    # debug               # Debug
    # uuid                # UUID
    # device_id           # Device ID
    # username_id         # Username ID
    # token               # _csrftoken
    # isLoggedIn          # Session status
    # rank_token          # Rank token
    # IGDataPath          # Data storage path

    def __init__(self, username, password, debug=False, IGDataPath=None):
        m = hashlib.md5()
        m.update(username.encode('utf-8') + password.encode('utf-8'))
        self.device_id = self.generateDeviceId(m.hexdigest())
        self.setUser(username, password)
        self.isLoggedIn = False
        self.LastResponse = None
        self.setUser(username, password)
        self.login()

    def setUser(self, username, password):
        self.username = username
        self.password = password
        self.uuid = self.generateUUID(True)

    def login(self, force=False):
        if (not self.isLoggedIn or force):
            self.s = requests.Session()
            # if you need proxy make something like this:
            # self.s.proxies = {"https" : "http://proxyip:proxyport"}
            if (self.SendRequest('si/fetch_headers/?challenge_type=signup&guid=' + self.generateUUID(False),
                                 None, True)):
                data = {'phone_id': self.generateUUID(True),
                        '_csrftoken': self.LastResponse.cookies['csrftoken'],
                        'username': self.username,
                        'guid': self.uuid,
                        'device_id': self.device_id,
                        'password': self.password,
                        'login_attempt_count': '0'}

                attempt = self.SendRequest('accounts/login/', self.generateSignature(json.dumps(data)), True)
                if (attempt):
                    print self.LastJson
                    self.sessionid = self.s.cookies['sessionid']
                    self.isLoggedIn = True
                    self.username_id = self.LastJson["logged_in_user"]["pk"]
                    self.rank_token = "%s_%s" % (self.username_id, self.uuid)
                    self.token = self.LastResponse.cookies["csrftoken"]

                    self.syncFeatures()
                    print ("Login success!\n")
                    return True

    def syncFeatures(self):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.username_id,
            'id': self.username_id,
            '_csrftoken': self.token,
            'experiments': self.EXPERIMENTS
            })
        return self.SendRequest('qe/sync/', self.generateSignature(data))

    def expose(self):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.username_id,
            'id': self.username_id,
            '_csrftoken': self.token,
            'experiment': 'ig_android_profile_contextual_feed'
            })
        return self.SendRequest('qe/expose/', self.generateSignature(data))

    def buildBody(self, upload_id, uuid, token, filepath):
        boundary = uuid

        bodies = [
            {
                'type': 'form-data',
                'name': 'upload_id',
                'data': upload_id,
            },
            {
                'type': 'form-data',
                'name': '_uuid',
                'data': uuid,
            },
            {
                'type': 'form-data',
                'name': '_csrftoken',
                'data': token,
            },
            {
                'type': 'form-data',
                'name': 'image_compression',
                'data': '{"lib_name":"jt","lib_version":"1.3.0","quality":"70"}',
            },
            {
                'type': 'form-data',
                'name': 'photo',
                'data': open(filepath, 'rb').read(),
                'filename': 'pending_media_'+str(int((time.time()*1000)))+'.jpg',
                'headers': ['Content-Transfer-Encoding: binary',
                            'Content-type: application/octet-stream'],
            },
        ]

        body = ''
        for b in bodies:
            body += '--' + boundary + '\r\n'
            body += 'Content-Disposition: ' + b['type'] + '; name="' + b['name'] + '"'
            if (b.get('filename', False)):
                # ext = pathinfo(b['filename'], PATHINFO_EXTENSION);
                body += '; filename="' + 'pending_media_' + str(int((time.time()*1000))) + '.jpg"'
            if (b.get('headers', False)):
                for header in b['headers']:
                    body += "\r\n" + header
            body += "\r\n\r\n" + b['data'] + "\r\n"
        body += '--' + boundary + '--'
        return body

    def uploadPhoto(self, filepath, caption=None, upload_id=None):
        if not upload_id:
            upload_id = str(int((time.time()*1000)))

        data = self.buildBody(upload_id, self.uuid, self.token, filepath)

        endpoint = 'https://i.instagram.com/api/v1/upload/photo/'

        cookies = [c[0]+'='+c[1]+';' for c in self.s.cookies.items()]
        cookie_str = ' '.join(cookies)

        headers = {'Connection': 'close',
                   'Accept': '*/*',
                   'Content-type': 'multipart/form-data; boundary='+self.uuid,
                   'Content-Length': str(len(data)),
                   'Cookie': cookie_str,
                   'Cookie2': '$Version=1',
                   'Accept-Language': 'en-US',
                   'Accept-Encoding': 'gzip',
                   'User-Agent': self.USER_AGENT,
                   }

        resp = self.s.post(endpoint, data=data, headers=headers)
        print json.loads(resp.text)

        self.expose()
        self.configure(upload_id, filepath, caption)

        return self.s.cookies

    def configure(self, upload_id, filepath, caption):
        im = Image.open(filepath)
        size = im.size

        post = json.dumps({
            'upload_id': upload_id,
            'camera_model': 'HM1S',
            'source_type': 3,
            'date_time_original': strftime("%Y:%m:%d %H:%M:%S"),
            'camera_make': 'XIAOMI',
            'edits': {
                'crop_original_size': [size[0], size[1]],
                'crop_zoom': 1.3333334,
                'crop_center': [0.0, -0.0],
            },
            'extra': {
                'source_width': size[1],
                'source_height': size[0],
            },
            'device': {
                'manufacturer': 'Xiaomi',
                'model': 'HM 1SW',
                'android_version': 18,
                'android_release': '4.3',
            },
            '_csrftoken': self.token,
            '_uuid': self.uuid,
            '_uid': self.username_id,
            'caption': caption,
            })

        post = post.replace('"crop_center":[0,0]', '"crop_center":[0.0,-0.0]')

        return self.SendRequest('media/configure/', self.generateSignature(post))

# ###### API calls not used by Instegogram ####### #

    # def logout(self):
    #     logout = self.SendRequest('accounts/logout/')
    #     # TODO Instagram.php 180-185

    # def autoCompleteUserList(self):
    #     return self.SendRequest('friendships/autocomplete_user_list/')

    # def timelineFeed(self):
    #     return self.SendRequest('feed/timeline/')

    # def megaphoneLog(self):
    #     return self.SendRequest('megaphone/log/')

    # def uploadVideo(self, video, caption = None):
    #     # TODO Instagram.php 290-415
    #     return False

    # def direct_share(self, media_id, recipients, text = None):
    #     # TODO Instagram.php 420-490
    #     return False

    # def configureVideo(upload_id, video, caption = ''):
    #     # TODO Instagram.php 490-530
    #     return False

    # def editMedia(self, mediaId, captionText = ''):
    #     data = json.dumps({
    #     '_uuid'        : self.uuid,
    #     '_uid'         : self.username_id,
    #     '_csrftoken'   : self.token,
    #     'caption_text' : captionText
    #     })
    #     return self.SendRequest('media/'+ str(mediaId) +'/edit_media/', self.generateSignature(data))

    # def removeSelftag(self, mediaId):
    #     data = json.dumps({
    #     '_uuid'        : self.uuid,
    #     '_uid'         : self.username_id,
    #     '_csrftoken'   : self.token
    #     })
    #     return self.SendRequest('media/'+ str(mediaId) +'/remove/', self.generateSignature(data))

    # def mediaInfo(self, mediaId):
    #     data = json.dumps({
    #     '_uuid'        : self.uuid,
    #     '_uid'         : self.username_id,
    #     '_csrftoken'   : self.token,
    #     'media_id'     : mediaId
    #     })
    #     return self.SendRequest('media/'+ str(mediaId) +'/info/', self.generateSignature(data))

    # def deleteMedia(self, mediaId):
    #     data = json.dumps({
    #     '_uuid'        : self.uuid,
    #     '_uid'         : self.username_id,
    #     '_csrftoken'   : self.token,
    #     'media_id'     : mediaId
    #     })
    #     return self.SendRequest('media/'+ str(mediaId) +'/delete/', self.generateSignature(data))

    # def comment(self, mediaId, commentText):
    #     data = json.dumps({
    #     '_uuid'        : self.uuid,
    #     '_uid'         : self.username_id,
    #     '_csrftoken'   : self.token,
    #     'comment_text' : commentText
    #     })
    #     return self.SendRequest('media/'+ str(mediaId) +'/comment/', self.generateSignature(data))

    # def deleteComment(self, mediaId, captionText, commentId):
    #     data = json.dumps({
    #     '_uuid'        : self.uuid,
    #     '_uid'         : self.username_id,
    #     '_csrftoken'   : self.token,
    #     'caption_text' : captionText
    #     })
        # return self.SendRequest('media/'+ str(mediaId) +'/comment/'+ str(commentId) +'/delete/',
        #                         self.generateSignature(data))

    # def changeProfilePicture(self, photo):
    #     # TODO Instagram.php 705-775
    #     return False

    # def removeProfilePicture(self):
    #     data = json.dumps({
    #     '_uuid'        : self.uuid,
    #     '_uid'         : self.username_id,
    #     '_csrftoken'   : self.token
    #     })
    #     return self.SendRequest('accounts/remove_profile_picture/', self.generateSignature(data))

    # def setPrivateAccount(self):
    #     data = json.dumps({
    #     '_uuid'        : self.uuid,
    #     '_uid'         : self.username_id,
    #     '_csrftoken'   : self.token
    #     })
    #     return self.SendRequest('accounts/set_private/', self.generateSignature(data))

    # def setPublicAccount(self):
    #     data = json.dumps({
    #     '_uuid'        : self.uuid,
    #     '_uid'         : self.username_id,
    #     '_csrftoken'   : self.token
    #     })
    #     return self.SendRequest('accounts/set_public/', self.generateSignature(data))

    # def getProfileData(self):
    #     data = json.dumps({
    #     '_uuid'        : self.uuid,
    #     '_uid'         : self.username_id,
    #     '_csrftoken'   : self.token
    #     })
    #     return self.SendRequest('accounts/current_user/?edit=true', self.generateSignature(data))

    # def editProfile(self, url, phone, first_name, biography, email, gender):
    #     data = json.dumps({
    #     '_uuid'        : self.uuid,
    #     '_uid'         : self.username_id,
    #     '_csrftoken'   : self.token,
    #     'external_url' : url,
    #     'phone_number' : phone,
    #     'username'     : self.username,
    #     'full_name'    : first_name,
    #     'biography'    : biography,
    #     'email'        : email,
    #     'gender'       : gender,
    #     })
    #     return self.SendRequest('accounts/edit_profile/', self.generateSignature(data))

    # def getUsernameInfo(self, usernameId):
    #     return self.SendRequest('users/'+ str(usernameId) +'/info/')

    # def getSelfUsernameInfo(self):
    #     return self.getUsernameInfo(self.username_id)

    # def getRecentActivity(self):
    #     activity = self.SendRequest('news/inbox/?')
    #     # TODO Instagram.php 911-925
    #     return activity

    # def getFollowingRecentActivity(self):
    #     activity = self.SendRequest('news/?')
    #     # TODO Instagram.php 935-945
    #     return activity

    # def getv2Inbox(self):
    #     inbox = self.SendRequest('direct_v2/inbox/?')
    #     # TODO Instagram.php 950-960
    #     return inbox

    # def getUserTags(self, usernameId):
    #     tags = self.SendRequest('usertags/'+ str(usernameId) +'/feed/?rank_token='+ \
    #                             str(self.rank_token) +'&ranked_content=true&')
    #     # TODO Instagram.php 975-985
    #     return tags

    # def getSelfUserTags(self):
    #     return self.getUserTags(self.username_id)

    # def tagFeed(self, tag):
    #     userFeed = self.SendRequest('feed/tag/'+ str(tag) +'/?rank_token=' + \
    #                                 str(self.rank_token) + '&ranked_content=true&')
    #     # TODO Instagram.php 1000-1015
    #     return userFeed

    # def getMediaLikers(self, mediaId):
    #     likers = self.SendRequest('media/'+ str(mediaId) +'/likers/?')
    #     # TODO Instagram.php 1025-1035
    #     return likers

    # def getGeoMedia(self, usernameId):
    #     locations = self.SendRequest('maps/user/'+ str(usernameId) +'/')
    #     # TODO Instagram.php 1050-1060
    #     return locations

    # def getSelfGeoMedia(self):
    #     return self.getGeoMedia(self.username_id)

    # def fbUserSearch(self, query):
    #     query = self.SendRequest('fbsearch/topsearch/?context=blended&query='+ str(query) + \
    #                              '&rank_token='+ str(self.rank_token))
    #     # TODO Instagram.php 1080-1090
    #     return query

    # def searchUsers(self, query):
    #     query = self.SendRequest('users/search/?ig_sig_key_version='+ str(self.SIG_KEY_VERSION)
    #             +'&is_typeahead=true&query='+ str(query) +'&rank_token='+ str(self.rank_token))
    #     # TODO Instagram.php 1100-1110
    #     return query

    # def searchUsername(self, usernameName):
    #     query = self.SendRequest('users/'+ str(usernameName) +'/usernameinfo/')
    #     # TODO Instagram.php 1080-1090
    #     return query

    # def syncFromAdressBook(self, contacts):
    #     return self.SendRequest('address_book/link/?include=extra_display_name,thumbnails', json.dumps(contacts))

    # def searchTags(self, query):
    #     query = self.SendRequest('tags/search/?is_typeahead=true&q='+ str(query) + \
    #                              '&rank_token='+ str(self.rank_token))
    #     # TODO Instagram.php 1160-1170
    #     return query

    # def getTimeline(self):
    #     query = self.SendRequest('feed/timeline/?rank_token='+ str(self.rank_token) +'&ranked_content=true&')
    #     # TODO Instagram.php 1180-1190
    #     return query

    # def getUserFeed(self, usernameId, maxid = '', minTimestamp = None):
    #     # TODO Instagram.php 1200-1220
    #     return False

    # def getSelfUserFeed(self):
    #     return self.getUserFeed(self.username_id)

    # def getHashtagFeed(self, hashtagString, maxid = ''):
    #     # TODO Instagram.php 1230-1250
    #     return False

    # def searchLocation(self, query):
    #     locationFeed = self.SendRequest('fbsearch/places/?rank_token='+ str(self.rank_token) +'&query=' + str(query))
    #     # TODO Instagram.php 1250-1270
    #     return locationFeed

    # def getLocationFeed(self, locationId, maxid = ''):
    #     # TODO Instagram.php 1280-1300
    #     return False

    # def getPopularFeed(self):
    #     popularFeed = self.SendRequest('feed/popular/?people_teaser_supported=1&rank_token='+ \
    #                                    str(self.rank_token) +'&ranked_content=true&')
    #     # TODO Instagram.php 1315-1325
    #     return popularFeed

    # def getUserFollowings(self, usernameId, maxid = ''):
    #     return self.SendRequest('friendships/'+ str(usernameId) +'/following/?max_id='+ str(maxid)
    #         +'&ig_sig_key_version='+ self.SIG_KEY_VERSION +'&rank_token='+ self.rank_token)

    # def getSelfUsersFollowing(self):
    #     return self.getUserFollowings(self.username_id)

    # def getUserFollowers(self, usernameId, maxid = ''):
    #     return self.SendRequest('friendships/'+ str(usernameId) +'/followers/?max_id='+ str(maxid)
    #         +'&ig_sig_key_version='+ self.SIG_KEY_VERSION +'&rank_token='+ self.rank_token)

    # def getSelfUserFollowers(self):
    #     return self.getUserFollowers(self.username_id)

    # def like(self, mediaId):
    #     data = json.dumps({
    #         '_uuid': self.uuid,
    #         '_uid': self.username_id,
    #         '_csrftoken': self.token,
    #         'media_id': mediaId
    #         })
    #     return self.SendRequest('media/' + str(mediaId) + '/like/', self.generateSignature(data))

    # def unlike(self, mediaId):
    #     data = json.dumps({
    #     '_uuid'         : self.uuid,
    #     '_uid'          : self.username_id,
    #     '_csrftoken'    : self.token,
    #     'media_id'      : mediaId
    #     })
    #     return self.SendRequest('media/'+ str(mediaId) +'/unlike/', self.generateSignature(data))

    # def getMediaComments(self, mediaId):
    #     return self.SendRequest('media/'+ mediaId +'/comments/?')

    # def setNameAndPhone(self, name = '', phone = ''):
    #     data = json.dumps({
    #     '_uuid'         : self.uuid,
    #     '_uid'          : self.username_id,
    #     'first_name'    : name,
    #     'phone_number'  : phone,
    #     '_csrftoken'    : self.token
    #     })
    #     return self.SendRequest('accounts/set_phone_and_name/', self.generateSignature(data))

    # def getDirectShare(self):
    #     return self.SendRequest('direct_share/inbox/?')

    # def backup(self):
    #     # TODO Instagram.php 1470-1485
    #     return False

    # def follow(self, userId):
    #     data = json.dumps({
    #     '_uuid'         : self.uuid,
    #     '_uid'          : self.username_id,
    #     'user_id'       : userId,
    #     '_csrftoken'    : self.token
    #     })
    #     return self.SendRequest('friendships/create/'+ str(userId) +'/', self.generateSignature(data))

    # def unfollow(self, userId):
    #     data = json.dumps({
    #     '_uuid'         : self.uuid,
    #     '_uid'          : self.username_id,
    #     'user_id'       : userId,
    #     '_csrftoken'    : self.token
    #     })
    #     return self.SendRequest('friendships/destroy/'+ str(userId) +'/', self.generateSignature(data))

    # def block(self, userId):
    #     data = json.dumps({
    #     '_uuid'         : self.uuid,
    #     '_uid'          : self.username_id,
    #     'user_id'       : userId,
    #     '_csrftoken'    : self.token
    #     })
    #     return self.SendRequest('friendships/block/'+ str(userId) +'/', self.generateSignature(data))

    # def unblock(self, userId):
    #     data = json.dumps({
    #     '_uuid'         : self.uuid,
    #     '_uid'          : self.username_id,
    #     'user_id'       : userId,
    #     '_csrftoken'    : self.token
    #     })
    #     return self.SendRequest('friendships/unblock/'+ str(userId) +'/', self.generateSignature(data))

    # def userFriendship(self, userId):
    #     data = json.dumps({
    #     '_uuid'         : self.uuid,
    #     '_uid'          : self.username_id,
    #     'user_id'       : userId,
    #     '_csrftoken'    : self.token
    #     })
    #     return self.SendRequest('friendships/show/'+ str(userId) +'/', self.generateSignature(data))

    # def getLikedMedia(self):
    #     return self.SendRequest('feed/liked/?')

    def generateSignature(self, data):
        post_string = 'ig_sig_key_version=' + self.SIG_KEY_VERSION + \
                      '&signed_body=' + hmac.new(self.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() +  \
                      '.' + urllib.quote(data)
        return post_string

    def generateDeviceId(self, seed):
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    def generateUUID(self, type):
        uuid = '%04x%04x-%04x-%04x-%04x-%04x%04x%04x' % (random.randint(0, 0xffff),
                                                         random.randint(0, 0xffff), random.randint(0, 0xffff),
                                                         random.randint(0, 0x0fff) | 0x4000,
                                                         random.randint(0, 0x3fff) | 0x8000,
                                                         random.randint(0, 0xffff), random.randint(0, 0xffff),
                                                         random.randint(0, 0xffff))
        if (type):
            return uuid
        else:
            return uuid.replace('-', '')

    def SendRequest(self, endpoint, post=None, login=False):
        #        return self.SendRequest('media/upload/', self.generateSignature(data),  post=photo)
        if (not self.isLoggedIn and not login):
            raise Exception("Not logged in!\n")
            return

        self.s.headers.update({'Connection': 'closed',
                               'Accept': '*/*',
                               'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                               'Cookie2': '$Version=1',
                               'Accept-Language': 'en-US',
                               'User-Agent': self.USER_AGENT})

        if (post):  # POST
            response = self.s.post(self.API_URL + endpoint, post)  # , verify=False
        else:  # GET
            response = self.s.get(self.API_URL + endpoint)  # , verify=False

        if response.status_code == 200:
            self.LastResponse = response
            self.LastJson = json.loads(response.text)
            return True
        else:
            print ("Request return " + str(response.status_code) + " error!")
            return False
