// On https://bookstore.ams.org/GSM#BookSeries?GSM?all?all?page=0
var productcodes = document.querySelectorAll(".baseProductCode")

// This will not work as they're not all numeric:
// Math.max(...Array.from(productcodes).map(function(s){   return Number(s.innerText.split("/").reverse()[0]) }))

var listing = Array.from(productcodes).map(function(s){
	var n = s.innerText.split("/").reverse()[0]
	var isH = n.endsWith(".H"); return [Number(n.replace(/\.H$/g, "")),isH]
})

var listing_str = listing.map(function(s){
	return s.toString() // No string quoting as it's not 'free' text
}).join("\n")

copy(listing_str + "\n")

// Advance to the next page before getting listing
document.querySelector("a.t-nav-next:last-of-type").click()

// Then `xclip -o >> book-series-number-listing.csv` while the page reloads
