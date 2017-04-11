ADDON=$(shell xmllint --xpath "//addon/@id" addon.xml | sed 's/^.*"\([^"]*\)"$$/\1/')
VERSION=$(shell xmllint --xpath "//addon/@version" addon.xml | sed 's/^.*"\([^"]*\)"$$/\1/')
BRANCH=$(shell git branch | sed '/^*/!d;s/\* //')
zip:
	$(RM) $(PWD)/$(ADDON)-$(VERSION).zip
	git archive --format zip --prefix=$(ADDON)/ --output $(PWD)/$(ADDON)-$(VERSION).zip $(BRANCH)

clean:
	$(RM) -rf resources/site-packages/plugin_video/__pycache__
	$(RM) -rf resources/site-packages/plugin_video/tests/__pycache__
	$(RM) -rf resources/site-packages/kodi/__pycache__
	$(RM) -rf resources/site-packages/mock_kodi/__pycache__
	$(RM) -rf resources/site-packages/seasonvar/__pycache__
	$(RM) -rf resources/site-packages/seasonvar/tests/__pycache__
	$(RM) resources/site-packages/plugin_video/*.pyc
	$(RM) resources/site-packages/plugin_video/tests/*.pyc
	$(RM) resources/site-packages/kodi/*.pyc
	$(RM) resources/site-packages/mock_kodi/*.pyc
	$(RM) resources/site-packages/seasonvar/*.pyc
	$(RM) resources/site-packages/seasonvar/tests/*.pyc

localcleanup: zip
	ssh localkodi "rm -rf ~/.kodi"
	ssh localkodi "rm -rf ~/plugin.video.*.zip"
	scp plugin.video.* localkodi:.

localpush: clean
	ssh localkodi 'rm -rf .kodi/addons/$(ADDON)/resources/site-packages/*'
	scp -r resources/site-packages/* localkodi:.kodi/addons/$(ADDON)/resources/site-packages/


