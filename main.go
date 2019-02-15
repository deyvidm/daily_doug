package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
	"qol"

	"github.com/PuerkitoBio/goquery"
)

func main() {

	// doc := fetchPage("https://untappd.com/user/doug1516")
	// doc.Find("h3").Each(func(i int, s *goquery.Selection) {
	// fmt.Println(s.Text())
	// })
	saveTimeOfLatestDoug()
}

// func fetchNextDoug(previousDougTime time) {
// }

func saveTimeOfLatestDoug() {
	ex, err := os.Executable()
	qol.Check(err)

	filename := filepath.Dir(ex) + "/time_of_last_doug.dat"
	time := []byte("feb 12 1900\n")

	fmt.Println("saving state to " + filename)

	err = ioutil.WriteFile(filename, time, 0644)
	qol.Check(err)
}

func fetchPage(url string) *goquery.Document {
	client := &http.Client{}
	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36")
	resp, _ := client.Do(req)

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	qol.Check(err)

	resp.Body.Close()
	return doc
}
