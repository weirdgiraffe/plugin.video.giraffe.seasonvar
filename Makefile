VERSION=$(shell xmllint --xpath "//addon/@version" addon.xml | sed 's/^.*"\([^"]*\)"$$/\1/')
zip:
	$(RM) $(PWD)/plugin.video.me.seasonvar-$(VERSION).zip
	git archive --format zip --prefix=plugin.video.me.seasonvar/ --output $(PWD)/plugin.video.me.seasonvar-$(VERSION).zip master

localcleanup: zip
	ssh localkodi "rm -rf ~/.kodi"
	scp plugin.video.me.seasonvar-*.zip localkodi:

localupdate:
	scp -r resources/* localkodi:.kodi/addons/plugin.video.me.seasonvar/resources/


