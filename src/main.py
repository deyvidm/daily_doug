def main(logger, checkins, last_checkin_id): 
    slackblock_stack = []
    # the checkins are fetched latest -> oldest
    # > clean checkin data
    # > store the first checkin's id as 'latest' -- this is the latest checkin reported by untappd
    # > if the current checkin's id is the same as the one from last run, then we've run out of new checkins
    # > if the previous is true, AND the current checkin's id is the same as the 'latest' checkin's id, then there are no new checkins at all
    #   > just terminate, no work left to do
    # > else, store the ID and finish sending the remaining new checkins
    # > store the latest checkin ID and move on

    # in order to display them in the right order, the list needs to be reversed
    # also need to store the latest checkin's id for next run, which is easier when it's at index [0]

    # fetch checkins in default untappd order (latest -> oldest)
    latest_checkin_id = None
    for i, c in enumerate(checkins):
        clean_checkin = scrape_checkin(c)

        if i == 0:
            latest_checkin_id = clean_checkin['checkin_id']

        if clean_checkin['checkin_id'] == last_checkin_id:
            if clean_checkin['checkin_id'] == latest_checkin_id:
                logger.info("no new checkins")
                return
            # write_latest_checkin_id(latest_checkin_id)
            break

        # convert to slack message blocks
        slackblock_stack.append(build_slackblock(clean_checkin))

    # reverse and continue
    slackblock_stack.reverse()

    for c in slackblock_stack:
        post_to_webhook(os.environ['webhook_url'], json.dumps(c))

    write_latest_checkin_id(latest_checkin_id, config)
