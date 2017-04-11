ADDON=$(shell xmllint --xpath "//addon/@id" addon.xml | sed 's/^.*"\([^"]*\)"$$/\1/')
VERSION=$(shell xmllint --xpath "//addon/@version" addon.xml | sed 's/^.*"\([^"]*\)"$$/\1/')
BRANCH=$(shell git branch | sed '/^*/!d;s/\* //')
zip:
	$(RM) $(PWD)/$(ADDON)-$(VERSION).zip
	git archive --format zip --prefix=$(ADDON)/ --output $(PWD)/$(ADDON)-$(VERSION).zip $(BRANCH)

clean:
	$(RM) resources/site-packages/plugin_video/*.pyc
	$(RM) -rf resources/site-packages/plugin_video/__pycache__
	$(RM) resources/site-packages/plugin_video/tests/*.pyc
	$(RM) -rf resources/site-packages/plugin_video/tests/__pycache__
	$(RM) resources/site-packages/kodi/*.pyc
	$(RM) -rf resources/site-packages/kodi/__pycache__
	$(RM) resources/site-packages/seasonvar/*.pyc
	$(RM) -rf resources/site-packages/seasonvar/__pycache__
	$(RM) resources/site-packages/tests/*.pyc
	$(RM) -rf resources/site-packages/tests/__pycache__

localcleanup: zip
	ssh localkodi "rm -rf ~/.kodi"
	ssh localkodi "rm -rf ~/plugin.video.*.zip"
	scp plugin.video.* localkodi:.

localpush: clean
	scp -r resources/site-packages/* localkodi:.kodi/addons/$(ADDON)/resources/site-packages/


