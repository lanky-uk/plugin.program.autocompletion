# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details


import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests
import json
import urllib
import AutoCompletion

ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')
PORT = int(ADDON.getSetting('port'))

def get_xbmc_json(method, params):
    headers = {'content-type': 'application/json'}
    xbmc_host = 'localhost'
    xbmc_port = PORT
    xbmc_json_rpc_url = "http://" + xbmc_host + ":" + str(xbmc_port) + "/jsonrpc"
    payload = {"jsonrpc":"2.0","method":method,"params":params,"id":1}
    url_param = urllib.urlencode({'request': json.dumps(payload)})
    response = requests.get(xbmc_json_rpc_url + '?' + url_param, 
                        headers=headers)
    return json.loads(response.text)

def start_info_actions(infos, params):
    for info in infos:
        if info == 'autocomplete':
            listitems = AutoCompletion.get_autocomplete_items(params["id"], params.get("limit", 10))
        elif info == 'selectautocomplete':
            resolve_url(params.get("handle"))
            try:
                window_id = xbmcgui.getCurrentWindowDialogId()
                window = xbmcgui.Window(window_id)
            except:
                return None
            window.setFocusId(300)
            get_xbmc_json(method="Input.SendText",params={"text":params.get("id"),"done":False})
            return None
        pass_list_to_skin(data=listitems,
                          handle=params.get("handle", ""),
                          limit=params.get("limit", 20))


def pass_list_to_skin(data=[], handle=None, limit=False):
    if data and limit and int(limit) < len(data):
        data = data[:int(limit)]
    if not handle:
        return None
    if data:
        items = create_listitems(data)
        items = [(i.getProperty("path"), i, bool(i.getProperty("directory"))) for i in items]
        xbmcplugin.addDirectoryItems(handle=handle,
                                     items=items,
                                     totalItems=len(items))
    xbmcplugin.endOfDirectory(handle)


def create_listitems(data=None):
    if not data:
        return []
    itemlist = []
    for (count, result) in enumerate(data):
        listitem = xbmcgui.ListItem('%s' % (str(count)))
        for (key, value) in result.iteritems():
            if not value:
                continue
            value = unicode(value)
            if key.lower() in ["label"]:
                listitem.setLabel(value)
            elif key.lower() in ["search_string"]:
                path = "plugin://plugin.program.autocompletion/?info=selectautocomplete&&id=%s" % value
                listitem.setPath(path=path)
                listitem.setProperty('path', path)
        listitem.setProperty("index", str(count))
        itemlist.append(listitem)
    return itemlist


def resolve_url(handle):
    if handle:
        xbmcplugin.setResolvedUrl(handle=int(handle),
                                  succeeded=False,
                                  listitem=xbmcgui.ListItem())


class Main:

    def __init__(self):
        xbmc.log("version %s started" % ADDON_VERSION)
        self._parse_argv()
        if self.infos:
            start_info_actions(self.infos, self.params)

    def _parse_argv(self):
        args = sys.argv[2][1:]
        self.handle = int(sys.argv[1])
        self.infos = []
        self.params = {"handle": self.handle}
        if args.startswith("---"):
            delimiter = "&"
            args = args[3:]
        else:
            delimiter = "&&"
        for arg in args.split(delimiter):
            param = arg.replace('"', '').replace("'", " ")
            if param.startswith('info='):
                self.infos.append(param[5:])
            else:
                try:
                    self.params[param.split("=")[0].lower()] = "=".join(param.split("=")[1:]).strip()
                except:
                    pass

if (__name__ == "__main__"):
    Main()
xbmc.log('finished')
