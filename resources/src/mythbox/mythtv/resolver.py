#
#  MythBox for XBMC - http://mythbox.googlecode.com
#  Copyright (C) 2009 analogue@yahoo.com
# 
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

import logging
import md5

from mythbox.filecache import FileResolver
from mythbox.mythtv.conn import inject_conn
from mythbox.util import safe_str

log = logging.getLogger('mythbox.cache')

# =============================================================================
class MythThumbnailResolver(FileResolver):
    
    def __init__(self, conn=None):
        self._conn = conn
            
    def conn(self):
        return self._conn
    
    @inject_conn
    def store(self, program, dest):
        """
        @type program : RecordedProgram  
        @param dest: file to save downloaded program thumbnail to
        """
        if self.conn().getThumbnailCreationTime(program, program.hostname()) is None:
            self.conn().generateThumbnail(program, program.hostname())
        self.conn().transferFile(program.getRemoteThumbnailPath(), dest, program.hostname())
            
    def hash(self, program):
        return md5.new(safe_str(program.getRemoteThumbnailPath())).hexdigest()
        
# =============================================================================
class MythChannelIconResolver(FileResolver):
    
    def __init__(self, conn=None):
        self._conn = conn
            
    def conn(self):
        return self._conn
    
    @inject_conn
    def store(self, channel, dest):
        """
        @type channel : Channel 
        @param dest: file to save downloaded chanel icon to
        """
        if channel.getIconPath():
            # TODO: Can channel icons be requested from slave backend? Replace None with backend hostname 
            #       if this turns out to be true.
            self.conn().transferFile(channel.getIconPath(), dest, None)
        else:
            log.debug('Channel %s has no icon' % channel.getChannelName())
            
    def hash(self, channel):
        if channel.getIconPath():
            return md5.new(safe_str(channel.getIconPath())).hexdigest()
