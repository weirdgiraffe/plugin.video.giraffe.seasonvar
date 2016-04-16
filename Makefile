ADDON=$(shell xmllint --xpath "//addon/@id" addon.xml | sed 's/^.*"\([^"]*\)"$$/\1/')
VERSION=$(shell xmllint --xpath "//addon/@version" addon.xml | sed 's/^.*"\([^"]*\)"$$/\1/')
BRANCH=$(shell git branch | sed '/^*/!d;s/\* //')
zip:
	$(RM) $(PWD)/$(ADDON)-$(VERSION).zip
	git archive --format zip --prefix=$(ADDON)/ --output $(PWD)/$(ADDON)-$(VERSION).zip $(BRANCH)

localcleanup: zip
	ssh localkodi "rm -rf ~/.kodi"
	ssh localkodi "rm -rf ~/plugin.video.*.zip"
	scp plugin.video.* localkodi:.

localpush:
	scp plugin.video.*.zip localkodi:.


