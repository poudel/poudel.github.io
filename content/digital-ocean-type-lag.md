---
date: 2017-09-08
location: Kathmandu, Nepal
title: SSH terminal typing lag in a Digital Ocean droplet
description: Type lag caused by network latency in digital ocean servers
draft: false
---

A while ago, I played around with a Digital Ocean droplet for a few weeks.
This post was a draft from that time.
I don't have the droplet anymore but, I am going to publish this post
just in case some other person has to go through the same issue.

The data center region I chose while creating the droplet was New York. Now this
would not have been an issue if I wasn't living halfway across the world, in Nepal.
Although the site served through this droplet was loading fine, the SSH
shell connected to it would lag horribly. The terminal would
only show a character I typed after half a second of actually typing.
Needless to say, it was quite frustrating. I ran out of patience not long after that.

I looked around the internet and found that it was because of network latency.
I moved the location of the droplet to an Indian datacenter by following
[this tutorial](https://www.digitalocean.com/community/tutorials/how-to-migrate-digitalocean-droplets-using-snapshots).

After this, the annoying latency issue was resolved.
