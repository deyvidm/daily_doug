import pytest


raw_checkin_html = [
	{
		'description': 'Standard checkin structure -- happy days.',
		'content': '''
			<div class="item" id="checkin_740178339" data-checkin-id="740178339">
			<div class="avatar">
			<div class="avatar-holder">
			<span class="supporter"></span> <a href="/user/doug1516">
			<img class="lazy" data-original="https://untappd.akamaized.net/profile/460470c554b72ecd2a34ae2d497139e5_100x100.JPG" alt="Doug C." src="https://untappd.akamaized.net/profile/460470c554b72ecd2a34ae2d497139e5_100x100.JPG" style="display: inline;">
			</a>
			</div>
			</div>
			<div class="checkin">
			<div class="top">
			<a href="/b/5-paddles-brewing-company-love-you-to-death/2399364" class="label">
			<img class="lazy" data-original="https://untappd.akamaized.net/site/beer_logos/beer-2399364_df54c_sm.jpeg" alt="5 Paddles Brewing Company by Love You To Death" src="https://untappd.akamaized.net/site/beer_logos/beer-2399364_df54c_sm.jpeg" style="display: inline;">
			</a>
			<p class="text">
			<a href="/user/doug1516" class="user">Doug C.</a> is drinking a <a href="/b/5-paddles-brewing-company-love-you-to-death/2399364">Love You To Death</a> by <a href="/5PaddlesBrewingCompany">5 Paddles Brewing Company</a> at <a href="/v/the-hazy-cellar/5759656">The Hazy Cellar</a>
			</p>
			<div class="checkin-comment">
			<p class="comment-text" id="translate_740178339">
			Honey plays a secondary role in this braggot. Very close to an Imperial stout. Tons of roasted malt chocolate and coffee flavours. </p>
			<div class="rating-serving">
			<p class="serving">
			<img src="https://untappd.akamaized.net/static_app_assets/bottle@3x.png">
			<span>Bottle</span>
			</p>
			<span class="rating small r400"></span>
			</div>
			<span style="display: block; clear: both;"></span>
			</div>
			<p class="photo">
			<a href="/user/doug1516/checkin/740178339" class="track-click" data-track="activity_feed" data-href=":feed/viewcheckinphoto">
			<img class="lazy" data-original="https://untappd.akamaized.net/photos/2019_04_22/d5a3934ded80f47f243bdbeb5484b14c_640x640.jpg" img="Check-in Photo" src="https://untappd.akamaized.net/photos/2019_04_22/d5a3934ded80f47f243bdbeb5484b14c_640x640.jpg" style="display: inline;">
			</a>
			</p>
			</div>
			<div class="feedback">
			<div class="actions_bar">
			</div>
			<div class="bottom">
			<a href="/user/doug1516/checkin/740178339" class="time timezoner track-click" data-track="activity_feed" data-href=":feed/viewcheckindate" data-gregtime="Mon, 22 Apr 2019 17:49:26 +0000">22 Apr 19</a>
			<a href="/user/doug1516/checkin/740178339" class="track-click" data-track="activity_feed" data-href=":feed/viewcheckintext">View Detailed Check-in</a>
			</div>
			<div class="cheers"> <span class="count">
			<span>3</span>
			</span><span class="toast-list">
			<a class="user-toasts tip track-click" data-user-name="J-Mu" href="/user/J-Mu" title="James M." data-track="activity_feed" data-href=":feed/userprofiletoast">
			<img class="lazy" data-original="https://untappd.akamaized.net/profile/9d3d858370372ca0584962bfe5139b36_100x100.JPG" src="https://untappd.akamaized.net/profile/9d3d858370372ca0584962bfe5139b36_100x100.JPG" style="display: inline;">
			</a>
			<a class="user-toasts tip track-click" data-user-name="RalphVH" href="/user/RalphVH" title="Ralph V." data-track="activity_feed" data-href=":feed/userprofiletoast">
			<img class="lazy" data-original="https://untappd.akamaized.net/profile/bd4798f186e79197adc912e8e3255345_100x100.JPG" src="https://untappd.akamaized.net/profile/bd4798f186e79197adc912e8e3255345_100x100.JPG" style="display: inline;">
			</a>
			<a class="user-toasts tip track-click" data-user-name="komalthelist" href="/user/komalthelist" title="Komal" data-track="activity_feed" data-href=":feed/userprofiletoast">
			<img class="lazy" data-original="https://untappd.akamaized.net/profile/1ee82ee430471271d28bd3e4bce17678_100x100.jpg" src="https://untappd.akamaized.net/profile/1ee82ee430471271d28bd3e4bce17678_100x100.jpg" style="display: inline;">
			</a>
			</span>
			</div>
			<div class="comments">
			<div class="comments-container">
			</div>
			</div>
			</div>
			</div>
			</div>
		'''
	},{
		'description': 'missing image',
		'content': '''
			<div class="item" id="checkin_740162051" data-checkin-id="740162051">
			<div class="avatar">
			<div class="avatar-holder">
			<span class="supporter"></span> <a href="/user/doug1516">
			<img class="lazy" data-original="https://untappd.akamaized.net/profile/460470c554b72ecd2a34ae2d497139e5_100x100.JPG" alt="Doug C." src="https://untappd.akamaized.net/profile/460470c554b72ecd2a34ae2d497139e5_100x100.JPG" style="display: inline;">
			</a>
			</div>
			</div>
			<div class="checkin">
			<div class="top">
			<a href="/b/brewery-ommegang-game-of-thrones-king-in-the-north/2921396" class="label">
			<img class="lazy" data-original="https://untappd.akamaized.net/site/beer_logos/beer-2921396_d860f_sm.jpeg" alt="Brewery Ommegang by Game of Thrones: King in the North" src="https://untappd.akamaized.net/site/beer_logos/beer-2921396_d860f_sm.jpeg" style="display: inline;">
			</a>
			<p class="text">
			<a href="/user/doug1516" class="user">Doug C.</a> is drinking a <a href="/b/brewery-ommegang-game-of-thrones-king-in-the-north/2921396">Game of Thrones: King in the North</a> by <a href="/breweryommegang">Brewery Ommegang</a> at <a href="/v/the-hazy-cellar/5759656">The Hazy Cellar</a>
			</p>
			<div class="checkin-comment">
			<p class="comment-text" id="translate_740162051">
			Chocolate. Coffee. Bourbon. Vanilla. Love live Winterfell! </p>
			<div class="rating-serving">
			<p class="serving">
			<img src="https://untappd.akamaized.net/static_app_assets/bottle@3x.png">
			<span>Bottle</span>
			</p>
			<span class="rating small r425"></span>
			</div>
			<span style="display: block; clear: both;"></span>
			</div>
			</div>
			<div class="feedback">
			<div class="actions_bar">
			</div>
			<div class="bottom">
			<a href="/user/doug1516/checkin/740162051" class="time timezoner track-click" data-track="activity_feed" data-href=":feed/viewcheckindate" data-gregtime="Mon, 22 Apr 2019 16:53:19 +0000">22 Apr 19</a>
			<a href="/user/doug1516/checkin/740162051" class="track-click" data-track="activity_feed" data-href=":feed/viewcheckintext">View Detailed Check-in</a>
			</div>
			<div class="cheers"> <span class="count">
			<span>3</span>
			</span><span class="toast-list">
			<a class="user-toasts tip track-click" data-user-name="RalphVH" href="/user/RalphVH" title="Ralph V." data-track="activity_feed" data-href=":feed/userprofiletoast">
			<img class="lazy" data-original="https://untappd.akamaized.net/profile/bd4798f186e79197adc912e8e3255345_100x100.JPG" src="https://untappd.akamaized.net/profile/bd4798f186e79197adc912e8e3255345_100x100.JPG" style="display: inline;">
			</a>
			<a class="user-toasts tip track-click" data-user-name="J-Mu" href="/user/J-Mu" title="James M." data-track="activity_feed" data-href=":feed/userprofiletoast">
			<img class="lazy" data-original="https://untappd.akamaized.net/profile/9d3d858370372ca0584962bfe5139b36_100x100.JPG" src="https://untappd.akamaized.net/profile/9d3d858370372ca0584962bfe5139b36_100x100.JPG" style="display: inline;">
			</a>
			<a class="user-toasts tip track-click" data-user-name="JanickPelletier" href="/user/JanickPelletier" title="Janick P." data-track="activity_feed" data-href=":feed/userprofiletoast">
			<img class="lazy" data-original="https://untappd.akamaized.net/profile/5219b693d39bb3c4e87353fc71df43ba_100x100.jpg" src="https://untappd.akamaized.net/profile/5219b693d39bb3c4e87353fc71df43ba_100x100.jpg" style="display: inline;">
			</a>
			</span>
			</div>
			<div class="comments">
			<div class="comments-container">
			</div>
			</div>
			</div>
			</div>
			</div>
		'''
	},{
		'description': 'no location',
		'content': '''
			<div class="item" id="checkin_746267291" data-checkin-id="746267291">
			<div class="avatar">
			<div class="avatar-holder">
			<span class="supporter"></span> <a href="/user/doug1516">
			<img class="lazy" data-original="https://untappd.akamaized.net/profile/460470c554b72ecd2a34ae2d497139e5_100x100.JPG" alt="Doug C." src="https://untappd.akamaized.net/profile/460470c554b72ecd2a34ae2d497139e5_100x100.JPG" style="display: inline;">
			</a>
			</div>
			</div>
			<div class="checkin">
			<div class="top">
			<a href="/b/nickel-brook-brewing-co-cafe-del-bastardo-2018/2476273" class="label">
			<img class="lazy" data-original="https://untappd.akamaized.net/site/beer_logos/beer-2476273_819c1_sm.jpeg" alt="Nickel Brook Brewing Co. by Cafe Del Bastardo (2018)" src="https://untappd.akamaized.net/site/beer_logos/beer-2476273_819c1_sm.jpeg" style="display: inline;">
			</a>
			<p class="text">
			<a href="/user/doug1516" class="user">Doug C.</a> is drinking a <a href="/b/nickel-brook-brewing-co-cafe-del-bastardo-2018/2476273">Cafe Del Bastardo (2018)</a> by <a href="/nickelbrook">Nickel Brook Brewing Co.</a>
			</p>
			<div class="checkin-comment">
			<p class="comment-text" id="translate_746267291">
			The coffee is incredible here (and I don’t even drink coffee on its own). The bourbon, vanilla and oak just blend naturally with the coffee. </p>
			<div class="rating-serving">
			<p class="serving">
			<img src="https://untappd.akamaized.net/static_app_assets/bottle@3x.png">
			<span>Bottle</span>
			</p>
			<span class="rating small r450"></span>
			</div>
			<span class="badge">
			<img class="lazy" data-original="https://untappd.akamaized.net/badges/bdg_ImperialStout_sm.jpg" alt="Imperial Czar (Level 31)" src="https://untappd.akamaized.net/badges/bdg_ImperialStout_sm.jpg" style="display: inline-block;">
			<span>Earned the Imperial Czar (Level 31) badge!</span>
			</span>
			<span style="display: block; clear: both;"></span>
			</div>
			<p class="photo">
			<a href="/user/doug1516/checkin/746267291" class="track-click" data-track="activity_feed" data-href=":feed/viewcheckinphoto">
			<img class="lazy" data-original="https://untappd.akamaized.net/photos/2019_05_07/ac064364a7ac0efc4ef7524c52755ce1_640x640.jpg" img="Check-in Photo" src="https://untappd.akamaized.net/photos/2019_05_07/ac064364a7ac0efc4ef7524c52755ce1_640x640.jpg" style="display: inline;">
			</a>
			</p>
			</div>
			<div class="feedback">
			<div class="actions_bar">
			</div>
			<div class="bottom">
			<a href="/user/doug1516/checkin/746267291" class="time timezoner track-click" data-track="activity_feed" data-href=":feed/viewcheckindate" data-gregtime="Tue, 07 May 2019 01:17:27 +0000">18 hours ago</a>
			<a href="/user/doug1516/checkin/746267291" class="track-click" data-track="activity_feed" data-href=":feed/viewcheckintext">View Detailed Check-in</a>
			 </div>
			<div class="cheers"> <span class="count">
			<span>4</span>
			</span><span class="toast-list">
			<a class="user-toasts tip track-click" data-user-name="kabin" href="/user/kabin" title="Chris K." data-track="activity_feed" data-href=":feed/userprofiletoast">
			<img class="lazy" data-original="https://untappd.akamaized.net/profile/6c772b7edac1b070733f7023d13b987e_100x100.jpg" src="https://untappd.akamaized.net/profile/6c772b7edac1b070733f7023d13b987e_100x100.jpg" style="display: inline;">
			</a>
			<a class="user-toasts tip track-click" data-user-name="walz22" href="/user/walz22" title="Mike" data-track="activity_feed" data-href=":feed/userprofiletoast">
			<img class="lazy" data-original="https://untappd.akamaized.net/profile/bebcd184b7ef8aa04535e7f3fb097145_100x100.jpg" src="https://untappd.akamaized.net/profile/bebcd184b7ef8aa04535e7f3fb097145_100x100.jpg" style="display: inline;">
			</a>
			<a class="user-toasts tip track-click" data-user-name="ChampionsPrerogative" href="/user/ChampionsPrerogative" title="Steven" data-track="activity_feed" data-href=":feed/userprofiletoast">
			<img class="lazy" data-original="https://untappd.akamaized.net/profile/7603679c49fbb1ac746162edebd9a322_100x100.jpg" src="https://untappd.akamaized.net/profile/7603679c49fbb1ac746162edebd9a322_100x100.jpg" style="display: inline;">
			</a>
			<a class="user-toasts tip track-click" data-user-name="J-Mu" href="/user/J-Mu" title="James M." data-track="activity_feed" data-href=":feed/userprofiletoast">
			<img class="lazy" data-original="https://untappd.akamaized.net/profile/9d3d858370372ca0584962bfe5139b36_100x100.JPG" src="https://untappd.akamaized.net/profile/9d3d858370372ca0584962bfe5139b36_100x100.JPG" style="display: inline;">
			</a>
			</span>
			</div>
			<div class="comments">
			<div class="comments-container">
			</div>
			</div>
			</div>
			</div>
			</div>
		'''
	}
]

def get_test_checkin():
	return raw_checkin_html[0]['content']
