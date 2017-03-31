### How android knows it's on an expensive connection

#### 安卓手机热点的特殊行为

Keywords: android, hotspot, tethering, `ANDROID_METERED`, expensive

When an android phone is using another android phone's hotspot, it knows it's on a "metered connection" and therefore disables the expensive sync options ( eg: photo sync). How does it know this? The android hotspot sends DHCP Option 43 (Vendor specific options) with the value ANDROID_METERED. The client, if it sees ANDROID_METERED anywhere in the option 43 values, turns on the "expensive data connection" option.


The problem with this is that the DHCP server isn't supposed to send DHCP options unless the DHCP client asked for it, and the android DHCP client doesn't ask for option 43 (at least under ≤4.3). But the android DHCP server, just returns option 43 anyway. It really shouldn't do that, and the client listens for options it's not requested, which it shouldn't do either. The practical upshot is that if you're trying to set this option, remember to force it rather than wait for the client to ask for it.


From [TetherController](https://android.googlesource.com/platform/system/netd/+/7b90f090d9e48e76d5fb3f674eb7bfd5fbdfaf7d/TetherController.cpp):

```
args[0] = (char *)"/system/bin/dnsmasq";
args[1] = (char *)"--keep-in-foreground";
args[2] = (char *)"--no-resolv";
args[3] = (char *)"--no-poll";
// TODO: pipe through metered status from ConnService
args[4] = (char *)"--dhcp-option-force=43,ANDROID_METERED";
args[5] = (char *)"--pid-file";
args[6] = (char *)"";
```

The comment here shows that all tethering is assumed to be "metered", and there is a todo to fix it.

And from [core.java.android.net.DhcpInfoInternal](https://bitbucket.org/seandroid/frameworks-base/src/33034b13cae1/core/java/android/net/DhcpInfoInternal.java)

```
public boolean hasMeteredHint() {
    if (vendorInfo != null) {
        return vendorInfo.contains("ANDROID_METERED");
    } else {
        return false;
    }
}
```

Notes

I'm unaware of any laptops that listen to this attribute, but it wouldn't be hard to add. I'm also unaware of any support in iOS for this attribute, or another similar attribute.

There's Settings > Data usage > ⋮ > Mobile Hotspots, which appears to be a similar thing. "Apps can be restricted from using these networks when in the background and can also warn you about using these networks for large downloads."

Ideas

There are some obvious ideas that might be helpful. If you're on an expensive internet connection, then using this option to tell android to back off is of course fairly obvious. If you're a laptop doing sync, or auto updates, listening for this option would be very welcome as well.

Using this to get android phones to back off on congested wifi

One idea would be to look at the amount of spare air time there is on the wifi interface, and if it starts looking busy, then start handing this option out. If the airtime is mostly free then don't hand it out.

Airtime is fairly hard to measure, and bit of a layer violation, so a good proxy for airtime might be combined in/out bandwidth on the interface. 
Bandwidth is fairly hard for a dhcp server to measure too, so you might want to use the number of associated stations as a proxy for bandwidth. And since number of associated stations is annoying to measure from a DHCP server, you might just want to count the number of DHCP leases as a proxy for number of associations.

Using this to stop your laptop from trying to update while tethered

If you're tethering, you might not want your laptop to automatically try and update everything. Even if you have enough of a data cap to deal with this, you might not want to have it congest all your bandwidth while you're trying to get some emergency work done.

** (UNTESTED) **

You can trigger this by dropping an executable script in `/etc/dhcp/dhclient-enter-hooks.d/`, this should look for an environmental variable called new_vendor_encapsulated_options and see if it contains the string `ANDROID_METERED`.

Some things to do:

```
 gconftool --set --type bool /apps/apps-notifier/auto_launch false
 dconf write /com/ubuntu/update-notifier/auto_launch false
 ```

You might also want to look at `gconftool -R / | egrep 'auto|sync' and dtool dump / | egrep 'auto|sync'` for other things you might want to flip off.

If I ever get around to testing it, I'll put an example script here.

[Reference: How android knows it's on an expensive connection](http://www.lorier.net/docs/android-metered)