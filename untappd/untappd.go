package untappd

import (
	"fmt"
	"io"
	"log"
	"net/http"

	"github.com/PuerkitoBio/goquery"
)

func FetchCheckinHTML(checkinID string) io.ReadCloser {
	url := fmt.Sprintf("https://untappd.com/user/doug1516/checkin/%s", checkinID)
	res, err := http.Get(url)
	if err != nil {
		panic(err)
	}
	if res.StatusCode != 200 {
		log.Fatalf("status code error: %d %s", res.StatusCode, res.Status)
	}
	return res.Body
}

func ScrapeFeedPics(body io.Reader) {
	// Load the HTML document
	doc, err := goquery.NewDocumentFromReader(body)
	if err != nil {
		log.Fatal(err)
	}

	// Find the review items
	doc.Find("div[id^='checkin']").Each(func(i int, s *goquery.Selection) {
		picURL := s.Find("img[img='Check-in Photo']").AttrOr("data-original", "undefined")
		title := s.Find("p.text").Text()
		fmt.Printf("Review %d: %s - %s\n\n", i, title, picURL)
	})
}
