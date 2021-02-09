package main

// const clientID = "FEB3594FDFACD0D4E55B44CC23F8681FB856621D"
// const clientSecret = "4619E5C13A7821B0854329191B25D7C2AE2C52B0"
// const authInfo = `?client_id=${clientId}&client_secret=${clientSecret}`

// const lookupuser = "doug1516"

// var cachedFeed = ""

import "untappd"

func main() {

	untappd.FetchCheckinHTML("993738934")
	// bod := fetchFeedHTML()
	// defer bod.Close()

	// // buf := new(bytes.Buffer)
	// // buf.ReadFrom(bod)
	// // newStr := buf.String()

	// // fmt.Printf(newStr)
	// scrapeFeedPics(bod)
}
