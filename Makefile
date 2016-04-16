ADDON=$(shell xmllint --xpath "//addon/@id" addon.xml | sed 's/^.*"\([^"]*\)"$$/\1/')
VERSION=$(shell xmllint --xpath "//addon/@version" addon.xml | sed 's/^.*"\([^"]*\)"$$/\1/')
BRANCH=$(shell git branch | sed '/^*/!d;s/\* //')
zip:
	$(RM) $(PWD)/$(ADDON)-$(VERSION).zip
	git archive --format zip --prefix=$(ADDON)/ --output $(PWD)/$(ADDON)-$(VERSION).zip $(BRANCH)

cleanup:
	$(RM) resources/site-packages/*.pyc
	$(RM) -r resources/site-packages/__pycache__
	$(RM) resources/site-packages/addon/*.pyc
	$(RM) -r resources/site-packages/addon/__pycache__
	$(RM) resources/site-packages/seasonvar/*.pyc
	$(RM) -r resources/site-packages/seasonvar/__pycache__
	$(RM) tests/*.pyc
	$(RM) -r tests/__pycache__

localcleanup: zip
	ssh localkodi "rm -rf ~/.kodi"
	ssh localkodi "rm -rf ~/plugin.video.*.zip"
	scp plugin.video.* localkodi:.

localpush: cleanup
	scp -r resources/site-packages/* localkodi:.kodi/addons/$(ADDON)/resources/site-packages/


