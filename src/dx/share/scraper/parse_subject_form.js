var seriesOptions = document.querySelectorAll('select.form-control.featuredSelect1 option')
var seriesOptArr = Array.from(seriesOptions, s => String('"' + s.value + '","' + s.text + '"'))
copy(Array.from(seriesOptArr).join("\n"))
// `xclip -o > topics.csv` and manually delete first line with '"All", "Browse All"'
