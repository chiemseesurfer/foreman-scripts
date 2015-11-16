# License

This files are free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

* * *

1. Introduction
===============
In this repo I post some of my foreman workarounds, just to share it with the
world and to help someone not to die stupid ;)

2. Scripts
===============
## foreman_dhcp_workaround.py

It's a small workaround which is scheduled by cron every night.

I use a small IP range for installation which is provided by dhcp running on the
foreman host. After installation I change the IP to the right address. I can't
use the real address because of some network infrastructure guideluines. And I
don't want to do the IP change in foreman by hand. That's why I created that
small workaround which cleans up dhcp and changes the address in foreman to the
dns resolvable address.
